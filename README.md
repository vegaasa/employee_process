# employee_process
AN ETL PROCESS TO LOAD DATA EMPLOYEE &amp; CALCULATE EMPLOYEE PER HOUR

# Case
Imagine that we should have Creating ETL Process that could store our data to Database & transform them to be accessible by others team member.

This is Our Data Modelling:

![Employee Diagram drawio](https://github.com/vegaasa/employee_process/assets/45099588/0c56c4d2-2b04-413a-a8af-4a976ed84e34)

# Lets Create Many Cases that might be happend

1. Database have been created on POSTGRESQL : db_employee
![image](https://github.com/vegaasa/employee_process/assets/45099588/ae0948ce-bb4b-4649-b242-4ca1b29de461)

# First Create table in Our database
  Create table in our database:
  a. temp_tbl_employee:
      contain: daily employee data
      from our ETL store our data to this temporary table then insert our data to main table since ETL will run daily and we must avoiding duplication of data
  b.tbl_employee:
      contain: full employee data
      from table temp_tbl_employee insert our employee data to this final table
  c. temp_tbl_timesheet:
      contain: daily timesheet data
      creating temp table to avoid duplicate data process
  d. tbl_timesheet:
      contain: full timesheet data
      from table temp_tbl_timesheet insert our timesheet data to this final table
  e. temp_tbl_ex_employee:
      contain: daily ex-employee data
      this table is full of employee that have been resigned. insert to this table to avoid duplicated data
  f. tbl_ex_employee:
      contain: full ex-employee data
      thsi is main table for ex employee data.
  g. tbl_branch_cost:
      contain : calulation Cost salary  for hour by branch id
      to save data salary per hour after calculation from tbl_timesheet & tbl_employee.

      

  # File
  1. config.py
  2. generate_tbl.py
  3. ingest_employee.py
  4. ingest_timesheet.py
  5. salary_per_hour_process.py

  config.py:
  this python file contain configuration of database & file it self. and will be added to config many configuration of this project.

  generate_tbl.py:
  this python file contain to generate all needed table to our postgres database.
  Run this only by fist time when we wanna start the project

  ingest_employee.py:
  this python file contain our ingestion to postgres database.
  cleansing employee file by:
  1. drop duplicate employee that cover multiple branch, so 1 employee only cover 1 branch --> let's assume this is not possible to handle multiple branch
  2. drop employee that have been resign & store resigned employee to other table.

  ingest_timesheet.py
  this python file contain ingestion to postgres database
  cleansing timesheet by:
  1. deleting data employee that have been resigned
  2. delete check out time < check in time -> let's assume this is system failur.

  salary_per_hour.py
  this is python file to runnig calcultaion of salary perhour

all of data above is possible to run daily as per Business Case Needs.

we could store our .py file to windows scheduler.

or i do recomend using orchestrator tools like Airflow.
so it will run & executed by airflow shceduler and DAG Task.


