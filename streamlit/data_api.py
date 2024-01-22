import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import streamlit as st

#main script to find, manipulate, and story data
def get_file_paths(directory):
    paths = []
    for i in os.path('../data'):
        paths.append(i)
    
    return paths

@st.cache_data
def get_tidy_excel_data(file_path):

    """
    read in excel weekly tabs, create two dataframes -- one qualitative data and one quantitative data
    """
    
    excel_object = pd.ExcelFile(file_path)
    sheets = excel_object.sheet_names

    sheets = [item for item in sheets if not any(char.isalpha() for char in item)]

    sheet_df_list_quant = []
    sheet_df_list_qual = []


    for sheet in sheets:
        sheet_ex_data = pd.read_excel(file_path,usecols='A:J',sheet_name = sheet)

        #find the first row of data
        for i in range(10):
            non_null_count = sheet_ex_data.iloc[i].notnull().sum()
            if non_null_count > 3:  # arbitrary threshold to find the starting row
                data_start_row = i
                break
        # Displaying the first few rows of actual data
        
        sample_data_start = sheet_ex_data.iloc[data_start_row:]
        sample_data_start.head()

        #find the first column of data
        while sample_data_start.iloc[:, 0].isna().all():
            sample_data_start = sample_data_start.drop(sample_data_start.columns[0], axis=1)
        

        # We need to transpose the DataFrame to get dates as rows and categories as columns

        # Extracting the relevant data (excluding the total column for now)
        if file_path == 'data/tulia_data.xlsx':
            date_index_val = 0
        else:
            date_index_val = 1
        data = sample_data_start.iloc[date_index_val :-1, 0:-1].T

        # Setting the first row as the header and the first column as the index
        data.columns = data.iloc[0]
        data = data[1:]

        # Resetting the index to make the date a column
        data.reset_index(drop=True, inplace=True)

        #remove Weekly Totals
        data = data[data['DATE'] != 'WEEKLY TOTALS']


        # Melting the DataFrame to get a long format
        data_melted = data.melt(id_vars=["DATE"], var_name="Category", value_name="Value")
        def clean_date(x):
            try:
                if '//' in x:
                    return x.replace('//','/')
                else:
                    return x
            except:
                return x
        data_melted['DATE'] = data_melted['DATE'].apply(np.vectorize(clean_date))
        data_melted['DATE'] = pd.to_datetime(data_melted['DATE'])
        data_melted = data_melted[~data_melted['Category'].isnull()]

        #split out qualitative and quantitative dataframes
        exp_list = []
        for i in data_melted[~data_melted['Category'].isnull()].Category.unique():
            if 'Explanation' in i:
                exp_list.append(i)
            else:
                pass
        
        #split out qualitative and quantitative dataframes
        data_melted_qual = data_melted[data_melted['Category'].isin(exp_list)]
        data_melted_quant = data_melted[~data_melted['Category'].isin(exp_list)]

        data_melted_quant.loc[data_melted_quant['Value']=='19.445.44', 'Value'] = 19445.44
        data_melted_quant['Value'] = data_melted_quant['Value'].replace({'#DIV/0!': np.nan})
        data_melted_quant.loc[data_melted_quant['Value'] == 'a lot of birthdays', 'Value'] = np.nan

        data_melted_quant['Value'] = data_melted_quant['Value'].astype(float)

        #take instances where the cateogry = '2022 Net Sales' and relable them Total Net Sales, with a year prior date value

        #if the lowercase value of the column Category == 2022 net sales then do something

        data_melted_quant.loc[data_melted_quant['Category'].str.lower() == '2022 net sales', 'DATE'] = data_melted_quant.loc[data_melted_quant['Category'].str.lower() == '2022 net sales', 'DATE'].apply(lambda x: x - timedelta(days=365))
        data_melted_quant.loc[data_melted_quant['Category'].str.lower() =='2022 net sales','Category'] = 'TOTAL NET SALES'


    #     #add data to list
        sheet_df_list_quant.append(data_melted_quant)
        sheet_df_list_qual.append(data_melted_qual)

        sheet_data_concat_quant = pd.concat(sheet_df_list_quant)
        sheet_data_concat_qual = pd.concat(sheet_df_list_qual)






        friendly_column_name_dict = {
        'LUNCH SALES': 'lunch_sales',
        'LUNCH COVERS': 'lunch_covers',
        'DINNER SALES': 'dinner_sales',
        'DINNER COVERS': 'dinner_covers',
        'BAR SALES': 'bar_sales',
        'BAR COVERS': 'bar_covers',
        'TAKEOUT SALES': 'takeout_sales',
        'TOTAL NET SALES': 'total_net_sales',
        'VARIANCE': 'variance',
        'Explanation of sales variance +/- 2%': 'explanation_of_sales_variance_plus_minus_2percent',
        'Total Covers': 'total_covers',
        'LUNCH PPA': 'lunch_ppa',
        'DINNER PPA': 'dinner_ppa',
        'COMPS (excluding employee comps)': 'comps_excluding_employee_comps',
        'Comp %': 'comp_percent',
        'Explanation of comps +/- 2%': 'explanation_of_comps_plus_minus_2percent',
        'LABOR $': 'labor_dollar',
        'LABOR %': 'labor_percent',
        'Labor $': 'labor_dollar',
        'Labor %': 'labor_percent'
        }

        # #adjust column names
        sheet_data_concat_quant['Category'] = sheet_data_concat_quant['Category'].replace(friendly_column_name_dict)
        sheet_data_concat_quant = sheet_data_concat_quant[~sheet_data_concat_quant['Category'].isnull()]
        sheet_data_concat_qual['Category'] = sheet_data_concat_qual['Category'].replace(friendly_column_name_dict)
        sheet_data_concat_qual = sheet_data_concat_qual[~sheet_data_concat_qual['Category'].isnull()]

        df_final = pd.concat([
        df.pivot(index='DATE', columns='Category', values='Value').reset_index() for df in [sheet_data_concat_qual.drop_duplicates(), sheet_data_concat_quant.drop_duplicates()]])
        # df_final = sheet_data_concat_quant.reset_index().pivot(index = 'DATE',columns = 'Category', values = 'Value').reset_index()
        #additional metrics
        df_final['labor_percent'] = df_final['labor_dollar']/df_final['total_net_sales']

        # #update the column names
        df_final = df_final.rename(columns = {'DATE': 'date',
        'Category':'category',
        'Value': 'value'
        })




    return df_final