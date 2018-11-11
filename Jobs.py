"""
Database
"""
import sqlite3

def create_tables():
    #run again to clear all tables
    #connects to database
    conn = sqlite3.connect("jobs.db")
    #create cursor
    cursor = conn.cursor()
    #delete current tables
    cursor.execute("drop table job")
    cursor.execute("drop table employee")
    #create and execute tables
    cursor.execute("""create table employee (
                        id integer primary key autoincrement,
                        first_name varchar(20) not null,
                        last_name varchar(20) not null,
                        age int not null,
                        gender tinyint,
                        experience varchar(20))""")
    
    cursor.execute("""create table job (
                        id integer primary key autoincrement,
                        name varchar(20) not null,
                        salary float,
                        employee_id int,
                        foreign key (employee_id) references employee(id))""")
    
    #save changes
    conn.commit()
    #close connection
    cursor.close()  

def employee_info():
    first_name = raw_input("Enter first name: ")
    last_name = raw_input("Enter last name: ")
    age = raw_input("Enter age: ")
    gender = raw_input("Enter gender (0 = male, 1 = female, 2 = other): ")
    experience = raw_input("Enter highest degree: ")
    
    return """insert into employee (first_name, last_name, age, gender, experience)
                values ('{0}', '{1}', {2}, {3}, '{4}')""".format(first_name, last_name, age, gender, experience)

def job_info():
    name = raw_input("Enter job name: ")
    salary = raw_input("Enter annual salary: $")
    
    return """insert into job (name, salary)
        values ('{0}', {1})""".format(name, salary)
                
def main():
    #tables are already created
    conn = sqlite3.connect("jobs.db")
    cursor = conn.cursor()
    
    ask = raw_input("""What would you like to do?
                        1: Assign an employee
                        2: Add a new position
                        3: See information\n""")
    
    if ask == "1":
        print "Welcome! Please enter the employee information."
        cursor.execute(employee_info())
        sql = cursor.execute("select * from job where employee_id is null")
        result = sql.fetchall()
        print "The available jobs are: "
        for row in result:
            print """ID: {0}
Name: {1}
Salary: {2}""".format(row[0], row[1], row[2])
        selected_job= raw_input("Assign this employee to an available job. Enter the id: ")
        selected_job = int(float(selected_job))
        sql = """update job
                    set employee_id = (
                        select id from employee where id = (select max(id) from employee)
                        )
                    where id = {}""".format(selected_job)
        cursor.execute(sql)
        print "The job is assigned! Have a nice day!"
    elif ask == "2":
        print "Please enter the information about the new job position."
        cursor.execute(job_info())
    else:
        input = raw_input(""""Would you like to see the job or employee list?
                                Type 1 for job and 2 for employee:\n""")
        if input == "1":
            sql = cursor.execute("select * from job")
            result = sql.fetchall()
            for row in result:
                print """ID: {0}
Name: {1}
Salary: {2}
Employee ID: {3}""".format(row[0], row[1], row[2], row[3])
        else:
            sql = cursor.execute("select * from employee")
            result = sql.fetchall()
            for row in result:
                print """ID: {0}
First Name: {1}
Last Name: {2}
Age: {3}
Gender: {4}
Experience: {5}""".format(row[0], row[1], row[2], row[3], row[4], row[5])
    
    conn.commit()
    cursor.close()

#run create tables first to reset
main()