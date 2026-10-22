import mysql.connector as mysql
import csv
from datetime import date

# this function is used to connect python with mysql
def connect():           # function 1 
    return mysql.connect(
        host="localhost",
        user="root",
        password="1234",
        database="hostel_management"  
        )
def setup_table():       # function 2
    conn=connect()
    cursor=conn.cursor()    #Cursor = work as a agent in between Python and Mysql!

    cursor.execute("""CREATE TABLE IF NOT EXISTS users(
    id INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(35),
    Role VARCHAR(15),
    Password VARCHAR(20)
    )
    """)
    cursor.execute("""CREATE TABLE IF NOT EXISTS complaints(
    id INT AUTO_INCREMENT PRIMARY KEY,
    Student_id INT,
    Room_NO VARCHAR(10),
    Issue TEXT,
    Status VARCHAR(20),
    Date DATE,
    FOREIGN KEY (Student_id) REFERENCES users(id)
    )
    """)

    conn.commit()
    cursor.close()
    conn.close()

def registration(name,role,password):  # function 3
    conn=connect()
    cursor=conn.cursor()

    cursor.execute("""INSERT INTO users(Name,Role,Password) VALUES(%s,%s,%s)""",(name,role,password))

    conn.commit()
    cursor.close()
    conn.close()

def login(name,password):     # function 4
    conn=connect()
    cursor=conn.cursor()

    cursor.execute("""SELECT * FROM users WHERE Name=%s AND Password=%s""",(name,password))
    result=cursor.fetchone()
    cursor.close()
    conn.close()
    return result

def submit_complaint(student_id,room_no,issue,date):   # function 5
    conn=connect()
    cursor=conn.cursor()

    cursor.execute("""INSERT INTO complaints(Student_id,Room_NO,Issue,Status,Date) VALUES(%s,%s,%s,'PENDING',%s)""",(student_id,room_no,issue,date))

    conn.commit()
    cursor.close()
    conn.close()


def View_my_complaint(Student_id):     # function 6
    conn=connect()
    cursor=conn.cursor()

    cursor.execute("""SELECT * FROM complaints WHERE Student_id=%s""",(Student_id,))
    result=cursor.fetchall()

    cursor.close()
    conn.close()
    return result

def View_all_complaints():     # function 7
    conn=connect()
    cursor=conn.cursor()

    cursor.execute("""
    SELECT complaints.id,complaints.student_id,users.name,complaints.room_no,complaints.issue,complaints.status,complaints.date
    FROM complaints
    JOIN users on complaints.Student_id=users.id
    """)
    result=cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def update__on_problem(complaint_id,new_status):    # function 8
    conn=connect()
    cursor=conn.cursor()

    cursor.execute("""UPDATE complaints SET Status=%s WHERE id=%s""",(new_status,complaint_id))

    conn.commit()
    cursor.close()
    conn.close()


def export_csv(date_filter=None):        # function 9
    conn = connect()
    cursor = conn.cursor()
    
    # data fetching
    if date_filter is None:
        cursor.execute("""SELECT complaints.*, users.name 
        FROM complaints 
        JOIN users ON complaints.Student_id = users.id""")
        result = cursor.fetchall()
    else:
        cursor.execute("""SELECT complaints.*, users.name 
        FROM complaints 
        JOIN users ON complaints.Student_id = users.id
        WHERE complaints.Date=%s""",(date_filter,))
        result = cursor.fetchall()
    cursor.close()
    conn.close()
    
    
    today = date.today()
    if date_filter:
        filename = f"complaints_{date_filter}.csv"
    else:
        filename = f"complaints_{today}.csv"
    
    # writing inside the file
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID","Student_id","Room","Issue","Status","Date","Name"])
        writer.writerows(result)
    
    print(f"Report saved as {filename}!")


# ------------------main------------------------

setup_table()


while True:

    print("="*50)
    print("  HOSTEL COMPLAINT SYSTEM")
    print("="*50)
    print(" 1-> Registration")
    print(" 2-> Login as Student")
    print(" 3-> Login as Warden")
    print(" 4-> Exit")
    print("="*50)

    choice=input("Enter your choice : ")

    # Registration

    if choice=="1":
        name=input("Enter your name :")
        password=input("Create your personal password : ")
        role=input("Enter your role (student/warden) : ")
        if role.lower() not in ["student","warden"]:
            print("Invalid role! Please enter 'student' or 'warden' only.")
        else:
            registration(name,role.lower(),password)
            print(f"Congratulations! {name} Your newly registration done successfully ")

    # Login as a Student

    elif choice=="2":
        name=input("Enter your name : ")
        password=input("Enter your login Password : ")
        s_user_data=login(name,password)

        if s_user_data is None:
            print("Something went wrong. Please enter correct details. ")
        elif s_user_data[2].lower()!="student":
            print("Access denied! You are not Student.")

        else:
            while True:
                print("="*50)
                print(" A-> Submit Your Complaint")
                print(" B-> View Your Complaints")
                print(" C-> Exit")
                print("="*50)
                s_choice=input("Enter Your Choice : ")

                if s_choice=="a"or s_choice=="A":
                    stu_id=s_user_data[0]
                    room_no=input("Enter your room no : ")
                    Issue=input("Enter your Issue : ")
                    Date = input("Enter date of Issue (YYYY-MM-DD) : ")
                    submit_complaint(stu_id,room_no,Issue,Date)
                    print("Complaint registered successfully!")
                elif s_choice=="b" or s_choice=="B":
                    stu_id=s_user_data[0]
                    x=View_my_complaint(stu_id)
                    header = f"{'ID':<10} {'STU_ID':<10} {'ROOM':<10} {'ISSUE':<20} {'STATUS':<10} {'DATE':<10}"
                    print(header)
                    print("-"*len(header))
                    for row in x:
                        print(f"{row[0]:<10} {row[1]:<10} {row[2]:<10} {row[3]:<20} {row[4]:<10} {str(row[5]):<10}")
                elif s_choice=="c"or s_choice=="C":
                    break
                else:
                    print("Something went wrong!")

    # Login as a Warden 


    elif choice=="3":
        w_name=input("Enter your name : ")
        w_password=input("Enter your password : ")
        w_user_data=login(w_name,w_password)
    
        if w_user_data is None:
            print("Invalid credentials!")
        elif w_user_data[2].lower()!="warden":
            print("Access denied! You are not a warden.")
        else:
            while True:
                print("="*50)
                print("A-> View All Complaints")
                print("B-> Update Complaint Status")
                print("C-> Export CSV")
                print("D-> Exit")
                print("="*50)
                w_choice=input("Enter Your Choice : ")

                if w_choice=="a"or w_choice=="A":
                    w_rows=View_all_complaints()
                    w_header = f"{'ID':<10} {'STU_ID':<10} {'NAME':<10} {'ROOM':<10} {'ISSUE':<20} {'STATUS':<10} {'DATE':<10}"
                    print(w_header)
                    print("-"*len(w_header))
                    for row in w_rows:
                        print(f"{row[0]:<10} {row[1]:<10} {row[2]:<10} {row[3]:<10} {row[4]:<20} {row[5]:<10} {str(row[6]):<10}")

                elif w_choice=="b"or w_choice=="B":
                    complaint_id = int(input("Enter Complaint ID to update : "))
                    print("-"*50)
                    print("1-> Pending")
                    print("2-> In Progress")
                    print("3-> Resolved")
                    print("-"*50)
                    status_choice = input("Enter: ")

                    if status_choice == "1":
                        new_status = "Pending"
                    elif status_choice == "2":
                        new_status = "In Progress"
                    elif status_choice == "3":
                        new_status = "Resolved"
                    else:
                        print("Invalid choice!")
                        continue  # back to the loop

                    update__on_problem(complaint_id,new_status)
                    print("_"*50)
                    print(f"  Complaint #{complaint_id} updated to '{new_status}' successfully!")
                    print("_"*50)

                elif w_choice=="c" or w_choice=="C":
                    date_choice = input("Do you want report for a specific date? (y/n) : ")
                    if date_choice == "y" or date_choice=="Y":
                        date_filter = input("Enter date (YYYY-MM-DD) : ")
                        export_csv(date_filter)
                    else:
                        export_csv()

                elif w_choice=="d"or w_choice=="D":
                    break
                else:
                    print("Invalid choice!")

    # Exit

    elif choice=="4":
        break
    else:
        print("Invalid choice! Please try again.")