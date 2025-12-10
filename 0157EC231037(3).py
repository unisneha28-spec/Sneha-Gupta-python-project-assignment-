import sys
import hashlib

students = {}
logged_in_user = None

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_student():
    print("\n--- Student Registration ---")
    while True:
        username = input("Enter Username (required): ").strip()
        if not username or username in students:
            print("Username invalid or already taken.")
            continue
        break
        
    password = input("Create Password: ")
    hashed_password = hash_password(password)
    
    details = {
        'password': hashed_password,
        'enrollment': input("Enrollment No (1): "),
        'first_name': input("First Name (2): "),
        'last_name': input("Last Name (3): "),
        'email': input("Email (4): "),
        'phone': input("Contact Number (5): "),
        'branch': input("Branch (6): "),
        'year': input("Academic Year (7): "),
        'dob': input("Date of Birth (8): "),
        'address': input("Address (9): "),
        'gpa': input("Current GPA (10): ")
    }

    students[username] = details
    print(f"\nRegistration successful for {details['first_name']}!")

def login():
    global logged_in_user
    if logged_in_user:
        print(f"\nAlready logged in as {logged_in_user}.")
        return

    print("\n--- Login ---")
    username = input("Username: ")
    password = input("Password: ")
    hashed_pw = hash_password(password)

    if username in students and students[username]['password'] == hashed_pw:
        logged_in_user = username
        print(f"\nWelcome, {students[username]['first_name']}!")
    else:
        print("\nInvalid username or password.")

def show_profile():
    if not logged_in_user:
        print("\nPlease log in first.")
        return

    profile = students[logged_in_user]
    print(f"\n--- Student Profile: {profile['first_name']} {profile['last_name']} ---")
    
    for key, value in profile.items():
        if key != 'password':
            print(f"{key.replace('_', ' ').title():<15}: {value}")
    print("----------------------------")

def update_profile():
    if not logged_in_user:
        print("\nPlease log in first.")
        return

    profile = students[logged_in_user]
    print("\n--- Update Profile ---")
    print("Updatable fields: 1. Email, 2. Phone, 3. Address, 4. Password")
    
    field_map = {'1': 'email', '2': 'phone', '3': 'address', '4': 'password'}
    
    choice = input("Enter number of the field to update (or '0' to cancel): ").strip()

    if choice == '0':
        return

    field = field_map.get(choice)
    if field:
        new_value = input(f"Enter new {field.title()}: ")
        
        if field == 'password':
            profile[field] = hash_password(new_value)
        else:
            profile[field] = new_value
        
        print(f"\n{field.title()} updated successfully!")
    else:
        print("\nInvalid choice.")

def logout():
    global logged_in_user
    if logged_in_user:
        print(f"\nLogged out {logged_in_user}.")
        logged_in_user = None
    else:
        print("\nYou are not currently logged in.")

def exit_system():
    print("\n--- Exiting System ---")
    print("Goodbye!")
    sys.exit()
def main():
    while True:
        print("\n=== Simple Student Manager ===")
        
        if logged_in_user:
            print(f"Status: Logged in as {logged_in_user}")
            print("1. Show Profile")
            print("2. Update Profile")
            print("3. Logout")
            print("4. Exit")
            
            choice = input("Enter your choice: ")
            
            if choice == '1': show_profile()
            elif choice == '2': update_profile()
            elif choice == '3': logout()
            elif choice == '4': exit_system()
            else: print("Invalid choice.")
        else:
            print("Status: Logged Out")
            print("1. Registration")
            print("2. Login")
            print("3. Exit")
            
            choice = input("Enter your choice: ")
            
            if choice == '1': register_student()
            elif choice == '2': login()
            elif choice == '3': exit_system()
            else: print("Invalid choice.")

if __name__ == "__main__":
    main()