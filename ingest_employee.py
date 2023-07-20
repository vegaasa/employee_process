import pandas as pd
import config
import argparse
from datetime import datetime
from sqlalchemy import create_engine

current_date = datetime.now().strftime('%Y-%m-%d')
file = config.fl_name_employee

temp_tbl_employee = "temp_tbl_employee"
tbl_employee = "tbl_employee"
temp_tbl_ex_emplyee = "temp_tbl_ex_employee"
tbl_ex_emplyee = "tbl_ex_employee"

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
    
def read_file(file):
    "This Function created to read & re-naming column name & parsing any date column"
    parse_date = ['join_date','resign_date']
    columns = ['employee_id','branch_id','salary',
              'join_date','resign_date']
    df = pd.read_csv(file,names=columns,header=0,parse_dates=parse_date)
    df[['employee_id','branch_id']] = df[['employee_id','branch_id']].astype(str)
    return df

def transform(file):
    """This function is doing:
        1.add column today as date process
        2. Droping duplicate employee and take the highest salary if duplicated
        3. generate tblemployee have been resign
        4. drop employee heve been resign
    This function returns 2 dataset:
      1. clean employee
      2. Resigned Dataset """
    
    df_employee = read_file(file)
    df_employee['date_process'] = pd.to_datetime(current_date)
    
    df_employee = df_employee.sort_values(['employee_id','salary'],ascending=False).drop_duplicates('employee_id',keep='first')
    df_employee_resign = df_employee[~df_employee['resign_date'].isnull()]
    df_employee = df_employee[df_employee['resign_date'].isnull()]
    
    return(df_employee,df_employee_resign)

def load(connection,file):
    index=False
    if_exists = 'replace'
    """This function is load dataset to Database postgresql.
    dataset loaded to temp table due to avoiding duplication, then load to main table."""
    df_employee,df_ex_employee = transform(file)

    #Load employee data to database
    df_employee.to_sql(name=temp_tbl_employee,
                       if_exists=if_exists,
                       con=connection,
                       index=index)
    
    df_ex_employee.to_sql(name=temp_tbl_ex_emplyee,
                       if_exists=if_exists,
                       con=connection,
                       index=index)

def main(psql_pass):
    #Get Connnection to database
    connection = get_connection(psql_pass)

    load_data = load(connection,file)

    qry_insert_tbl = """insert into {main_tbl} select t1.* from {temp_tbl} t1 left join {main_tbl} t2 
                          on t1.employee_id = t2.employee_id where t2.employee_id is null;"""
    
    insert_tbl_employee = connection.execute(qry_insert_tbl.format(main_tbl = tbl_employee,temp_tbl = temp_tbl_employee))
    insert_tbl_ex_employee = connection.execute(qry_insert_tbl.format(main_tbl = tbl_ex_emplyee,temp_tbl = temp_tbl_ex_emplyee))

if __name__ == '__main__':
    #Passing SQL Password using argumen
    parser = argparse.ArgumentParser()
    parser.add_argument("--password", required=True, type=str)
    args = parser.parse_args()
    main(args.password)




