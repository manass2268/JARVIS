import sqlite3
from tabulate import tabulate
con=sqlite3.connect('Jarvis.db')
cur=con.cursor()

query="CREATE TABLE IF NOT EXISTS System_Command (Id INTEGER PRIMARY KEY AUTOINCREMENT, Name varchar(1000) null, File_Path varchar(100000) null)"
cur.execute(query)
query="CREATE TABLE IF NOT EXISTS Web_Command (Id INTEGER PRIMARY KEY AUTOINCREMENT, Name varchar(1000) null, Url varchar(100000) null)"
cur.execute(query)
query="CREATE TABLE IF NOT EXISTS Contact_Command (Id INTEGER PRIMARY KEY AUTOINCREMENT, Name varchar(255), Phone_No varchar(255) primary key,Sec_Phone_No varchar(255) primary Key, Email varchar(255) null)" 
cur.execute(query)

#=====================Menu Function========================

def menu():
    print("Welcome to JARVIS Command Control Database")
    print('PRESS 1 FOR Continue:')
    print('PRESS 2 FOR Exit:')
    ch=int(input('DO YOU WANT TO CONTINUE :'))
    while ch==1:
        print("Welcome to JARVIS Command Control Database")
        print("1.Add a new command to the database:")
        print("2.Show Commands in the database:")
        print("3.Delete a command from the database:")
        print("4.Delete All Command fromt the database")
        print("5.Edit a command in the database:")
        print("6.Reset Command IDs:")
        print("7. Search Command.")
        print("8.Exit:")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            Add_command()
            print("Command IDs have been Added successfully.")
        elif choice == 2:
            Show_command()
            print("Command IDs have been Show successfully.")
        elif choice == 3:
            Delete_command()
            print("Command IDs have been Delete successfully.")
        elif choice == 4:
            Delete_All_Command()
            print("Command IDs have been All Deleted successfully.")
        elif choice == 5:
            Edit_command()
            print("Command IDs have been Edit successfully.")
        elif choice == 6:
            Reset_command_id()
            print("Command IDs have been reset successfully.")
        elif choice == 7:
            Search_Command()
        elif choice == 8:
            print("You have chosen to exit")
            break
        else:
            print("Invalid choice, please try again.")
        
#=============================Add Command========================
def Add_command():
    print("1. System_Command")
    print("2. Web_Command")
    print("3. Contact_Command")
    print("4. Exit")
    ch = input("Enter your choice: ")
    if ch == '1':
        Add_System_Command()
    elif ch == '2':
        Add_Web_Command()
    elif ch == '3':
        Add_Contact_Command()
    elif ch == '4':
        print("You have chosen to exit")
        return

    else:
        print("Invalid choice, please try again.")
        Add_command()
#=============================Add System Command========================
def Add_System_Command():
    # 1. Purane data dikhaye
    print("\n--- Existing System Commands ---")
    cur.execute("SELECT * FROM System_Command")
    rows = cur.fetchall()
    if rows:
        print(tabulate(rows, headers=["Id", "Name", "File_Path"], tablefmt="grid"))
    else:
        print("No commands found in System_Command.")

    # 2. Naya data lein
    name = input("Enter the name of the command: ")
    file_path = input("Enter the file path of the command: ")
    query = "INSERT INTO System_Command (Name, File_Path) VALUES (?, ?)"
    cur.execute(query, (name, file_path))
    con.commit()
    print("\nCommand added successfully.")

    # 3. Updated table dikhaye
    print("\n--- Updated System Commands ---")
    cur.execute("SELECT * FROM System_Command")
    rows = cur.fetchall()
    print(tabulate(rows, headers=["Id", "Name", "File_Path"], tablefmt="grid"))
    Add_command()
#=============================Add Web Command========================
def Add_Web_Command():
    # 1. Purane data dikhaye
    print("\n--- Existing Web Commands ---")
    cur.execute("SELECT * FROM Web_Command")
    rows = cur.fetchall()
    if rows:
        print(tabulate(rows, headers=["Id", "Name", "Url"], tablefmt="grid"))
    else:
        print("No commands found in Web_Command.")

    # 2. Naya data lein
    name = input("Enter the name of the command: ")
    url = input("Enter the URL of the command: ")
    query = "INSERT INTO Web_Command (Name, Url) VALUES (?, ?)"
    cur.execute(query, (name, url))
    con.commit()
    print("\nWeb Command added successfully.")

    # 3. Updated table dikhaye
    print("\n--- Updated Web Commands ---")
    cur.execute("SELECT * FROM Web_Command")
    rows = cur.fetchall()
    print(tabulate(rows, headers=["Id", "Name", "Url"], tablefmt="grid"))
    Add_command()
#=================Add Contact_Command=======================================
def Add_Contact_Command():
    while True:
        print("\nHow do you want to add contacts?")
        print("1. Manually add contact")
        print("2. Import contacts from CSV")
        print("3. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            # Manual add
            name = input("Enter the name of the contact: ")
            phone_no = input("Enter the phone number of the contact: ")
            email = input("Enter the email of the contact (optional): ")
            query = "INSERT INTO Contact_Command (Name, Phone_No, Email) VALUES (?, ?, ?)"
            cur.execute(query, (name, phone_no, email))
            con.commit()
            print("\nContact added successfully.")
        elif choice == '2':
            import csv
            csv_file = 'contacts.csv'
            try:
                with open(csv_file, 'r', encoding='utf-8') as csvfile:
                    csvreader = csv.reader(csvfile)
                    next(csvreader, None)  # skip header if present
                    for row in csvreader:
                        # CSV columns: SR. No.,First Name,Middle Name,Last Name,Phone 1 - Value,Phone 2 - Value
                        first = row[1].strip() if len(row) > 1 else ""
                        middle = row[2].strip() if len(row) > 2 else ""
                        last = row[3].strip() if len(row) > 3 else ""
                        phone1_raw = row[4].strip() if len(row) > 4 else ""
                        phone2_raw = row[5].strip() if len(row) > 5 else ""
        
                        # Phone 1 - Value: split if contains ':::' or ','
                        phone_parts = [p.strip() for p in phone1_raw.replace('.00', '').replace(' ', '').split(':::')] if phone1_raw else []
                        phone_no = phone_parts[0] if len(phone_parts) > 0 else ""
                        sec_phone_no = phone_parts[1] if len(phone_parts) > 1 else ""
        
                        # Agar Phone 2 - Value bhi hai aur sec_phone_no blank hai to use bhi daal do
                        if not sec_phone_no and phone2_raw:
                            sec_phone_no = phone2_raw.replace('.00', '').replace(' ', '')
        
                        # Name banaye (sirf non-empty parts)
                        name = " ".join(part for part in [first, middle, last] if part)
                        email = ""
        
                        # Sirf valid name aur phone ho to hi insert karo
                        if name and phone_no:
                            cur.execute(
                                "INSERT INTO Contact_Command (Name, Phone_No, Sec_Phone_No, Email) VALUES (?, ?, ?, ?)",
                                (name, phone_no, sec_phone_no, email)
                            )
                    con.commit()
                print("\nAll valid contacts from CSV added successfully.")
            except Exception as e:
                print("Error importing from CSV:", e)
        elif choice == '3':
            break

        else:
            print("Invalid choice, please try again.")
            continue

        # Show updated table after every add/import
        print("\n--- Updated Contact Commands ---")
        cur.execute("SELECT * FROM Contact_Command")
        rows = cur.fetchall()
        print(tabulate(rows, headers=["Id", "Name", "Phone_No", "Email"], tablefmt="grid"))

        again = input("Do you want to add/import another contact? (y/n): ").strip().lower()
        if again != 'y':
            break
#=============================Show Commands========================
def Show_command():
    print("1. System_Command")
    print("2. Web_Command")
    print("3. Contact_Command")
    print("4. Exit")
    ch = input("Enter your choice: ")
    if ch == '1':
        Show_System_Command()
    elif ch == '2':
        Show_Web_Command()
    elif ch == '3':
        Show_Contact_Command()
    elif ch == '4':
        print("You have chosen to exit")
        return
    else:
        print("Invalid choice, please try again.")
        Show_command()
#=============================Show System Command========================
def Show_System_Command():
    query = "SELECT * FROM System_Command"
    cur.execute(query)
    rows = cur.fetchall()
    if rows:
        print(tabulate(rows, headers=["Id", "Name", "File_Path"], tablefmt="grid"))
    else:
        print("No commands found in System_Command.")
    Show_command()
#=============================Show Web Command========================
def Show_Web_Command():

    query = "SELECT * FROM Web_Command"
    cur.execute(query)
    rows = cur.fetchall()
    if rows:
        print(tabulate(rows, headers=["Id", "Name", "Url"], tablefmt="grid"))
    else:
        print("No commands found in Web_Command.")
    Show_command()
#=============================Show Contact Command========================
def Show_Contact_Command():
    query = "SELECT * FROM Contact_Command"
    cur.execute(query)
    rows = cur.fetchall()
    # Filter only valid rows
    rows = [row for row in rows if row[1] and (row[2] or row[3])]
    if rows:
        print(tabulate(rows, headers=["Id", "Name", "Phone_No", "Sec_Phone_No", "Email"], tablefmt="grid"))
    else:
        print("No valid contacts found in Contact_Command.")
    return

#=============================Delete Command========================
def Delete_command():
    print("1. System_Command")
    print("2. Web_Command")
    print("3. Contact_Command")
    print("4. Exit")
    ch = input("Enter your choice: ")
    if ch == '1':
        Delete_System_Command()
    elif ch == '2':
        Delete_Web_Command()
    elif ch == '3':
        Delete_Contact_Command()
    elif ch == '4':
        print("You have chosen to exit")
        return
    else:
        print("Invalid choice, please try again.")
        Delete_command()
#=============================Delete System Command========================
def Delete_System_Command():
    print("\n--- Existing System Commands ---")
    cur.execute("SELECT * FROM System_Command")
    rows = cur.fetchall()
    if rows:
        print(tabulate(rows, headers=["Id", "Name", "File_Path"], tablefmt="grid"))
    else:
        print("No commands found in System_Command.")

    id = input("Enter the Id of the command to delete: ")
    query = "DELETE FROM System_Command WHERE Id = ?"
    cur.execute(query, (id,))
    con.commit()
    print("Command deleted successfully.")

    print("\n--- Updated System Commands ---")
    cur.execute("SELECT * FROM System_Command")
    rows = cur.fetchall()
    print(tabulate(rows, headers=["Id", "Name", "File_Path"], tablefmt="grid"))
    
#=============================Delete Web Command========================
def Delete_Web_Command():
    print("\n--- Existing Web Commands ---")
    cur.execute("SELECT * FROM Web_Command")
    rows = cur.fetchall()
    if rows:
        print(tabulate(rows, headers=["Id", "Name", "Url"], tablefmt="grid"))
    else:
        print("No commands found in Web_Command.")

    id = input("Enter the Id of the command to delete: ")
    query = "DELETE FROM Web_Command WHERE Id = ?"
    cur.execute(query, (id,))
    con.commit()
    print("Command deleted successfully.")

    print("\n--- Updated Web Commands ---")
    cur.execute("SELECT * FROM Web_Command")
    rows = cur.fetchall()
    print(tabulate(rows, headers=["Id", "Name", "Url"], tablefmt="grid"))
#=============================Delete Contact Command========================
def Delete_Contact_Command():
    print("\n--- Existing Contact Commands ---")
    cur.execute("SELECT * FROM Contact_Command")
    rows = cur.fetchall()
    if rows:
        print(tabulate(rows, headers=["Id", "Name", "Phone_No", "Email"], tablefmt="grid"))
    else:
        print("No commands found in Contact_Command.")
        return

    id = input("Enter the Id of the contact command to delete: ")
    query = "DELETE FROM Contact_Command WHERE Id = ?"
    cur.execute(query, (id,))
    con.commit()
    print("Contact command deleted successfully.")

    print("\n--- Updated Contact Commands ---")
    cur.execute("SELECT * FROM Contact_Command")
    rows = cur.fetchall()
    print(tabulate(rows, headers=["Id", "Name", "Phone_No", "Email"], tablefmt="grid"))
    # Bas return karo, Delete_command() call mat karo
    return
#===========Delete All Command===============
def Delete_All_Command():
    print("Which table's ALL data do you want to delete?")
    print("1. System_Command")
    print("2. Web_Command")
    print("3. Contact_Command")
    print("4. Exit")
    ch = int(input("Enter your choice: "))
    if ch == 1:
        Delete_All_System_Command()
    elif ch == 2:
        Delete_All_Web_Command()
    elif ch == 3:
        Delete_All_Contact_Command()
    elif ch == 4:
        print("You have chosen to exit.")
        return
    else:
        print("Invalid choice, please try again.")
        Delete_All_Command()
#==========================Delete_All__System_Command==============================    
def Delete_All_System_Command():
    confirm = input("Are you sure you want to delete ALL System Commands? (y/n): ").strip().lower()
    if confirm == 'y':
        cur.execute("DELETE FROM System_Command")
        con.commit()
        print("All System Commands deleted successfully.")
    else:
        print("Operation cancelled.")


#========================Delete_All__Web_Command================================
def Delete_All_Web_Command():
    confirm = input("Are you sure you want to delete ALL Web Commands? (y/n): ").strip().lower()
    if confirm == 'y':
        cur.execute("DELETE FROM Web_Command")
        con.commit()
        print("All Web Commands deleted successfully.")
    else:
        print("Operation cancelled.")
#================================Delete_All__Contact_Command========================
def Delete_All_Contact_Command():
    confirm = input("Are you sure you want to delete ALL Contact Commands? (y/n): ").strip().lower()
    if confirm == 'y':
        cur.execute("DELETE FROM Contact_Command")
        con.commit()
        print("All Contact Commands deleted successfully.")
    else:
        print("Operation cancelled.")
#==========Reset Command Id========================
def Reset_command_id():
    print("1. Reset System Command IDs")
    print("2. Reset Web Command IDs")
    print("3. Reset Contact command IDs")
    print("4. Exit")
    ch = input("Enter your choice: ")
    if ch == '1':
        Reset_system_command_ids()
    elif ch == '2':
        Reset_web_command_ids()
    elif ch == '3':
        Reset_Contact_id()
    elif ch == '4':
        print("You Chosen the Exit")
        return
    else:
        print("Invalid choice, please try again.")
        Reset_command_id()
#===========================Reset System Command Id========================
def Reset_system_command_ids():
    cur.execute("SELECT Name, File_Path FROM System_Command")
    data = cur.fetchall()
    if data:
        print("\n--- System Commands Before Reset ---")
        print(tabulate([(i+1, row[0], row[1]) for i, row in enumerate(data)], headers=["Id", "Name", "File_Path"], tablefmt="grid"))
    else:
        print("No commands found in System_Command.")
        return
    cur.execute("DELETE FROM System_Command")
    con.commit()
    for i, row in enumerate(data, start=1):
        cur.execute("INSERT INTO System_Command (Id, Name, File_Path) VALUES (?, ?, ?)", (i, row[0], row[1]))
    con.commit()
    print("\nSystem Command IDs have been reset successfully.")
    # Ab nayi table dikhao (nayi Ids ke sath)
    cur.execute("SELECT * FROM System_Command")
    rows = cur.fetchall()
    print(tabulate(rows, headers=["Id", "Name", "File_Path"], tablefmt="grid"))
#===========================Reset Web Command Id========================
def Reset_web_command_ids():
    cur.execute("SELECT Name, Url FROM Web_Command")
    data = cur.fetchall()
    if data:
        print("\n--- Web Commands Before Reset ---")
        print(tabulate([(i+1, row[0], row[1]) for i, row in enumerate(data)], headers=["Id", "Name", "Url"], tablefmt="grid"))
    else:
        print("No commands found in Web_Command.")
        return
    cur.execute("DELETE FROM Web_Command")
    con.commit()
    for i, row in enumerate(data, start=1):
        cur.execute("INSERT INTO Web_Command (Id, Name, Url) VALUES (?, ?, ?)", (i, row[0], row[1]))
    con.commit()
    print("\nWeb Command IDs have been reset successfully.")
    # Ab nayi table dikhao (nayi Ids ke sath)
    cur.execute("SELECT * FROM Web_Command")
    rows = cur.fetchall()
    print(tabulate(rows, headers=["Id", "Name", "Url"], tablefmt="grid"))
#===================Reset Contact Command Idz===================
def Reset_Contact_id():
    cur.execute("SELECT Name, Phone_No, Email FROM Contact_Command")
    data = cur.fetchall()
    if data:
        print("\n--- Contact Commands Before Reset ---")
        print(tabulate([(i+1, row[0], row[1], row[2]) for i, row in enumerate(data)], headers=["Id", "Name", "Phone_No", "Email"], tablefmt="grid"))
    else:
        print("No commands found in Contact_Command.")
        return
    cur.execute("DELETE FROM Contact_Command")
    con.commit()
    for i, row in enumerate(data, start=1):
        cur.execute("INSERT INTO Contact_Command (Id, Name, Phone_No, Email) VALUES (?, ?, ?, ?)", (i, row[0], row[1], row[2]))
    con.commit()
    print("\nContact Command IDs have been reset successfully.")
    cur.execute("SELECT * FROM Contact_Command")
    rows = cur.fetchall()
    print(tabulate(rows, headers=["Id", "Name", "Phone_No", "Email"], tablefmt="grid"))

#=============================Edit Command========================
def Edit_command():
    print("1. System_Command")
    print("2. Web_Command")
    print("3. Contact_Command")
    print("4. Exit")
    ch = input("Enter your choice: ")
    if ch == '1':
        Edit_System_Command()
    elif ch == '2':
        Edit_Web_Command()
    elif ch == '3':
        Edit_Contact_Command()
    elif ch == '4':
        print("You have chosen to exit")
        return
    else:
        print("Invalid choice, please try again.")
        Edit_command()
#=============================Edit System Command========================
def Edit_System_Command():
    print("\n--- Existing System Commands ---")
    cur.execute("SELECT * FROM System_Command")
    rows = cur.fetchall()
    if rows:
        print(tabulate(rows, headers=["Id", "Name", "File_Path"], tablefmt="grid"))
    else:
        print("No commands found in System_Command.")

    id = input("Enter the Id of the command to edit: ")
    name = input("Enter the new name of the command: ")
    file_path = input("Enter the new file path of the command: ")
    query = "UPDATE System_Command SET Name = ?, File_Path = ? WHERE Id = ?"
    cur.execute(query, (name, file_path, id))
    con.commit()
    print("Command edited successfully.")

    print("\n--- Updated System Commands ---")
    cur.execute("SELECT * FROM System_Command")
    rows = cur.fetchall()
    print(tabulate(rows, headers=["Id", "Name", "File_Path"], tablefmt="grid"))
#=============================Edit Web Command========================
def Edit_Web_Command():
    print("\n--- Existing Web Commands ---")
    cur.execute("SELECT * FROM Web_Command")
    rows = cur.fetchall()
    if rows:
        print(tabulate(rows, headers=["Id", "Name", "Url"], tablefmt="grid"))
    else:
        print("No commands found in Web_Command.")

    id = input("Enter the Id of the command to edit: ")
    name = input("Enter the new name of the command: ")
    url = input("Enter the new URL of the command: ")
    query = "UPDATE Web_Command SET Name = ?, Url = ? WHERE Id = ?"
    cur.execute(query, (name, url, id))
    con.commit()
    print("Command edited successfully.")

    print("\n--- Updated Web Commands ---")
    cur.execute("SELECT * FROM Web_Command")
    rows = cur.fetchall()
    print(tabulate(rows, headers=["Id", "Name", "Url"], tablefmt="grid"))

#=============================Edit Contact Command========================

def Edit_Contact_Command():
    print("\n--- Existing Contact Commands ---")
    cur.execute("SELECT * FROM Contact_Command")
    rows = cur.fetchall()
    if rows:
        print(tabulate(rows, headers=["Id", "Name", "Phone_No", "Email"], tablefmt="grid"))
    else:
        print("No commands found in Contact_Command.")
        return

    id = input("Enter the Id of the contact command to edit: ")
    name = input("Enter the new name of the contact: ")
    phone_no = input("Enter the new phone number of the contact: ")
    email = input("Enter the new email of the contact (optional): ")
    query = "UPDATE Contact_Command SET Name = ?, Phone_No = ?, Email = ? WHERE Id = ?"
    cur.execute(query, (name, phone_no, email, id))
    con.commit()
    print("Contact command edited successfully.")

    print("\n--- Updated Contact Commands ---")
    cur.execute("SELECT * FROM Contact_Command")
    rows = cur.fetchall()
    print(tabulate(rows, headers=["Id", "Name", "Phone_No", "Email"], tablefmt="grid"))
    # Bas return karo, Edit_command() call mat karo
    return
#========================Search Command====================
def Search_Command():
    print("Search in:")
    print("1. System_Command")
    print("2. Web_Command")
    print("3. Contact_Command")
    print("4. Exit")
    ch = input("Enter your choice: ").strip()
    if ch == '1':
        Search_System_Command()
    elif ch == '2':
        Search_Web_Command()
    elif ch == '3':
        Search_Contact_Command()
    elif ch == '4':
        print("You have chosen to exit")
        return
    else:
        print("Invalid choice, please try again.")
        Search_Command()
#===================Search_System_Command========================
def Search_System_Command():
    keyword = input("Enter keyword to search in System Commands (Name/File_Path): ").strip()
    cur.execute("SELECT * FROM System_Command WHERE Name LIKE ? OR File_Path LIKE ?", (f"%{keyword}%", f"%{keyword}%"))
    rows = cur.fetchall()
    if rows:
        print(tabulate(rows, headers=["Id", "Name", "File_Path"], tablefmt="grid"))
    else:
        print("No matching System Commands found.")
#===============Search_Contact_Command================================
def Search_Web_Command():
    keyword = input("Enter keyword to search in Web Commands (Name/Url): ").strip()
    cur.execute("SELECT * FROM Web_Command WHERE Name LIKE ? OR Url LIKE ?", (f"%{keyword}%", f"%{keyword}%"))
    rows = cur.fetchall()
    if rows:
        print(tabulate(rows, headers=["Id", "Name", "Url"], tablefmt="grid"))
    else:
        print("No matching Web Commands found.")
#===============Search_Web_Command==============================
def Search_Contact_Command():
    keyword = input("Enter keyword to search in Contacts (Name/Phone/Email): ").strip()
    cur.execute("SELECT * FROM Contact_Command WHERE Name LIKE ? OR Phone_No LIKE ? OR Sec_Phone_No LIKE ? OR Email LIKE ?", 
                (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
    rows = cur.fetchall()
    if rows:
        print(tabulate(rows, headers=["Id", "Name", "Phone_No", "Sec_Phone_No", "Email"], tablefmt="grid"))
    else:
        print("No matching Contacts found.")
menu()