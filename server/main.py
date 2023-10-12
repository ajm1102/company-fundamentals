
def return_metrics_pandas(ticker):
    import os 
    import pandas as pd
    import numpy as np
    from metric_parsing_functions import (parse_10Q, parse_10K, parse_10Q_sql, parse_10K_sql)
    from preprocessing_functions import (convert_ticker_cik)

    company_cik = convert_ticker_cik(ticker)

    files = os.listdir('./data_code/')
    files.reverse()

    income_statements = []
    balance_statements = []

    for file_name in files:
        path_submissions = f'./data_code/{file_name}/sub.tsv'

        df_submissions = pd.read_table(path_submissions)

        df_submissions_quarterly_reports = df_submissions[(df_submissions['form'] == '10-Q') | # reduce to quarterly statements
                                                          (df_submissions['form'] == '10-K')]

        company_submissions = df_submissions_quarterly_reports[df_submissions_quarterly_reports['cik'] == company_cik]
        # check if comapany released a statement in month/quarter
        if not company_submissions.empty and company_submissions['form'].values[0] == '10-Q':

            income_statement, balance_statement = parse_10Q_sql(company_submissions, file_name)
            income_statement = income_statement.drop('index', axis=1)
            balance_statement = balance_statement.drop('index', axis=1)
            income_statements.append(income_statement)
            balance_statements.append(balance_statement)

        if not company_submissions.empty and company_submissions['form'].values[0] == '10-K':

            income_statement, balance_statement = parse_10K_sql(company_submissions, file_name)
            income_statement = income_statement.drop('index', axis=1)
            balance_statement = balance_statement.drop('index', axis=1)
            print(income_statement.columns)
            income_statements.append(income_statement)
            balance_statements.append(balance_statement)        
    balance_statements_rough = pd.DataFrame().join(balance_statements, how="outer")
    income_statements_rough = pd.DataFrame().join(income_statements, how="outer")

    available_metrics = list(balance_statements_rough.index) + list(income_statements_rough.index)
    
    return available_metrics, balance_statements_rough, income_statements_rough

