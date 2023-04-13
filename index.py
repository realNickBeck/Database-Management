import mysql.connector


hostname = 'localhost'
username = 'root'
pswd = 'rootUser77!'
database = 'practice_database'
port_id = 3306

conn= None
cur = None

#try:
conn = mysql.connector.connect(
    host = hostname,
    user = username,
    password = pswd,
    db = database,
    port = port_id
)
cur = conn.cursor()

############################################################
#                Employee Session Function Call
############################################################
def employeeSession(username):
    while 1:
        print("")
        print("Employee Menu")
        print("1. View Projects")
        print("2. Logout")

        userInput = input(str("Option : "))
        if(userInput == "1"):               #user chose option 1 View Projects
            print("")
            print("view Projects")
            dataBaseValue = (username,)
            cur.execute("Select employee_id, project_name, project_timespan from project, assignment where project.project_num = assignment.project_num and employee_id = (select employee_id from employee where username = %s)", dataBaseValue)
            print(cur.fetchall())
            conn.commit()
        elif(userInput == "2"):             #user chose option 2 logout
            break
        else:
            print("\nPlease Select a Valid Number")

############################################################
#           Admin Seesion Function Call
############################################################
def adminSession():
    while 1:
        print("")
        print("Admin Menu")
        print("1. Register New Employee")
        print("2. Modify Employee Information")
        print("3. Delete Existing Employee")
        print("4. Delete/Add Project")
        print("5. Assign/Deassign Project")
        print("6. Logout")

        userInput = input(str("Option : "))

        if userInput == "1":               #user chose option 1 Register New Employee
            print("")
            print("Register New Employee")

            firstName= input(str("Employee First Name : "))
            lastName= input(str("Employee Last Name : "))
            title= input(str("Employee Title : "))
            username= input(str("Employee Username : "))
            password= input(str("Employee Password : "))

            dataBaseValue = (firstName, lastName, title, username, password)
            value = (firstName, lastName)
            cur.execute("INSERT INTO employee (employee_fname, employee_lname, employee_title, username, password) VALUES(%s,%s,%s,%s,%s)", dataBaseValue)
            conn.commit()
            print("\n" + firstName + " " + lastName + " has been registered as a new employee!")
            cur.execute("SELECT employee_id FROM employee WHERE employee_fname = %s AND employee_lname = %s", value)
            print(cur.fetchall())
            
        elif userInput == "2":               #user chose option 2 modify employee
            print("")
            print("Modify Current Employee")
            id = int(input(str("Enter Employee ID : ")))

            print("")
            print("What Would you like to edit for employee ID : " + str(id))
            print("1. Employee Title")
            print("2. Password")
            user_input = input(str("Option : "))

            if(user_input == "1"):
                dataBaseValue = (id,)
                cur.execute("SELECT employee_title FROM employee WHERE employee_id = %s", dataBaseValue)
                print(cur.fetchall())

                print("")
                newTitle = input(str("Enter New Title : "))
                anotherDataBaseValue = (newTitle, id)
                cur.execute("UPDATE employee \
                            SET employee_title = %s \
                            WHERE employee_id = %s", anotherDataBaseValue)
                conn.commit()

                cur.execute("SELECT employee_title FROM employee WHERE employee_id = %s", dataBaseValue)
                print("")
                print(cur.fetchall())
                print("Password Changed Sucessfully")

            elif(user_input == "2"):
                dataBaseValue = (id,)
                cur.execute("SELECT password FROM employee WHERE employee_id = %s", dataBaseValue)
                print(cur.fetchall())

                print("")
                newPassword = input(str("Enter New Password : "))
                anotherDataBaseValue = (newPassword, id)
                cur.execute("UPDATE employee \
                            SET password = %s \
                            WHERE employee_id = %s", anotherDataBaseValue)
                conn.commit()

                cur.execute("SELECT password FROM employee WHERE employee_id = %s", dataBaseValue)
                print("")
                print(cur.fetchall())
                print("Title Changed Sucessfully")

            else:
                print("\nPlease Select a Valid Number")
        
        elif userInput == "3":               #user chose option 3 Delete Existing Employee
            print("")
            print("Delete Current Employee")
            id = int(input(str("Enter Employee ID : ")))
            dataBaseValue = (id,)
            cur.execute("DELETE FROM employee WHERE employee_id = %s", dataBaseValue)
            conn.commit()
            if(cur.rowcount < 1):
                print("\nEmployee not found")
            else:
                print("\nEmployee with ID : " + str(id) + " has been succesfully deleted")

        elif userInput == "4":               #user chose option 4 Delete/Add Project
            print("")
            cur.execute("SELECT project_name FROM project")
            print(cur.fetchall())

            print("")
            print("Delete/Add Project")
            print("1. Add Project")
            print("2. Delete Project")

            userInput = input(str("Option : "))
            if userInput == "1":  #user chose option add
                projectName = input(str("\nEnter Project Name : "))
                projectTimeSpan = input(str("Enter Project Time Span : "))

                dataBaseValue = (projectName, projectTimeSpan)
                cur.execute("INSERT INTO project (project_name, project_timespan) VALUES(%s,%s)", dataBaseValue)
                conn.commit()
                print("\n" + projectName + " has been added")

            elif userInput == "2":   #user chose option delete
                projectName = input(str("Enter Project Name : "))
                dataBaseValue = (projectName,)

                cur.execute("DELETE FROM project WHERE project_name = %s", dataBaseValue)
                conn.commit()
                if(cur.rowcount < 1):
                    print("\nProject not found")
                else:
                    print("\nProject : " + projectName + ", has been succesfully deleted")
            else:
                print("\nPlease Select a Valid Number")

        elif userInput == "5":               #user chose option 5 assign/deassign project
            print("")
            cur.execute("SELECT * FROM assignment")
            print(cur.fetchall())

            print("")
            print("Assign/Deassign Project")
            print("1. Assign Project")
            print("2. Deassign Project")

            userInput = input(str("\nOption : "))

            if userInput == "1":     
                projectNumber = input(str("Enter Project Number : "))
                employeeID = int(input(str("Enter Employee ID : ")))
                dataBaseValue = (employeeID, projectNumber)
                anotherDataBaseValue = (employeeID,)

                cur.execute("INSERT INTO assignment (employee_id, project_num) VALUES(%s,%s)", dataBaseValue)
                conn.commit()
                print("\nProject has been assigned to employee with ID : " + str(employeeID))
                cur.execute("Select employee_id, project_name, project_timespan from project, assignment where project.project_num = assignment.project_num and employee_id = (select employee_id from employee where employee_id = %s)", anotherDataBaseValue)
                print(cur.fetchall())

            elif userInput == "2":   
                projectNumber = input(str("Enter Project Number : "))
                employeeID = int(input(str("Enter Employee ID : ")))
                dataBaseValue = (employeeID, projectNumber)

                cur.execute("DELETE FROM assignment WHERE employee_id = %s AND project_num = %s", dataBaseValue)
                conn.commit()
                if(cur.rowcount < 1):
                    print("\nAssignment not found")
                else:
                    print("\nProject Number : " + projectNumber + ", assigned to employee with ID : " + str(employeeID) + " has been succesfully deleted")

            else:
                print("\nPlease Select a Valid Number")

        elif userInput == "6":               #user chose option 6 logout
            break
        else:                              #user put invalid option
            print("\nPlease Select a Valid Number")

############################################################
#           Authenticate Employee Function Call
############################################################
def authenticateEmployee():
    print("")
    print("Employee Login")
    
    username = input(str("Username : "))
    password = input(str("Password : "))
    
    dataBaseValue = (username,)
    cur.execute("SELECT username FROM employee WHERE username = %s", dataBaseValue)
    newArray = [dataBaseValue]
    var=cur.fetchall()

    dbValue = (password, username )
    value= (password,)
    cur.execute("SELECT password FROM employee WHERE password = %s AND username =%s", dbValue)
    variable = cur.fetchall()
    newerArray = [value]

    if(newArray == var):
        if(newerArray == variable):
            print("\nLogin Succesfull")
            employeeSession(username)
        else:

            print("\nIncorrect Password")
    else:
        print("\nLogin Not Found")

############################################################
#           Authenticate Admin Function Calls
############################################################
def authenticateAdmin():
    print("")
    print("Admin Login")
    print("")
    username = input(str("Username : "))
    password = input(str("Password : "))
    if(username == "admin"):
        if(password == "password123"):
            print("\nLogin Succesfull")
            adminSession()
        else:
            print("\nIncorrect Password")
    else:
        print("\nLogin Not Found")

############################################################
#                    main program
############################################################
def main():
    while 1:
        print("\nWelcome to The Portal" )
        print("")
        print("1. Login as employee")
        print("2. Login as admin")

        user_input = input(str("Option : ")) #get user input

        if user_input == "1":               #user chose option 1
            authenticateEmployee()
        elif user_input == "2":             #user chose option 2
            authenticateAdmin()
        else:                               #user put invalid option
            print("\nPlease Select a Valid Number")

#except Exception as error:
#    print(error)
#finally:
#    if cur is not None:
#      cur.close()
#   if conn is not None:
#      conn.close()

main()