import pandas as pd
import config
import argparse
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy import types 

current_date = datetime.now().strftime('%Y-%m-%d')
file = config.fl_name_timehseet

def get_connection(psql_pass):
    psql_db = config.PSQL_DB
    psql_username = config.PSQL_USER
    psql_port = config.PSQL_PORT
    psql_host = config.PSQL_HOST
    DB_URI = "postgresql://{}:{}@{}:{}/{}".format(psql_username,
                                                         psql_pass,
                                                         psql_host,
                                                         psql_port,
                                                         psql_db)
    engine = create_engine(DB_URI)
    connections = engine.connect()

    return connections

def get_resign_employee(connection):
    """Get list of resigned employee & Return list of employee_id have been resign"""
    query = """select distinct employee_id from tbl_ex_employee;"""
    list_employee = connection.execute(query).fetchall()
    merged_list_employee = list()
    for employee in list_employee:
        merged_list_employee.extend(list(employee))

    return merged_list_employee

def read_file(file):
    "This Function created to read & re-naming column name & parsing any date column"
    df = pd.read_csv(file)
    df[['timesheet_id','employee_id']] = df[['timesheet_id','employee_id']].astype(str)

    return df

def transform(file,connection):
    df_timesheets = read_file(file)

    #List Resigned employee
    list_id_resign_employee = get_resign_employee(connection)

    #Drop timesheet resign employee
    df_timesheets = df_timesheets[~df_timesheets['employee_id'].isin(list_id_resign_employee)]
    #Consider check out time > checikin time
    df_timesheets = df_timesheets[df_timesheets['checkin']<df_timesheets['checkout']]

    df_timesheets['date_process'] = pd.to_datetime(current_date)

    return df_timesheets

def load(file,connection):
    #Read & Transform data
    df_timesheets = transform(file,connection)

    #Load data
    tbl_timesheets = 'temp_tbl_timesheet'
    index = False
    if_exists = 'replace'
    sql_types =  {'timesheet_id' : types.String(0),
                  'employee_id'  :types.String(0),
                  'date'         :types.Date(),
                  'checkin'      :types.Time(0),
                  'checkout'     :types.Time(0),
                  'date_process' :types.DATE()
                  }
    df_timesheets.to_sql(name=tbl_timesheets,
                         index=index,
                         if_exists=if_exists,
                         dtype=sql_types,
                         con=connection)


def insert_to_main_tbl(connection):
    temp_timesheet_tbl = 'temp_tbl_timesheet'
    main_timehseet_tbl = 'tbl_timesheet'

    query = """
            insert into {main_tbl} select t1.* from {temp_tbl} t1 left join {main_tbl} t2 
            on t1.timesheet_id = t2.timesheet_id where t2.timesheet_id is null;
                """.format(main_tbl=main_timehseet_tbl,
                           temp_tbl = temp_timesheet_tbl)
    #print(query)
    exec_query = connection.execute(query)

def main(psql_pass):
    connection = get_connection(psql_pass)

    #Load
    loads = load(file,connection)
    insert_main_table = insert_to_main_tbl(connection)

if __name__ == '__main__':
    #Passing SQL Password using argumen
    parser = argparse.ArgumentParser()
    parser.add_argument("--password", required=True, type=str)
    args = parser.parse_args()
    main(args.password)

