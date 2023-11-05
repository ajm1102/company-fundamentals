
def return_metrics(ticker):
    import os 
    import pandas as pd
    import numpy as np
    from metric_parsing_functions import (parse_10Q, parse_10K, parse_10Q_sql, parse_10K_sql)
    from preprocessing_functions import (convert_ticker_cik)

    # each comapany is identified with unique string called a cik
    # can convert the cik with a ticker
    company_cik = convert_ticker_cik(ticker)

    
    files = os.listdir('./data_code/')
    files.reverse()

    income_statements = []
    balance_statements = []

    # goes through each quarter then month files
    for file_name in files:
        # load table that stores identifier to reports
        path_submissions = f'./data_code/{file_name}/sub.tsv'
        df_submissions = pd.read_table(path_submissions)
        
        # reduce to quarterly statements
        df_submissions_quarterly_reports = df_submissions[(df_submissions['form'] == '10-Q') | 
                                                          (df_submissions['form'] == '10-K')]
        # extract for the given company
        company_submissions = df_submissions_quarterly_reports[df_submissions_quarterly_reports['cik'] == company_cik]
        
        # check if comapany released a 10-Q statement in month/quarter
        if not company_submissions.empty and company_submissions['form'].values[0] == '10-Q':

            # using sql query the database for each submissions convert adsh to metrics
            income_statement, balance_statement = parse_10Q_sql(company_submissions, file_name)
            
            # add income to list for this time period
            income_statements.append(income_statement)
            balance_statements.append(balance_statement)

        # check if comapany released a 10-K statement in month/quarter
        if not company_submissions.empty and company_submissions['form'].values[0] == '10-K':
            # using sql query the database for each submissions convert adsh to metrics
            income_statement, balance_statement = parse_10K_sql(company_submissions, file_name)
            
            # add income to list for this time period
            income_statements.append(income_statement)
            balance_statements.append(balance_statement)       

    # join the lists of dataframes  
    balance_statements_rough = pd.DataFrame().join(balance_statements, how="outer")
    income_statements_rough = pd.DataFrame().join(income_statements, how="outer")

    # list all xbrl metrics such as assets for this stock
    available_metrics = list(balance_statements_rough.index) + list(income_statements_rough.index)
    
    return available_metrics, balance_statements_rough, income_statements_rough

