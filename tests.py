import unittest
import pandas as pd
from business_logic import *


class Test_methods(unittest.TestCase):
    # This is a class that will contain all the tests for the methods in the bussiness_logic.py file
    def setUp(self):
        self.df_uk = pd.read_csv("C:\\Users\\shush\\Desktop\\cobrainer\\uk.csv")
        self.df_us = pd.read_csv("C:\\Users\\shush\\Desktop\\cobrainer\\us.csv")

    def test_phone_it(self):
        data1 = {
        "phone1": "01937-864715",
        "phone2": "907-770-3542"
        }
        data2 = {
            "phone1": "01937-864715",
            "phone2": None
        }
        data3 = {
            "phone1": None,
            "phone2": "907-770-3542"
        }
        data4 = {"phone1": None,
                 "phone2": None}
        # Create a DataFrame from the dictionary
        data1 = pd.DataFrame(data1, index=[0])
        data2 = pd.DataFrame(data2, index=[0])
        data3 = pd.DataFrame(data3, index=[0])
        data4 = pd.DataFrame(data4, index=[0])

        test_cases = {"case1": {"input": (data1, "uk"), "expected_output": "01937-864715"},
                      "case2": {"input": (data1, "us"), "expected_output": "907-770-3542"},
                      "case3": {"input": (data2, "us"), "expected_output": "01937-864715"},
                      "case4": {"input": (data3, "us"), "expected_output": "907-770-3542"},
                      "case5": {"input": (data4, "us"), "expected_output": None}
                    }   

        for _, value in test_cases.items():
            result = phone_it(value["input"][0], value["input"][1])
            self.assertEqual(result, value["expected_output"])

        print("phone_it - Test passed")


    def test_address_it(self):
        us_adress = {"address": "some street N4", "city": "Gotham", "state": "NY", "zip": "4000"}
        uk_adress = {"address": "some street N7", "city": "Gotham", "county": "York", "postal": "42000"}
        us_adress = pd.DataFrame(us_adress, index=[0])
        uk_adress = pd.DataFrame(uk_adress, index=[0])

        test_cases = {"case1": {"input": (uk_adress, "uk"), "expected_output": "some street N7, Gotham, YORK, 42000 UK"},
                      "case2": {"input": (us_adress, "us"), "expected_output": "some street N4, Gotham, NY 4000, USA"},
                      "case3": {"input": (uk_adress, ""), "expected_output": None}
                    }

        for _, value in test_cases.items():
            result = address_it(value["input"][0], value["input"][1])
            self.assertEqual(result, value["expected_output"])
        print("adress_it - Test passed")
            
    def test_check_matches(self):
        full_dict = {"address": "some street N4", "city": "Gotham", "state": "NY", "zip": "4000"}
        empty_dict = {}
        full_df = pd.DataFrame(full_dict, index=[0])
        empty_df = pd.DataFrame(empty_dict, index=[0])

        test_cases = {"case1": {"input": (empty_df, full_df), "expected_output": (full_df, "us")},
                      "case2": {"input": (full_df, empty_df), "expected_output": (full_df, "uk")},
                      "case3": {"input": (empty_df, empty_df), "expected_output": (None, None)},
                      "case4": {"input": (full_df, full_df), "expected_output": (None, "both")}
                    }

        for _, value in test_cases.items():
            result = check_matches(value["input"][0], value["input"][1])
            self.assertEqual(result, value["expected_output"])
        print("check_matches - Test passed")

    def test_region_stats(self):
        dict_us = {"first_name": ["bat", "gan", "spider", "saru", "gun"],
               "last_name": ["man", "dalf", "man", "man", "Doe"],
               "state": ["NY", "NY", "NY", "CA", "CA"]}
        dict_uk = {"first_name": ["John", "Jane", "Jim", "Jack", "Jill"],
                   "last_name": ["Does", "Does", "Doe", "Doe", "Doe"],
                   "county": ["York", "York", "York", "London", "London"]}

        df_us = pd.DataFrame(dict_us)
        df_uk = pd.DataFrame(dict_uk)

        test_cases = {"case1": {"input": (df_us, df_uk), "expected_output": {'region': ['CA', 'NY', 'London', 'York'],
                     'count': [2, 3, 2, 3], 'employees': [['saru man', 'gun Doe'], ['bat man', 'gan dalf', 'spider man'],
                     ['Jack Doe', 'Jill Doe'], ['John Does', 'Jane Does', 'Jim Doe']]}}}

        for _, value in test_cases.items():
            result = region_stats(value["input"][0], value["input"][1])
            self.assertEqual(result, value["expected_output"])
        print("region_stats - Test passed")

    def test_get_employee_data(self):
        dict_us = {"first_name": "Evan", "last_name": "Bruch","address": "some street N4",
                    "city": "Gotham", "state": "NY", "zip": "4000", "phone1": "907-770-3542",
                    "phone2": "01937-864715",
                    "email": "wizard@wizardmail.com", "company_name": "Crowan, Kenneth W Esq"}
        dict_uk = {"first_name": "Gandalf", "last_name": "The Cool","address": "some street N7",
                    "city": "Gotham", "county": "York", "postal": "42000","phone1": "01937-864715","phone2": "907-770-3542",
                    "email": "wizard@wizardmail.com", "company_name": "Crowan, Kenneth W Esq"}
        df_us = pd.DataFrame(dict_us, index=[0])
        df_uk = pd.DataFrame(dict_uk, index=[0])

        test_cases = {"case1": {"input": (df_us, df_uk, "Evan Bruch"), "expected_output": {'name': "Evan Bruch", 'company_name': "Crowan, Kenneth W Esq",
                        'address': "some street N4, Gotham, NY 4000, USA", 'phone': "01937-864715", 'email': "wizard@wizardmail.com"}},
                      "case2": {"input": (df_us, df_uk, "Gandalf"), "expected_output": {'name': "Gandalf The Cool", 'company_name': "Crowan, Kenneth W Esq",
                        'address': "some street N7, Gotham, YORK, 42000 UK", 'phone': "01937-864715", 'email': "wizard@wizardmail.com"}}}

        for _, value in test_cases.items():
            result = get_employee_data(value["input"][0], value["input"][1], value["input"][2])
            self.assertEqual(result, value["expected_output"])
        print("get_employee_data - Test passed")

    def test_wage_stats(self):
        # unfinished - compare plots or dfs
        dict_us = {"company_name" : "WereWorking", "base_salary": "32", "other_pay": "10"}
        dict_uk = {"company_name" : "WereWorking", "base_salary": "22", "other_pay": "20"}

        df_us = pd.DataFrame(dict_us, index=[0])
        df_uk = pd.DataFrame(dict_uk, index=[0])

        test_cases = {"case1": {"input": (df_us, df_uk, "Evan Bruch"), "expected_output": {}}}
        pass


if __name__ == '__main__':
    unittest.main()