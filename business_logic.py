import io
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# .iloc[0] is a bit sloppy, because it doesnt account for the case where there are
# multiple rows i.e. multiple people with the same name

def address_it(df, country):
    """
    Formats the address based on the country.

    Parameters:
    df (pandas.DataFrame): DataFrame containing address information.
    country (str): The country code ("us" or "uk").

    Returns:
    str: The formatted address if the country code is "us" or "uk", None otherwise.
    """
    if country == "us":
        return ", ".join([df["address"].iloc[0], df["city"].iloc[0], df["state"].iloc[0] + " " + str(df["zip"].iloc[0]), "USA"])
    elif country == "uk":
        return ", ".join([df["address"].iloc[0], df["city"].iloc[0], df["county"].iloc[0].upper(), df["postal"].iloc[0] + " UK"])
    else:
        return None


def phone_it(df, country):
    """
    Returns the phone number based on the country.

    Parameters:
    df (pandas.DataFrame): DataFrame containing phone information.
    country (str): The country code ("us" or "uk").

    Returns:
    str: The phone number if available, None otherwise.
    """
    if df['phone1'].notna().any() and df['phone2'].notna().any():
        if country == "uk":
            return df['phone1'].iloc[0]
        elif country == "us":
            return df['phone2'].iloc[0]
    elif df['phone1'].notna().any():
        return df['phone1'].iloc[0]
    elif df['phone2'].notna().any():
        return df['phone2'].iloc[0]
    else:
        return None
    

# rewrite as match ?
def check_matches(matches_uk, matches_us):
    """
    Checks the matches from UK and US data.

    Parameters:
    matches_uk (pandas.DataFrame): DataFrame containing UK matches.
    matches_us (pandas.DataFrame): DataFrame containing US matches.

    Returns:
    tuple: A tuple containing the matched DataFrame and country code.
    """ 
    if matches_uk.empty and not matches_us.empty:
        return matches_us, "us"
    elif matches_us.empty and not matches_uk.empty:
        return matches_uk, "uk"
    elif matches_us.empty and matches_uk.empty:
        return None, None
    elif not matches_us.empty and not matches_uk.empty:
        return None, "both"


def get_employee_data(df_us, df_uk, name):
    # doesnt account for the case someone has just one name: Madonna
    """
    Retrieves the employee data based on the name.

    Parameters:
    df_us (pandas.DataFrame): DataFrame containing US data.
    df_uk (pandas.DataFrame): DataFrame containing UK data.
    name (str): The name of the employee.

    Returns:
    dict: A dictionary containing the employee name, company name, address, phone and email.
    """
    names = name.split(' ')
    if len(names) == 1:
        matches_uk = df_uk[df_uk['first_name'].str.contains(name) | df_uk['last_name'].str.contains(name)]
        matches_us = df_us[df_us['first_name'].str.contains(name) | df_us['last_name'].str.contains(name)]
    else:
        first_name = ' '.join(names[:-1]) # in case of multiple first names
        last_name = names[-1]
        matches_uk = df_uk[(df_uk['first_name'].str.contains(first_name)) & (df_uk['last_name'].str.contains(last_name))]
        matches_us = df_us[(df_us['first_name'].str.contains(first_name)) & (df_us['last_name'].str.contains(last_name))]

    matched_country, matched_flag = check_matches(matches_uk, matches_us)

    if matched_flag is not None:
        if matched_flag != "both":
            phone = phone_it(matched_country, matched_flag)
            address = address_it(matched_country, matched_flag)
            full_name = " ".join([matched_country["first_name"].iloc[0], matched_country["last_name"].iloc[0]])
            company_name = matched_country["company_name"].iloc[0]
            email = matched_country["email"].iloc[0]
        else:
            phone = f"{phone_it(matches_uk, 'uk')}, {phone_it(matches_us, 'us')}"
            address = f"{address_it(matches_uk, 'uk')}, {address_it(matches_us, 'us')}"
            full_name = name
            company_name = f"{matches_uk['company_name'].iloc[0]}, {matches_us['company_name'].iloc[0]}"
            email = f"{matches_uk['email'].iloc[0]}, {matches_us['email'].iloc[0]}"

        result = {'name': full_name, 'company_name': company_name,
                   'address': address, 'phone': phone, 'email':email}
        return result
    else:
        print("No matches found")
        return None


def region_stats(df_us, df_uk):
    """
    Calculates the statistics for each region.

    Parameters:
    df_us (pandas.DataFrame): DataFrame containing US data.
    df_uk (pandas.DataFrame): DataFrame containing UK data.

    Returns:
    dict: A dictionary containing the statistics for each region.
    """
    df_us['full_name'] = df_us['first_name'] + ' ' + df_us['last_name']
    df_uk['full_name'] = df_uk['first_name'] + ' ' + df_uk['last_name']
    
    # Group by region and count employees
    count_us = df_us.groupby('state')['full_name'].count().reset_index(name='count')
    count_uk = df_uk.groupby('county')['full_name'].count().reset_index(name='count')
    
    # Get list of employees in each region
    employees_us = df_us.groupby('state')['full_name'].apply(list).reset_index(name='employees')
    employees_uk = df_uk.groupby('county')['full_name'].apply(list).reset_index(name='employees')
    
    # Merge count and employees data
    result_us = pd.merge(count_us, employees_us, on='state').rename(columns={'state': 'region'})
    result_uk = pd.merge(count_uk, employees_uk, on='county').rename(columns={'county': 'region'})
    
    # Concatenate US and UK data
    result = pd.concat([result_us, result_uk])
    
    return result.to_dict('list')

def wage_stats(company_name, country, df_us, df_uk):
    """
    Calculates the wage statistics for a company based on country.

    Parameters:
    company_name (str): The name of the company.
    country (str): The country code ("us" or "uk").
    df_us (pandas.DataFrame): DataFrame containing US data.
    df_uk (pandas.DataFrame): DataFrame containing UK data.

    Returns:
    BytesIO: A BytesIO object containing the plot of the wage distribution.
    """
    if country:
        df = df_us if country == 'US' else df_uk
    else:
        df = pd.concat([df_us, df_uk])
    df = df[df['company_name'] == company_name]
    # check if company exists
    if not df.empty:
        # Calculate wages
        df['wages'] = df['base_salary'] + df['other_pay']

        # Create plot
        plt.figure(figsize=(10, 6))
        sns.histplot(df['wages'], kde=True)
        plt.title('Wage Distribution')
        plt.xlabel('Wages')
        plt.ylabel('Frequency')

        # Save plot to a BytesIO object
        bytes_image = io.BytesIO()
        plt.savefig(bytes_image, format='png')
        bytes_image.seek(0)

        return bytes_image
    else:
        return None

