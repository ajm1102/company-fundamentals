import pandas as pd
import os 
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
from datetime import date
import time
"""


"""

def download_update_clean_files(socketio):

    error_filenames = download_update(socketio)
    cleaner(socketio, error_filenames)

    return

def download_update():
    
    # dates for each release quarterly
    files = os.listdir('./data_code/')

    error_filenames = []

    filing_periods = [(d.year, d.quarter) for d in pd.date_range('2010-1-31', '2020-12-31', freq='Q')]
    for yr, qr in filing_periods:
        sec_url = 'https://www.sec.gov/files/dera/data/financial-statement-and-notes-data-sets/'
        sec_url = f'{sec_url}/{yr}q{qr}_notes.zip' # create download url 
        
        file_name = f'{yr}q{qr}_notes' # create file to store downloaded data

        if file_name in files:
            time.sleep(emit_wait_time)
            continue
            
        # download zip file and extract it 
        with urlopen(sec_url) as zipresp:
            with ZipFile(BytesIO(zipresp.read())) as zfile:
                zfile.extractall(rf'./data_code/{file_name}')
                
    current_date =  str(date.today())

    # dates for each release monthly
    filing_periods = [(d.year, d.month) for d in pd.date_range('2021-1-31', current_date, freq='M')]

    for yr, month in filing_periods:
        sec_url = 'https://www.sec.gov/files/dera/data/financial-statement-and-notes-data-sets/'
        month = str(month).zfill(2)  # pad month with zeros
        sec_url = f'{sec_url}/{yr}_{month}_notes.zip' # create download url 
        
        file_name = f'{yr}_{month}_notes'

        if file_name in files:
            continue    

        # download zip file and extract it 
        try:
            with urlopen(sec_url) as zipresp:
                with ZipFile(BytesIO(zipresp.read())) as zfile:
                    zfile.extractall(rf'./data_code/{file_name}')
        except:
            error_filenames.append(file_name)
    return error_filenames

def cleaner(error_filenames):
    from sqlalchemy import create_engine

    engine = create_engine('sqlite:///mydb.db', echo=False)
    
    # read in files and change to descending order, earliest date first
    files = os.listdir('./data_code/')
    files.reverse()

    # read only important columns and specify datatype so pandas doesn't to infer
    columns_to_use = ['adsh', 'tag', 'qtrs', 'dimh', 'value', 'ddate', 'iprx']
    dtype = {'adsh': 'category',
    'tag': 'category', 
    'qtrs': 'Int32', 
    'dimh': 'category', 
    'value': 'float64', 
    'ddate': 'Int32', 
    'iprx': 'Int32'}
    # open each num tsv fiie, the file stores each xbrl value for the sec document
    for file_name in files:
        # send update on editing to websocket
        socketio.emit('message_from_server', {"data": f"Editing {file_name}"})

        # check if files has already been create and skip if so
        data_files = os.listdir(f"./data_code/{file_name}")
        if "reduced_num.parquet" in data_files or file_name in error_filenames:
            continue

        # num tables
        path_values = f'./data_code/{file_name}/num.tsv'    
        df_num = pd.read_table(path_values, usecols=columns_to_use, dtype=dtype)
        
        # remove any sub varibles dimh, and duplicate values iprx
        reduced_df_num = df_num[(df_num['dimh'] == '0x00000000') & (df_num['iprx'] == 0)]
        
        # convert csv to quicker parquet file
        reduced_df_num.to_parquet(f'./data_code/{file_name}/reduced_num.parquet', compression="snappy")
        
        # add tables to sql server with 
        reduced_df_num.to_sql(file_name, engine)

    return

