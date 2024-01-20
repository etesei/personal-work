import pandas as pd
import numpy as np
from datetime import datetime, timedelta


#the goal of this sheet is to create functions that will read in the excel document in the data tab, and to manipulate it into a tidy, saved as a CSV

def read_excel_update(file_path):
    
    excel_object = pd.ExcelFile(file_path)
    sheets = excel_object.sheet_names
    sheets.remove('Master')

    sheet_df_list = []
 

    for sheet in sheets:
        print(sheet +' Running')
        sheet_ex_data = pd.read_excel(file_path,usecols='A:J',sheet_name = sheet)

        for i in range(10):
            non_null_count = sheet_ex_data.iloc[i].notnull().sum()
            if non_null_count > 3:  # arbitrary threshold to find the starting row
                data_start_row = i
                break

        # Displaying the first few rows of actual data
        sample_data_start = sheet_ex_data.iloc[data_start_row:]
        sample_data_start.head()

        # We need to transpose the DataFrame to get dates as rows and categories as columns

        # Extracting the relevant data (excluding the total column for now)
        data = sample_data_start.iloc[1:-1, 1:-1].T

        # Setting the first row as the header and the first column as the index
        data.columns = data.iloc[0]
        data = data[1:]

        # Resetting the index to make the date a column
        data.reset_index(drop=True, inplace=True)

        # Melting the DataFrame to get a long format
        data_melted = data.melt(id_vars=["DATE"], var_name="Category", value_name="Value")

        #take instances where the cateogry = '2022 Net Sales' and relable them Total Net Sales, with a year prior date value
        data_melted['DATE'] = pd.to_datetime(data_melted['DATE'])
        date_melted['Value'] = data_melted['Value'].astype(float)

        data_melted.loc[data_melted['Category'] == '2022 NET SALES', 'DATE'] = data_melted.loc[data_melted['Category'] == '2022 NET SALES', 'DATE'].apply(lambda x: x - timedelta(days=365))
        data_melted.loc[data_melted['Category']=='2022 NET SALES','Category'] = 'TOTAL NET SALES'

        #add data to list
        sheet_df_list.append(data_melted)

    sheet_data_concat = pd.concat(sheet_df_list)




    friendly_column_name_dict = {
    'LUNCH SALES': 'lunch_sales',
    'LUNCH COVERS': 'lunch_covers',
    'DINNER SALES': 'dinner_sales',
    'DINNER COVERS': 'dinner_covers',
    'BAR SALES': 'bar_sales',
    'BAR COVERS': 'bar_covers',
    'TAKEOUT SALES': 'takeout_sales',
    'TOTAL NET SALES': 'total_net_sales',
    '2022 NET SALES': '2022_net_sales',
    'VARIANCE': 'variance',
    'Explanation of sales variance +/- 2%': 'explanation_of_sales_variance_plus_minus_2percent',
    'Total Covers': 'total_covers',
    'LUNCH PPA': 'lunch_ppa',
    'DINNER PPA': 'dinner_ppa',
    'COMPS (excluding employee comps)': 'comps_excluding_employee_comps',
    'Comp %': 'comp_percent',
    'Explanation of comps +/- 2%': 'explanation_of_comps_plus_minus_2percent',
    'LABOR $': 'labor_dollar',
    'LABOR %': 'labor_percent'
    }

    #adjust column names
    sheet_data_concat['Category'] = sheet_data_concat['Category'].replace(friendly_column_name_dict)

    #update the column names
    sheet_data_concat = sheet_data_concat.rename(columns = {'DATE': 'date',
    'Category':'category',
    'Value': 'value'
    })


    #send the CSV out to the data tab
    sheet_data_concat.to_csv('../data/output.csv')


#write function printing 'hi world'

read_excel_update('../data/BTM SALES REPORT 11.5.2023.xlsx')


    
