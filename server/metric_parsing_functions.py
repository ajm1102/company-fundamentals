import pandas as pd
import sqlite3

# get 10Q dataframes 
def parse_10Q_sql(company_submissions, file_name, metric_count_table):

    cur_date = int(company_submissions['period'].values[0])

    # connect to database
    conn = sqlite3.connect('mydb.db')
    cur = conn.cursor()
    
    # adsh values map to metric values
    adsh_values = tuple(company_submissions['adsh'].tolist())

    # use query to extract relevant
    metric_values_df = cur.execute(f"SELECT * FROM '{file_name}' WHERE adsh=?", adsh_values)
    column_names = [description[0] for description in metric_values_df.description]
    
    # convert to dataframe and add column names
    metric_values_df = metric_values_df.fetchall()
    metric_values_df = pd.DataFrame(metric_values_df)
    metric_values_df.columns = column_names
    metric_values_df = metric_values_df[metric_values_df['tag'].isin(list(metric_count_table.index))]
    
    income_df = income_extraction_10Q(metric_values_df, cur_date)
    balance_df = balance_extraction_10Q(metric_values_df, cur_date)

    return income_df, balance_df


def parse_10K_sql(company_submissions, file_name, metric_count_table):

    cur_date = int(company_submissions['period'].values[0])

    # connect to database
    conn = sqlite3.connect('mydb.db')
    cur = conn.cursor()

    # adsh values map to metric values
    adsh_values = tuple(company_submissions['adsh'].tolist())

    # use query to extract relevant
    metric_values_df = cur.execute(f"SELECT * FROM '{file_name}' WHERE adsh=?", adsh_values)
    column_names = [description[0] for description in metric_values_df.description]
    
    # convert to dataframe and add column names
    metric_values_df = metric_values_df.fetchall()
    metric_values_df = pd.DataFrame(metric_values_df)
    metric_values_df.columns = column_names
    metric_values_df = metric_values_df[metric_values_df['tag'].isin(list(metric_count_table.index))]

    income_df = income_extraction_10K(metric_values_df, cur_date)
    balance_df = balance_extraction_10K(metric_values_df, cur_date)

    income_df = income_df.drop('index', axis=1)
    balance_df = balance_df.drop('index', axis=1)

    return income_df, balance_df

def income_extraction_10Q(val, cur_date):
    # extract metrics loosely similar to the income statement
    income_dataframe = val[(val['qtrs'] == 1) & (val['ddate'] == cur_date) & (val['iprx'] == 0)]

    # drop all but on column with left with index being the metric on one value column
    income_dataframe = income_dataframe.set_index(income_dataframe['tag']).drop(columns=['tag','dimh','qtrs', 'iprx', 'adsh', 'ddate'])
    income_dataframe = income_dataframe.rename(columns={'value': cur_date}) # rename the value column to the date 
    return income_dataframe

def balance_extraction_10Q(val, cur_date):
    # extract metrics loosely similar to the income statement
    balance_dataframe = val[(val['qtrs'] == 0) & (val['ddate'] == cur_date) & 
               (val['iprx'] == 0)]
    
    # drop all but on column with left with index being the metric on one value column
    balance_dataframe = balance_dataframe.set_index(balance_dataframe['tag']).drop(columns=['tag','dimh','qtrs', 'iprx', 'adsh', 'ddate'])
    balance_dataframe = balance_dataframe.rename(columns={'value': cur_date})
    return balance_dataframe

def income_extraction_10K(val, cur_date):
    # extract metrics loosely similar to the income statement
    income_dataframe = val[(val['qtrs'] == 4) & (val['ddate'] == cur_date) & 
        (val['iprx'] == 0)]

    # drop all but on column with left with index being the metric on one value column
    income_dataframe = income_dataframe.set_index(income_dataframe['tag']).drop(columns=['tag','dimh','qtrs', 'iprx', 'adsh', 'ddate'])
    income_dataframe = income_dataframe.rename(columns={'value': cur_date}) # rename the value column to the date 
    return income_dataframe

def balance_extraction_10K(val, cur_date):
    # extract metrics loosely similar to the balance statement
    balance_dataframe = val[(val['qtrs'] == 0) & (val['ddate'] == cur_date) & 
              (val['iprx'] == 0)]
    
    # drop all but on column with left with index being the metric on one value column
    balance_dataframe = balance_dataframe.set_index(balance_dataframe['tag']).drop(columns=['tag','dimh','qtrs', 'iprx', 'adsh', 'ddate'])
    balance_dataframe = balance_dataframe.rename(columns={'value': cur_date}) # rename the value column to the date 
    return balance_dataframe

# pandas old alternative to sql
def parse_10Q(company_submissions, file_name):
    # release period 
    cur_date = int(company_submissions['period'].values[0])
    # read table that contains filings released by companies and metrics
    df_statement_values = pd.read_parquet(f'./data_code/datasets/{file_name}/reduced_num.parquet')
    # extact metr
    val = df_statement_values[df_statement_values['adsh'].isin(company_submissions['adsh'])]


    income_df = income_extraction_10Q(val, cur_date)
    balance_df = balance_extraction_10Q(val, cur_date)

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