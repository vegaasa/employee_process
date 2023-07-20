from sqlalchemy import create_engine
from datetime import datetime
import config
import argparse

current_date = datetime.now().strftime('%Y-%m-%d')

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
query_delete = """delete from tbl_branch_cost where id is not null;"""

query_insert = """ insert into tbl_branch_cost 
with tbl_ttl_hour_employee as 
--calulcate total hour per employee
(select extract(month from date) as month,extract(year from date) as year,employee_id,sum(checkout-checkin)  as ttl_hour 
from tbl_timesheet group by 1,2,3 order by year,month),
-- convert total hour to integer value
tbl_ttl_hour_employee_int as 
(select month,year,employee_id,date_part('hour',ttl_hour)+(date_part('minutes',ttl_hour)/60)+(date_part('minutes',ttl_hour)/3600) ttl_hour 
from tbl_ttl_hour_employee),
-- generate cte table to make window function successfully executed
final_table as 
(select year,cast(month as INTEGER) as month,branch_id,count(distinct t1.employee_id) as ttl_employee,sum(salary) ttl_salary,sum(t2.ttl_hour) ttl_working_time,sum(salary)/sum(t2.ttl_hour) salary_per_hour,
current_date as date_process from tbl_employee t1 left join tbl_ttl_hour_employee_int t2 on t1.employee_id = t2.employee_id group by 1,2,3) 
select row_number() over() as id, * from final_table;"""

def main(pass_psql):
    connection = get_connection(pass_psql)
    delete_table = connection.execute(query_delete)
    exec_query = connection.execute(query_insert)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--password", required=True, type=str)
    args = parser.parse_args()
    main(args.password)