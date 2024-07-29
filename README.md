# Employee Search MicroService

## Introduction

Hello,

In this coding exercise I be addressing an issue/task that is central to day-to-day work: writing and maintaining microservices. This exercise aims to showcase a small microservice that fetches/calculates information about employees, creates plots and can be remotely health checked, all while running in a container.

## The service

The API provides the following basic functionalities to retrieve and serve employee data from a data source. Typically, this would be some SQL database. However, for the sake of simplicity, in this task, I am using two CSV files with fake data in the `./employees` folder.

#### 1. Getting employee (name, company, ... )

- **Calling `GET /api/employees?name=:name` returns a JSON object containing the list of all the employees who matches the `:name`**.
- `:name` is an url-encoded string.
  - If `:name` is a single word, an entry is considered as a match if either of the `first_name` or `last_name` matches the `:name`.
  - When the `:name` is multiple words, an entry would be considered as a match if the last word matches the `last_name` and the rest matches the `first_name`.
- Returned objected has the following keys: `{ name, company, address, phone, email }`
- The following rules apply:
  - `name` is full name, i.e, `first_name<space>last_name` .
  - `address` is constructed differently for UK and US.
    - For UK: `address, city, upper_case(county), postal UK`.
    - For US: `address, city, state zip, USA`.
  - If both phones are available, select `phone1` for UK and `phone2` for US. Also, the country code is prepended.

#### 2. Getting stats

- **Calling `GET /api/employees/` without any parameter returns a JSON array representing with following keys**.
  - `{ region, count, employees }`.
    - `region` is `state` for US and `county` for UK.
    - `count` is number of employees from that `region`.
    - `employees` is a list containing the full name of those employees

#### 3. Company wages

- **Calling `GET /api/wage_stats?company_name=:name&country=:country` returns an image object that shows the wage distribution of the given company**.
  - `country` is an optional query parameter with the following accepted values: `UK`, `US`.
    - If country is given, use only the data from the given country, otherwise all data should be considered.
  - Consider using the sum of `base_salary` and `other_pay` to get wages.
  - The wage distribution is drawn everytime when this endpoint is called and returned as a response with `media_type` `"image/png"`.

## Run it

`docker build -t micro_flask .`

`docker run -p 5000:5000 micro_flask`

or

`pip install -r requirements.txt`

`python main.py`
