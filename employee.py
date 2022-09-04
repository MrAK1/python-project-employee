import sqlite3
import csv


DB_NAME = "employees.db"
FILE = "employees.csv"
INPUT_STRING = """
Enter the option:
    1. CREATE TABLE EMPLOYEE.
    2. Import data from csv file.
    3. Add new record to database.
    4. Delete a record from id of user.
    5. Delete all records from employee table.
    6. Query all records from employee table.
    7. Update a record using id of user.
    8. Press any key to exit.
"""

CREATE_EMPLOYEES_TABLE_QUERY = """
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        FIRST_NAME CHAR(255) NOT NULL,
        LAST_NAME CHAR(255) NOT NULL,
        ADDRESS CHAR(255) NOT NULL,
        EMAIL CHAR(255) NOT NULL,
        PHONE1 CHAR(255) NOT NULL,
        TEL_no CHAR(255),
        JOB_NAME NOT NULL,
        SALARY INTEGER NOT NULL
    );
"""
COLUMNS = (
    "FIRST_NAME",
    "LAST_NAME", 
    "ADDRESS", 
    "EMAIL", 
    "PHONE1", 
    "TEL_no", 
    "JOB_NAME", 
    "SALARY",
)

COLUMN_INPUT_STRING = f"""
    Which column would you like to update? \
Please make sure column is one of the {COLUMNS}
    """
#CRUDE operation => Create, Retrieve(select), Update, Delete, Exit

def create_connection(db_name):
    """Creating connection and return cursor object

    Returns:
        conn: sqlite3 connection object
    """
    conn = None
    try:
        conn = sqlite3.connect(db_name)
    except Exception as e:
        print(str(e))
    finally:
        return conn
    
def create_table(conn):
    """Create a table

    Args:
        conn (sqlite3): sqlite3 connection object
    """
    cur = conn.cursor()
    cur.execute(CREATE_EMPLOYEES_TABLE_QUERY)
    conn.commit()
    print("Employee table was sucessfully created.")

def open_csv_file(FILE):
    """Open csv file and return all records in list of tuple

    Args:
        FILE (str): name of file

    Returns:
        list[tuple]: all records from csv file
    """
    db_data = []

    with open(FILE) as f:
        """Opens file as value f
        """
        data = csv.reader(f, delimiter=",")
        for datum in data:
            db_data.append(tuple(datum))
    return db_data[1:]

def insert_employees(conn, db_data):
    """Insert records to table

    Args: 
        conn (sqlite3 connection): sqlite3 connection object
        db_data (list[tuple]): all records for table

    Returns:
        None:None
    """
    employee_add_query = """
    INSERT INTO employees
    (FIRST_NAME, LAST_NAME, ADDRESS,  EMAIL, PHONE1, TEL_no, JOB_NAME, SALARY)

    VALUES(?,?,?,?,?,?,?,?);
    """
    cur = conn.cursor()
    cur.executemany(employee_add_query, db_data)
    conn.commit()
    print("Successfully inserted data into employee table.")

def select_all_records(conn):
    """Select and print records from table

    Args:
        conn (sqlite3): sqlite3 connection object
    """
    cur = conn.execute("Select * from employees ;")
    for row in cur:
        print(row)

def update_employee(conn, column_name, employee_id, column_value):
    """Update single record to table

    Args:
        conn (sqlite2 connection): sqlite3 connection object
        column_name (str): name of column
        employee_id (int): id of user
        column_value (str): value of column
    """
    cur = conn.execute(f"UPDATE employees set {column_name}=? where id=?", (column_value, employee_id))
    conn.commit()
    print(f"Successfully updated {column_name} of employee {employee_id}")        

def delete_employee_id(conn, employee_id):
    """Delete single record from table

    Args:
        conn (sqlite3 connection): sqlite3 connection object
        employee_id (int): id of user
    """
    cur = conn.execute("Delete from employees where id = ?", (employee_id,))
    conn.commit()
    print("Successfully deleted record from employee table.")

def delete_all_records(conn):
    """Delete all records from table

    Args:
        conn (sqlite3 connection): sqlite3 connection object
    """
    cur = conn.execute("Delete from employees")
    conn.commit()
    print("Successfully deleted all records from employee table.")

def main():
    """_summary_
    """
    conn = create_connection(DB_NAME)

    while True:

        user_input = input(INPUT_STRING)

        if user_input == "1":
            create_table(conn)

        elif user_input == "2":
            data = open_csv_file(FILE)
            insert_employees(conn, data)
        
        elif user_input == "3":
            data = []
            for column in COLUMNS:
                user_input = input(f"Enter {column}: ")
                data.append(employee_id)
            data = tuple(data)
            insert_employees(conn, [data])

        elif user_input == "4":
            employee_id = input("Enter id of employee: ")
            if employee_id.isnumeric():
                delete_employee_id(conn, employee_id)

        elif user_input == "5":
            confirmation = input(
                "Are you sure? \
                Press Y or Yes to continue, or \
                Press N or No to skip."
            )
            if confirmation.lower() in ['y', 'yes']:
                delete_all_records(conn)

        elif user_input == "6":
            select_all_records(conn)

        elif user_input == "7":
            employee_id = input("Enter id of user:")
            if employee_id.isnumeric():
                column_name = input(COLUMN_INPUT_STRING)
                column_value = input(f"Enter value of {column_name}: ")
                update_employee(conn, column_name, employee_id, column_value)

        else:
            exit()

if __name__ == "__main__":
    main()
