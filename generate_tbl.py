from sqlalchemy.orm import declarative_base
from sqlalchemy import Column,Integer,String,Date,Float,Time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import config
import argparse

Base = declarative_base()

#GENERATING TBL EMPLOYEE
class tbl_employee(Base):
    __tablename__ = 'tbl_employee'
    employee_id = Column(String,primary_key=True)
    branch_id =  Column(String)
    salary = Column(Float)
    join_date = Column(Date)
    resign_date = Column(Date)
    date_process = Column(Date)

    def __init__(self,employee_id,branch_id,salary,join_date,resign_date,date_process):
        self.employee_id = employee_id
        self.branch_id = branch_id
        self.salary = salary
        self.join_date = join_date
        self.resign_date = resign_date
        self.date_process = date_process

#GENERATING TEMP TBL EMPLOYEE
class temp_tbl_employee(Base):
    __tablename__ = 'temp_tbl_employee'
    employee_id = Column(String,primary_key=True)
    branch_id =  Column(String)
    salary = Column(Float)
    join_date = Column(Date)
    resign_date = Column(Date)
    date_process = Column(Date)

    def __init__(self,employee_id,branch_id,salary,join_date,resign_date,date_process):
        self.employee_id = employee_id
        self.branch_id = branch_id
        self.salary = salary
        self.join_date = join_date
        self.resign_date = resign_date
        self.date_process = date_process

#GENERATING TBL TIMESHEET
class tbl_timesheet(Base):
    __tablename__ = 'tbl_timesheet'

    timesheet_id = Column(String,primary_key=True)
    employee_id =  Column(String)
    date = Column(Date)
    checkin = Column(Time)
    checkout = Column(Time)
    date_process = Column(Date)

    def __init__(self,timehseet_id,employee_id,date,checkin,checkout,date_process):
        self.timehseet_id = timehseet_id
        self.employee_id = employee_id
        self.date = date
        self.checkin = checkin
        self.checkout = checkout
        self.date_process = date_process

##GENERATING TEMP TBL TIMESHEET
class temp_tbl_timesheet(Base):
    __tablename__ = 'temp_tbl_timesheet'

    timesheet_id = Column(String,primary_key=True)
    employee_id =  Column(String)
    date = Column(Date)
    checkin = Column(Time)
    checkout = Column(Time)
    date_process = Column(Date)

    def __init__(self,timehseet_id,employee_id,date,checkin,checkout,date_process):
        self.timehseet_id = timehseet_id
        self.employee_id = employee_id
        self.date = date
        self.checkin = checkin
        self.checkout = checkout
        self.date_process = date_process

#GENERATING TBL BRANCH COST
class tbl_branch_cost(Base):
    __tablename__ = 'tbl_branch_cost'

    id = Column(Integer,primary_key=True)
    year =  Column(Integer)
    month = Column(Integer)
    branch_id = Column(String)
    ttl_employee = Column(Integer)
    ttl_salary = Column(Integer)
    ttl_working_time = Column(Integer)
    salary_per_hour = Column(Float)
    date_process = Column(Date)

    def __init__(self,id,year,month,branch_id,ttl_employee,ttl_salary,ttl_working_time,salary_per_hour,date_process):
        self.id = id
        self.year = year
        self.month = month
        self.branch_id = branch_id
        self.ttl_employee = ttl_employee
        self.ttl_salary = ttl_salary
        self.ttl_working_time = ttl_working_time
        self.salary_per_hour = salary_per_hour
        self.date_process = date_process

#GENERATING TBL EX EMPLOYEE
class tbl_ex_employee(Base):
    __tablename__ = 'tbl_ex_employee'
    employee_id = Column(String,primary_key=True)
    branch_id =  Column(String)
    salary = Column(Float)
    join_date = Column(Date)
    resign_date = Column(Date)
    date_process = Column(Date)

    def __init__(self,employee_id,branch_id,salary,join_date,resign_date,date_process):
        self.employee_id = employee_id
        self.branch_id = branch_id
        self.salary = salary
        self.join_date = join_date
        self.resign_date = resign_date
        self.date_process = date_process

#GENERATING TEMP TBL EX EMPLOYEE
class temp_tbl_ex_employee(Base):
    __tablename__ = 'temp_tbl_ex_employee'
    employee_id = Column(String,primary_key=True)
    branch_id =  Column(String)
    salary = Column(Float)
    join_date = Column(Date)
    resign_date = Column(Date)
    date_process = Column(Date)

    def __init__(self,employee_id,branch_id,salary,join_date,resign_date,date_process):
        self.employee_id = employee_id
        self.branch_id = branch_id
        self.salary = salary
        self.join_date = join_date
        self.resign_date = resign_date
        self.date_process = date_process


def main(psql_password):
    psql_db = config.PSQL_DB
    psql_pass = psql_password
    psql_username = config.PSQL_USER
    psql_port = config.PSQL_PORT
    psql_host = config.PSQL_HOST

    #URI Schema for database
    #schema: "postgres+psycopg2://<USERNAME>:<PASSWORD>@<IP_ADDRESS>:<PORT>/<DATABASE_NAME>"

    DB_URI = "postgresql://{}:{}@{}:{}/{}".format(psql_username,
                                                         psql_pass,
                                                         psql_host,
                                                         psql_port,
                                                         psql_db)
    #generate engine to interact with database
    engine = create_engine(DB_URI)
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    #using arg.parse to passing password database via cmd
    parser = argparse.ArgumentParser()
    parser.add_argument("--password", required=True, type=str)
    args = parser.parse_args()
    main(args.password)
