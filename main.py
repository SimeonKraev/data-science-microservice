import pandas as pd
from flask import Flask, request, jsonify, send_file
from business_logic import *
import unittest
from tests import Test_methods

# set path vars
df_uk = pd.read_csv("uk.csv")
df_us = pd.read_csv("us.csv")

app = Flask(__name__)

@app.route('/api/employees', methods=['GET'])
def employee():
    name = request.args.get('name')
    if name is not None:
        result = get_employee_data(df_us, df_uk, name)
        if result is not None:
            return jsonify(result)
        else:
            return f"Error: something went wrong with name: {name}", 400
    elif not request.args: # if no query string
        region_info = region_stats(df_us, df_uk)
        return jsonify(region_info)
    else:
        return "Error: something went wrong", 400
    

@app.route('/api/wage_stats', methods=['GET'])
def get_wage_stats():    
    company_name = request.args.get('company_name')
    country = request.args.get('country')
    if not company_name:
        return "Company name is required", 400
    else:
        bytes_image = wage_stats(company_name, country, df_us, df_uk)
        if bytes_image is not None:
            return send_file(bytes_image, mimetype='image/png')
        else: 
            return f"Records dont exist for company: {company_name}", 400


if __name__ == '__main__':
    unittest.main(module='tests', exit=False)
    app.run(debug=True)