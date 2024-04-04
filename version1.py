# Importing all from Tkinter graphical user interface (GUI) package
from tkinter import *

# Imtporting Tkinter submodule: "messagebox"
from tkinter import messagebox

# Importing elements of the TTK module
from tkinter import ttk

# Psycopg2 adapter module to connect to database
import psycopg2

# Run query function
def run_query(query, parameters=()):

    # Establishing connection to database
    try:
        conn = psycopg2.connect(host = "localhost", dbname = "studentdb", port = 5432, user = "postgres", password = "superuser")
    
    # Cursor to execute SQL queries using Python shell
        cur = conn.cursor()

    # Query result
        cur.execute(query, parameters)
        if query.lower().startswith("select"):
            query_result = cur.fetchall()
        else:
            conn.commit()
            query_result = None
        cur.close()
        conn.close()
        return query_result
    except psycopg2.Error as e:
        messagebox.showerror("Database error!", str(e))
        return None

# Refresh tree view function 
def refresh_treeview():

    # Deleting existing data in treeview
    for item in tree.get_children():
        tree.delete(item)

    # Getting student data from database
    records = run_query("SELECT * FROM students;")
    
    # Inserting student data into tree view
    for record in records:
        tree.insert("", END, values=record)

# Inserting student data function
def insert_data():
    query = "INSERT INTO students(name, address, age, number) VALUES (%s, %s, %s, %s)"
    parameters = (name_entry.get(), address_entry.get(), age_entry.get(), number_entry.get())
    run_query(query, parameters)
    messagebox.showinfo("Database Information", "Student data successfully added!")
    refresh_treeview()
    root.update()

# Deleting student data function
def delete_data():

    # ID of selected record in treeview
    selected_record = tree.selection()[0]

    # Student ID of selected record in treeview 
    student_id = tree.item(selected_record)["values"][0]

    # Deleting student record
    query = "DELETE FROM students WHERE student_id=%s"
    parameters = (student_id,)
    run_query(query, parameters)
    messagebox.showinfo("Database Information", "Student data successfully deleted!")
    refresh_treeview()
    root.update()

# Updating student data function
def update_data():
    # ID of selected record in treeview
    selected_record = tree.selection()[0]

    # Student ID of selected record in treeview 
    student_id = tree.item(selected_record)["values"][0]

    # Updating student record
    query = "UPDATE students SET name = %s, address = %s, age = %s, number = %s WHERE student_id = %s"
    parameters = (name_entry.get(), address_entry.get(), age_entry.get(), number_entry.get(), student_id)
    run_query(query, parameters)
    messagebox.showinfo("Database Information", "Student data successfully updated!")
    refresh_treeview()
    root.update()

# Creating table
def create_table():
    query = "CREATE TABLE IF NOT EXISTS students(student_id serial primary key, name text, address text, age int, number int);"
    run_query(query)
    messagebox.showinfo("Database Information", "Student table successfully created!")
    refresh_treeview
    root.update
    
# User window
root = Tk()
root.title("Student Database Management System")

# Frame and grid layout manager to enter student data
frame = LabelFrame(root, text="Student Data")
frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

# "Name" field
Label(frame, text="Name:").grid(row=0, column=0, padx=2, sticky="w")
name_entry = Entry(frame)
name_entry.grid(row=0, column=1, pady=2, sticky="ew")

# "Address" field
Label(frame, text="Address:").grid(row=1, column=0, padx=2, sticky="w")
address_entry = Entry(frame)
address_entry.grid(row=1, column=1, pady=2, sticky="ew")

# "Age" field
Label(frame, text="Age:").grid(row=2, column=0, padx=2, sticky="w")
age_entry = Entry(frame)
age_entry.grid(row=2, column=1, pady=2, sticky="ew")

# "Number" field
Label(frame, text="Number:").grid(row=3, column=0, padx=2, sticky="w")
number_entry = Entry(frame)
number_entry.grid(row=3, column=1, pady=2, sticky="ew")

# Frame and grid layout manager to place buttons
button_frame = Frame(root)
button_frame.grid(row=1, column=0, pady=10, sticky="ew")

# "Create table" button
Button(button_frame, text="Create Table", command=create_table).grid(row=0, column=0, padx=5)

# "Add data" button
Button(button_frame, text="Add Student", command=insert_data).grid(row=0, column=1, padx=5)

# "Update data" button
Button(button_frame, text="Update Student", command=update_data).grid(row=0, column=2, padx=5)

# "Delete data" button
Button(button_frame, text="Delete Student", command=delete_data).grid(row=0, column=3, padx=5)

# Tree view frame
tree_frame = Frame(root)
tree_frame.grid(row=2, column=0, pady=10, sticky="nsew")

# Scrollbar on right hand side of tree view frame
tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT, fill=Y)

# Tree view widget
tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll, selectmode="browse")
tree.pack()
tree_scroll.config(command=tree.yview)

# Tree view columns and headings
tree["columns"] = ("student_id", "name", "address", "age", "number")
tree.column("#0", width=0, stretch=NO)
tree.column("student_id", anchor=CENTER, width=50)
tree.column("name", anchor=CENTER, width=120)
tree.column("address", anchor=CENTER, width=120)
tree.column("age", anchor=CENTER, width=50)
tree.column("number", anchor=CENTER, width=120)
tree.heading("student_id", text="ID", anchor=CENTER)
tree.heading("name", text="Name", anchor=CENTER)
tree.heading("address", text="Address", anchor=CENTER)
tree.heading("age", text="Age", anchor=CENTER)
tree.heading("number", text="Number", anchor=CENTER)

# Populating tree view with student data
refresh_treeview()

# Keeping user window open (looping)                     
root.mainloop()