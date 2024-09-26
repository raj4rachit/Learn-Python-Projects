import sqlite3
import customtkinter
from tkinter import messagebox
from tkinter import *
from tkinter import ttk


# Initialize the customtkinter application
app = customtkinter.CTk()
app.title("Employee Management System")
app.geometry("800x500")
app.config(bg="#17043d")

# Define fonts
font1 = ("Arial", 20, "bold")
font2 = ("Arial", 15, "bold")
font3 = ("Arial", 12, "bold")

# Create a frame within the application with specified dimensions
frame1 = customtkinter.CTkFrame(app, fg_color="#FFFFFF", width=450, height=500)
frame1.place(x=350, y=0)

# Connect to SQLite database
db = sqlite3.connect("Employee.db")
cursor = db.cursor()  # Initialize cursor
cursor.execute("CREATE TABLE IF NOT EXISTS EMPLOYEES (Employee_ID INTEGER PRIMARY KEY, Name TEXT, Age TEXT, Role TEXT)")


# Define a function to save employee data
def insert():
    """Save the employee data to the database."""
    employee_id = id_entry.get()
    name = name_entry.get()
    age = age_entry.get()
    role = role_entry.get()
    if employee_id and name and age and role:  # Check if all fields are filled
        try:
            db.execute("INSERT INTO EMPLOYEES (Employee_ID, Name, Age, Role) VALUES (?, ?, ?, ?)",
                       (employee_id, name, age, role))
            db.commit()  # Commit changes to the database
            messagebox.showinfo("Success", "Employee data saved successfully")
            # Optionally clear fields after saving
            clear()
            display_data()
        except Exception as e:
            messagebox.showerror("Error", f"Error saving data: {e}")
    else:
        messagebox.showerror("Error", "All fields are required")

def delete():
    employee_id = id_entry.get()
    if employee_id:
        try:
            db.execute("DELETE FROM EMPLOYEES WHERE Employee_ID=?", (employee_id,))
            db.commit()
            messagebox.showinfo("Success", "Employee deleted successfully")
            clear()
            display_data()
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting data: {e}")
    else:
        messagebox.showerror("Error", "Please enter the Employee ID to delete")

def get_data(event):
   clear()
   selected_row = tv.focus()
   data = tv.item(selected_row)
   row = data["values"]
   if row:  # Check if row contains data
       id_entry.insert(0, row[0])
       name_entry.insert(0, row[1])
       age_entry.insert(0, row[2])
       role_entry.insert(0, row[3])
   else:
       messagebox.showinfo("Info", "No data available for this selection")

def update():
    employee_id = id_entry.get()
    name = name_entry.get()
    age = age_entry.get()
    role = role_entry.get()
    if employee_id and name and age and role:
        try:
            db.execute("UPDATE EMPLOYEES SET Name=?, Age=?, Role=? WHERE Employee_ID=?",
                       (name, age, role, employee_id))
            db.commit()
            messagebox.showinfo("Success", "Employee data updated successfully")
            clear()
            display_data()
        except Exception as e:
            messagebox.showerror("Error", f"Error updating data: {e}")
    else:
        messagebox.showerror("Error", "All fields are required for update")


def clear():
    id_entry.delete(0, 'end')
    name_entry.delete(0, 'end')
    age_entry.delete(0, 'end')
    role_entry.delete(0, 'end')

def fetch():
    cursor.execute("SELECT * FROM EMPLOYEES")
    rows = cursor.fetchall()
    return rows


# Create entry widgets for employee data
id_label = customtkinter.CTkLabel(app, text="ID:", font=font1)
id_label.place(x=20, y=20)
id_entry = customtkinter.CTkEntry(app, font=font2, fg_color="#FFFFFF", border_color="#FFFFFF", width=200)
id_entry.place(x=140, y=20)

name_label = customtkinter.CTkLabel(app, text="Name:", font=font1)
name_label.place(x=20, y=80)
name_entry = customtkinter.CTkEntry(app, font=font2, fg_color="#FFFFFF", border_color="#FFFFFF", width=200)
name_entry.place(x=140, y=80)

age_label = customtkinter.CTkLabel(app, text="Age:", font=font1)
age_label.place(x=20, y=140)
age_entry = customtkinter.CTkEntry(app, font=font2, fg_color="#FFFFFF", border_color="#FFFFFF", width=200)
age_entry.place(x=140, y=140)

role_label = customtkinter.CTkLabel(app, text="Role:", font=font1)
role_label.place(x=20, y=200)
role_entry = customtkinter.CTkEntry(app, font=font2, fg_color="#FFFFFF", border_color="#FFFFFF", width=200)
role_entry.place(x=140, y=200)

# Button to save employee data
save_button = customtkinter.CTkButton(app, command=insert, text="Save", font=font1, fg_color="#03a819", hover_color="#03a819", corner_radius=20, width=120, cursor="hand2")
save_button.place(x=70, y=250)

update_button = customtkinter.CTkButton(app, command=update, text="Update", font=font1, fg_color="#b86512", hover_color="#b86512", corner_radius=20, width=127, cursor="hand2")
update_button.place(x=200, y=250)

clear_button = customtkinter.CTkButton(app, command=clear, text="Clear", font=font1, fg_color="#6e0e53", hover_color="#6e0e53", corner_radius=20, width=120, cursor="hand2")
clear_button.place(x=70, y=300)

delete_button = customtkinter.CTkButton(app, command=delete, text="Delete", font=font1, fg_color="#cf061a", hover_color="#cf061a", corner_radius=20, width=140, cursor="hand2")
delete_button.place(x=200, y=300)


# Create TreeView to display data
frame2 = customtkinter.CTkFrame(app, fg_color="#FFFFFF", width=450, height=500)
frame2.place(x=500, y=0)  # Adjust position to the right side

style = ttk.Style()
style.configure("mystyle.Treeview", font=font3, rowheight=50)
style.configure("mystyle.Treeview.Heading", font=font2)
style.layout("mystyle.Treeview", [("mystyle.Treeview.treearea", {"sticky": "nswe"})])


tv = ttk.Treeview(frame2, columns=(1, 2, 3, 4), show="headings", style="mystyle.Treeview")
tv.heading(1, text="ID")
tv.column(1, width=105)
tv.heading(2, text="Name")
tv.column(2, width=105)
tv.heading(3, text="Age")
tv.column(3, width=105)
tv.heading(4, text="Role")
tv.column(4, width=105)
tv.pack(fill='both', expand=True)

tv.bind("<ButtonRelease-1>", get_data)

def display_data():
    tv.delete(*tv.get_children())
    for row in fetch():
        tv.insert("", END, values=row)

# Update GUI to refresh data periodically or on event
def refresh_data():
    display_data()
    app.after(10000, refresh_data)  # Refresh data every 10 seconds

app.after(100, refresh_data)  # Initial call to display data

# Run the application main loop
app.mainloop()
