
def return_metrics(ticker):
    import os 
    import pandas as pd
    import numpy as np
    from metric_parsing_functions import (parse_10Q, parse_10K, parse_10Q_sql, parse_10K_sql)
    from preprocessing_functions import (convert_ticker_cik)
    import sqlite3

    conn = sqlite3.connect('mydb.db')

    # each comapany is identified with unique string called a cik
    # can convert the cik with a ticker
    company_cik = convert_ticker_cik(ticker)

    
    files = os.listdir('./data_code/')
    files.reverse()

    income_statements = []
    balance_statements = []

    depth = 999999999999999999999999
    # metric count
    metric_count_path = f'./data_code/2024_02_notes/metric_count_values_2024_02_notes.parquet'
    metric_count_table = pd.read_parquet(metric_count_path)[0:depth]

    # goes through each quarter then month files
    for file_name in files:
        # load table that stores identifier to reports
        path_submissions = f'./data_code/{file_name}/sub.tsv'

        # Specify columns to read
        usecols2 = ['adsh', 'cik', 'name', "form", "period"]
        # Specify data types for columns
        dtype_mapping2 = {'adsh': str, 'cik': int, 'name': str, "form": str, "period": str}
        #
        df_submissions = pd.read_table(path_submissions, dtype=dtype_mapping2, usecols=usecols2)
        
        
        # reduce to quarterly statements
        df_submissions_quarterly_reports = df_submissions[(df_submissions['form'] == '10-Q') | 
                                                          (df_submissions['form'] == '10-K')]
        # extract for the given company
        company_submissions = df_submissions_quarterly_reports[df_submissions_quarterly_reports['cik'] == company_cik]

        # check if comapany released a 10-Q statement in month/quarter
        if not company_submissions.empty and company_submissions['form'].values[0] == '10-Q':

            # using sql query the database for each submissions convert adsh to metrics
            
            income_statement, balance_statement = parse_10Q_sql(company_submissions, file_name, metric_count_table, conn)
            
            income_statement = income_statement.drop(['index'], axis=1, errors='ignore')
            balance_statement = balance_statement.drop(['index'], axis=1, errors='ignore')
            
            # add income to list for this time period
            income_statements.append(income_statement)
            balance_statements.append(balance_statement)
            
        # check if comapany released a 10-K statement in month/quarter
        if not company_submissions.empty and company_submissions['form'].values[0] == '10-K':
            # using sql query the database for each submissions convert adsh to metrics
            income_statement, balance_statement = parse_10K_sql(company_submissions, file_name, metric_count_table, conn)

            income_statement = income_statement.drop(['index'], axis=1, errors='ignore')
            balance_statement = balance_statement.drop(['index'], axis=1, errors='ignore')

            # add income to list for this time period
            income_statements.append(income_statement)
            balance_statements.append(balance_statement)       
    
    
    # join the lists of dataframes  
    balance_statements_rough = pd.DataFrame().join(balance_statements, how="outer")
    income_statements_rough = pd.DataFrame().join(income_statements, how="outer")
    
    # list all xbrl metrics such as assets for this stock
    available_metrics = list(balance_statements_rough.index) + list(income_statements_rough.index)
    conn.close()
    return available_metrics, balance_statements_rough, income_statements_rough

