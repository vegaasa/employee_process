# employee_process
AN ETL PROCESS TO LOAD DATA EMPLOYEE &amp; CALCULATE EMPLOYEE PER HOUR

# Case
Imagine that we should have Creating ETL Process that could store our data to Database & transform them to be accessible by others team member.

![Employee Diagram drawio](https://github.com/vegaasa/employee_process/assets/45099588/0c56c4d2-2b04-413a-a8af-4a976ed84e34)

# Lets Create Many Cases that might be happend

1. Database have been created on POSTGRESQL : db_employee

# First Create table in Our database
  Create table in our database:
  a. temp_tbl_employee:
      from our ETL store our data to this temporary table then insert our data to main table since ETL will run daily and we must avoiding duplication of data
    


