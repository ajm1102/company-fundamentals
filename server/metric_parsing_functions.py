import pandas as pd
import sqlite3

def parse_10Q(company_submissions, file_name):

    cur_date = int(company_submissions['period'].values[0])

    path_values = f'./data_code/datasets/{file_name}/num.tsv'
    df_statement_values = pd.read_parquet(f'./data_code/datasets/{file_name}/reduced_num.parquet')

    val = df_statement_values[df_statement_values['adsh'].isin(company_submissions['adsh'])]

    income_df = income_extraction_10Q(val, cur_date)
    balance_df = balance_extraction_10Q(val, cur_date)

    return income_df, balance_df

def parse_10Q_sql(company_submissions, file_name):
    cur_date = int(company_submissions['period'].values[0])
    conn = sqlite3.connect('mydb.db')
    cur = conn.cursor()
    adsh_values = tuple(company_submissions['adsh'].tolist())
    x = cur.execute(f"SELECT * FROM '{file_name}' WHERE adsh=?", adsh_values)
    column_names = [description[0] for description in x.description]
    
    
    x = x.fetchall()
    x = pd.DataFrame(x)
    x.columns = column_names
    income_df = income_extraction_10Q(x, cur_date)
    balance_df = balance_extraction_10Q(x, cur_date)
    return income_df, balance_df

def parse_10K(company_submissions, file_name):
    cur_date = int(company_submissions['period'].values[0])

    df_statement_values = pd.read_parquet(f'./data_code/datasets/{file_name}/reduced_num.parquet')

    val = df_statement_values[df_statement_values['adsh'].isin(company_submissions['adsh'])]

    income_df = income_extraction_10K(val, cur_date)
    balance_df = balance_extraction_10K(val, cur_date)

    income_df = income_df.drop('index', axis=1)
    balance_df = balance_df.drop('index', axis=1)

    return income_df, balance_df

def parse_10K_sql(company_submissions, file_name):
    cur_date = int(company_submissions['period'].values[0])
    conn = sqlite3.connect('mydb.db')
    cur = conn.cursor()
    adsh_values = tuple(company_submissions['adsh'].tolist())
    x = cur.execute(f"SELECT * FROM '{file_name}' WHERE adsh=?", adsh_values)
    column_names = [description[0] for description in x.description]
    
    
    x = x.fetchall()
    x = pd.DataFrame(x)
    x.columns = column_names
    income_df = income_extraction_10K(x, cur_date)
    balance_df = balance_extraction_10K(x, cur_date)

    income_df = income_df.drop('index', axis=1)
    balance_df = balance_df.drop('index', axis=1)

    return income_df, balance_df

def income_extraction_10Q(val, cur_date):
    all_income = val[(val['qtrs'] == 1) & (val['ddate'] == cur_date) & 
           (val['iprx'] == 0)]


    tag_index = all_income.set_index(all_income['tag']).drop(columns=['tag','dimh','qtrs', 'iprx', 'adsh', 'ddate'])

    tag_index = tag_index.rename(columns={'value': cur_date})
    return tag_index

def balance_extraction_10Q(val, cur_date):
    balance_values = val[(val['qtrs'] == 0) & (val['ddate'] == cur_date) & 
               (val['iprx'] == 0)]
    
    tag_index = balance_values.set_index(balance_values['tag']).drop(columns=['tag','dimh','qtrs', 'iprx', 'adsh', 'ddate'])

    tag_index = tag_index.rename(columns={'value': cur_date})
    
    return tag_index

def income_extraction_10K(val, cur_date):
    all_income = val[(val['qtrs'] == 4) & (val['ddate'] == cur_date) & 
        (val['iprx'] == 0)]


    tag_index = all_income.set_index(all_income['tag']).drop(columns=['tag','dimh','qtrs', 'iprx', 'adsh', 'ddate'])

    tag_index = tag_index.rename(columns={'value': cur_date})
    return tag_index

def balance_extraction_10K(val, cur_date):
    balance_values = val[(val['qtrs'] == 0) & (val['ddate'] == cur_date) & 
              (val['iprx'] == 0)]
    
    
    tag_index = balance_values.set_index(balance_values['tag']).drop(columns=['tag','dimh','qtrs', 'iprx', 'adsh', 'ddate'])

    tag_index = tag_index.rename(columns={'value': cur_date})
    
    return tag_index




