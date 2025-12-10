import json
import re
import os
from datetime import datetime
import hashlib
import random

class Student:
    """Student data model class"""

    def __init__(self, student_id="", first_name="", last_name="", username="", 
                 password="", email="", phone_number="", address="", 
                 date_of_birth="", gender="", course="", semester="", 
                 father_name="", mother_name="", emergency_contact=""):
        self.student_id = student_id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password
        self.email = email
        self.phone_number = phone_number
        self.address = address
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.course = course
        self.semester = semester
        self.father_name = father_name
        self.mother_name = mother_name
        self.emergency_contact = emergency_contact

    def to_dict(self):
        """Convert student object to dictionary for JSON serialization"""
        return {
            'student_id': self.student_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'password': self.password,
            'email': self.email,
            'phone_number': self.phone_number,
            'address': self.address,
            'date_of_birth': self.date_of_birth,
            'gender': self.gender,
            'course': self.course,
            'semester': self.semester,
            'father_name': self.father_name,
            'mother_name': self.mother_name,
            'emergency_contact': self.emergency_contact
        }

    @classmethod
    def from_dict(cls, data):
        """Create student object from dictionary"""
        return cls(**data)

    def __str__(self):
        return f"Student(ID: {self.student_id}, Name: {self.first_name} {self.last_name}, Username: {self.username})"


class StudentDatabase:
    """Database operations class for managing student data"""

    def __init__(self, filename="students.json"):
        self.filename = filename
        self.students = {}
        self.load_students()

    def load_students(self):
        """Load students from JSON file"""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r') as file:
                    data = json.load(file)
                    for username, student_data in data.items():
                        self.students[username] = Student.from_dict(student_data)
                print(f"✓ Loaded {len(self.students)} students from database")
            else:
                print("✓ Starting with empty database")
        except Exception as e:
            print(f"Error loading students: {e}")
            self.students = {}

    def save_students(self):
        """Save students to JSON file"""
        try:
            data = {}
            for username, student in self.students.items():
                data[username] = student.to_dict()

            with open(self.filename, 'w') as file:
                json.dump(data, file, indent=4)
            return True
        except Exception as e:
            print(f"Error saving students: {e}")
            return False

    def register_student(self, student):
        """Register a new student"""
        if student.username in self.students:
            return False, "Username already exists!"

        # Generate unique student ID
        student.student_id = self.generate_student_id()

        # Hash password for security
        student.password = self.hash_password(student.password)

        self.students[student.username] = student
        if self.save_students():
            return True, "Registration successful!"
        else:
            return False, "Failed to save student data!"

    def authenticate_student(self, username, password):
        """Authenticate student login"""
        if username in self.students:
            stored_password = self.students[username].password
            if self.verify_password(password, stored_password):
                return self.students[username]
        return None

    def update_student(self, username, updated_student):
        """Update student profile"""
        if username in self.students:
            # Keep the original password and student_id
            updated_student.password = self.students[username].password
            updated_student.student_id = self.students[username].student_id
            updated_student.username = username

            self.students[username] = updated_student
            if self.save_students():
                return True, "Profile updated successfully!"
            else:
                return False, "Failed to save updated profile!"
        return False, "Student not found!"

    def username_exists(self, username):
        """Check if username exists"""
        return username in self.students

    def generate_student_id(self):
        """Generate unique student ID"""
        while True:
            student_id = f"STU{random.randint(100000, 999999)}"
            # Check if ID already exists
            exists = any(student.student_id == student_id for student in self.students.values())
            if not exists:
                return student_id

    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password, hashed_password):
        """Verify password against hash"""
        return self.hash_password(password) == hashed_password


class InputValidator:
    """Input validation class for all user inputs"""

    @staticmethod
    def validate_name(name, field_name):
        """Validate name fields"""
        if not name or not name.strip():
            return False, f"{field_name} cannot be empty"
        if not re.match(r'^[a-zA-Z\s]+$', name.strip()):
            return False, f"{field_name} should contain only letters and spaces"
        if len(name.strip()) < 2:
            return False, f"{field_name} should be at least 2 characters long"
        return True, name.strip().title()

    @staticmethod
    def validate_username(username):
        """Validate username"""
        if not username or not username.strip():
            return False, "Username cannot be empty"
        username = username.strip().lower()
        if not re.match(r'^[a-zA-Z0-9_]{3,20}$', username):
            return False, "Username should be 3-20 characters with letters, numbers, and underscores only"
        return True, username

    @staticmethod
    def validate_password(password):
        """Validate password"""
        if not password:
            return False, "Password cannot be empty"
        if len(password) < 6:
            return False, "Password should be at least 6 characters long"
        return True, password

    @staticmethod
    def validate_email(email):
        """Validate email address"""
        if not email or not email.strip():
            return False, "Email cannot be empty"
        email = email.strip().lower()
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return False, "Please enter a valid email address"
        return True, email

    @staticmethod
    def validate_phone(phone):
        """Validate phone number"""
        if not phone or not phone.strip():
            return False, "Phone number cannot be empty"
        phone = phone.strip()
        if not re.match(r'^[0-9]{10}$', phone):
            return False, "Phone number should be exactly 10 digits"
        return True, phone

    @staticmethod
    def validate_date(date_str):
        """Validate date in DD-MM-YYYY format"""
        if not date_str or not date_str.strip():
            return False, "Date cannot be empty"
        date_str = date_str.strip()
        if not re.match(r'^(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[0-2])-\d{4}$', date_str):
            return False, "Date format should be DD-MM-YYYY"

        # Additional validation for actual date
        try:
            day, month, year = map(int, date_str.split('-'))
            datetime(year, month, day)

            # Check if date is not in future
            birth_date = datetime(year, month, day)
            if birth_date > datetime.now():
                return False, "Birth date cannot be in the future"

            # Check reasonable age limits
            age = datetime.now().year - year
            if age > 100 or age < 10:
                return False, "Please enter a reasonable birth date"

            return True, date_str
        except ValueError:
            return False, "Invalid date. Please check day, month, and year"

    @staticmethod
    def validate_gender(gender):
        """Validate gender"""
        if not gender or not gender.strip():
            return False, "Gender cannot be empty"
        gender = gender.strip().upper()
        if gender not in ['M', 'F', 'O']:
            return False, "Gender should be M (Male), F (Female), or O (Other)"
        return True, gender

    @staticmethod
    def validate_semester(semester):
        """Validate semester"""
        if not semester or not semester.strip():
            return False, "Semester cannot be empty"
        semester = semester.strip()
        if not re.match(r'^[1-8]$', semester):
            return False, "Semester should be between 1 and 8"
        return True, semester

    @staticmethod
    def validate_course(course):
        """Validate course"""
        if not course or not course.strip():
            return False, "Course cannot be empty"
        course = course.strip().title()
        if not re.match(r'^[a-zA-Z\s]+$', course):
            return False, "Course should contain only letters and spaces"
        if len(course) < 2:
            return False, "Course name should be at least 2 characters long"
        return True, course


class StudentSystem:
    """Main application class with user interface"""

    def __init__(self):
        self.db = StudentDatabase()
        self.current_student = None
        self.validator = InputValidator()

    def run(self):
        """Main application loop"""
        print("=" * 50)
        print("       STUDENT MANAGEMENT SYSTEM")
        print("=" * 50)

        while True:
            try:
                if self.current_student is None:
                    self.show_main_menu()
                else:
                    self.show_student_menu()
            except KeyboardInterrupt:
                print("\n\n✓ Thank you for using Student Management System!")
                break
            except Exception as e:
                print(f"\nAn error occurred: {e}")
                input("Press Enter to continue...")

    def show_main_menu(self):
        """Show main menu for non-logged-in users"""
        print("\n" + "─" * 30)
        print("         MAIN MENU")
        print("─" * 30)
        print("1. Register New Student")
        print("2. Student Login")
        print("3. Exit")
        print("─" * 30)

        choice = self.get_menu_choice(1, 3)

        if choice == 1:
            self.register_student()
        elif choice == 2:
            self.login_student()
        elif choice == 3:
            self.exit_system()

    def show_student_menu(self):
        """Show menu for logged-in students"""
        print("\n" + "─" * 40)
        print("       STUDENT DASHBOARD")
        print("─" * 40)
        print(f"Welcome, {self.current_student.first_name} {self.current_student.last_name}!")
        print("─" * 40)
        print("1. Show Profile")
        print("2. Update Profile")
        print("3. Logout")
        print("4. Exit")
        print("─" * 40)

        choice = self.get_menu_choice(1, 4)

        if choice == 1:
            self.show_profile()
        elif choice == 2:
            self.update_profile()
        elif choice == 3:
            self.logout()
        elif choice == 4:
            self.exit_system()

    def register_student(self):
        """Register new student"""
        print("\n" + "=" * 40)
        print("      STUDENT REGISTRATION")
        print("=" * 40)
        print("Please fill in all the required information:")
        print("─" * 40)

        try:
            # Get and validate all student information
            first_name = self.get_validated_input("First Name: ", self.validator.validate_name, "First Name")
            last_name = self.get_validated_input("Last Name: ", self.validator.validate_name, "Last Name")

            # Username validation with uniqueness check
            while True:
                username = self.get_validated_input("Username: ", self.validator.validate_username)
                if not self.db.username_exists(username):
                    break
                print("✗ Username already exists! Please choose another.")

            password = self.get_validated_input("Password: ", self.validator.validate_password)
            email = self.get_validated_input("Email: ", self.validator.validate_email)
            phone_number = self.get_validated_input("Phone Number: ", self.validator.validate_phone)

            print("Address: ", end="")
            address = input().strip()
            while not address:
                print("✗ Address cannot be empty")
                print("Address: ", end="")
                address = input().strip()

            date_of_birth = self.get_validated_input("Date of Birth (DD-MM-YYYY): ", self.validator.validate_date)
            gender = self.get_validated_input("Gender (M/F/O): ", self.validator.validate_gender)
            course = self.get_validated_input("Course: ", self.validator.validate_course)
            semester = self.get_validated_input("Semester (1-8): ", self.validator.validate_semester)
            father_name = self.get_validated_input("Father's Name: ", self.validator.validate_name, "Father's Name")
            mother_name = self.get_validated_input("Mother's Name: ", self.validator.validate_name, "Mother's Name")
            emergency_contact = self.get_validated_input("Emergency Contact: ", self.validator.validate_phone)

            # Create new student
            new_student = Student(
                first_name=first_name, last_name=last_name, username=username,
                password=password, email=email, phone_number=phone_number,
                address=address, date_of_birth=date_of_birth, gender=gender,
                course=course, semester=semester, father_name=father_name,
                mother_name=mother_name, emergency_contact=emergency_contact
            )

            # Register student
            success, message = self.db.register_student(new_student)

            if success:
                print("\n" + "✓" * 50)
                print("         REGISTRATION SUCCESSFUL!")
                print("✓" * 50)
                print(f"Your Student ID: {new_student.student_id}")
                print("Please note down your Student ID for future reference.")
                print("You can now login with your username and password.")
            else:
                print(f"\n✗ Registration failed: {message}")

            input("\nPress Enter to continue...")

        except KeyboardInterrupt:
            print("\n✗ Registration cancelled.")
            input("Press Enter to continue...")

    def login_student(self):
        """Login student"""
        print("\n" + "=" * 30)
        print("       STUDENT LOGIN")
        print("=" * 30)

        try:
            print("Username: ", end="")
            username = input().strip().lower()
            print("Password: ", end="")
            password = input()

            student = self.db.authenticate_student(username, password)

            if student:
                self.current_student = student
                print("\n✓ Login successful!")
                print(f"Welcome back, {student.first_name}!")
            else:
                print("\n✗ Invalid username or password!")

            input("Press Enter to continue...")

        except KeyboardInterrupt:
            print("\n✗ Login cancelled.")
            input("Press Enter to continue...")

    def show_profile(self):
        """Show student profile"""
        print("\n" + "=" * 50)
        print("           STUDENT PROFILE")
        print("=" * 50)

        s = self.current_student
        print(f"Student ID      : {s.student_id}")
        print(f"Name           : {s.first_name} {s.last_name}")
        print(f"Username       : {s.username}")
        print(f"Email          : {s.email}")
        print(f"Phone          : {s.phone_number}")
        print(f"Address        : {s.address}")
        print(f"Date of Birth  : {s.date_of_birth}")
        print(f"Gender         : {s.gender}")
        print(f"Course         : {s.course}")
        print(f"Semester       : {s.semester}")
        print(f"Father's Name  : {s.father_name}")
        print(f"Mother's Name  : {s.mother_name}")
        print(f"Emergency Contact: {s.emergency_contact}")
        print("=" * 50)

        input("Press Enter to continue...")

    def update_profile(self):
        """Update student profile"""
        print("\n" + "=" * 40)
        print("        UPDATE PROFILE")
        print("=" * 40)
        print("Leave blank to keep current value")
        print("─" * 40)

        try:
            s = self.current_student
            updated_student = Student()

            # Copy current values
            updated_student.first_name = s.first_name
            updated_student.last_name = s.last_name
            updated_student.email = s.email
            updated_student.phone_number = s.phone_number
            updated_student.address = s.address
            updated_student.course = s.course
            updated_student.semester = s.semester
            updated_student.emergency_contact = s.emergency_contact

            # Update fields
            new_value = self.get_optional_input(f"First Name ({s.first_name}): ", 
                                              self.validator.validate_name, "First Name")
            if new_value:
                updated_student.first_name = new_value

            new_value = self.get_optional_input(f"Last Name ({s.last_name}): ", 
                                              self.validator.validate_name, "Last Name")
            if new_value:
                updated_student.last_name = new_value

            new_value = self.get_optional_input(f"Email ({s.email}): ", 
                                              self.validator.validate_email)
            if new_value:
                updated_student.email = new_value

            new_value = self.get_optional_input(f"Phone ({s.phone_number}): ", 
                                              self.validator.validate_phone)
            if new_value:
                updated_student.phone_number = new_value

            print(f"Address ({s.address}): ", end="")
            new_address = input().strip()
            if new_address:
                updated_student.address = new_address

            new_value = self.get_optional_input(f"Course ({s.course}): ", 
                                              self.validator.validate_course)
            if new_value:
                updated_student.course = new_value

            new_value = self.get_optional_input(f"Semester ({s.semester}): ", 
                                              self.validator.validate_semester)
            if new_value:
                updated_student.semester = new_value

            new_value = self.get_optional_input(f"Emergency Contact ({s.emergency_contact}): ", 
                                              self.validator.validate_phone)
            if new_value:
                updated_student.emergency_contact = new_value

            # Update in database
            success, message = self.db.update_student(s.username, updated_student)

            if success:
                self.current_student = updated_student
                print(f"\n✓ {message}")
            else:
                print(f"\n✗ Update failed: {message}")

            input("Press Enter to continue...")

        except KeyboardInterrupt:
            print("\n✗ Update cancelled.")
            input("Press Enter to continue...")

    def logout(self):
        """Logout current student"""
        print(f"\n✓ Goodbye, {self.current_student.first_name}!")
        self.current_student = None
        input("Press Enter to continue...")

    def exit_system(self):
        """Exit the system"""
        print("\n" + "✓" * 50)
        print("  Thank you for using Student Management System!")
        print("                Goodbye!")
        print("✓" * 50)
        exit()

    def get_menu_choice(self, min_choice, max_choice):
        """Get valid menu choice from user"""
        while True:
            try:
                print(f"Enter your choice ({min_choice}-{max_choice}): ", end="")
                choice = int(input())
                if min_choice <= choice <= max_choice:
                    return choice
                else:
                    print(f"✗ Please enter a number between {min_choice} and {max_choice}")
            except ValueError:
                print("✗ Please enter a valid number")
            except KeyboardInterrupt:
                print("\n✗ Operation cancelled.")
                return max_choice  # Return exit option

    def get_validated_input(self, prompt, validator, *args):
        """Get validated input from user"""
        while True:
            try:
                print(prompt, end="")
                value = input()
                if args:
                    is_valid, result = validator(value, *args)
                else:
                    is_valid, result = validator(value)

                if is_valid:
                    return result
                else:
                    print(f"✗ {result}")
            except KeyboardInterrupt:
                print("\n✗ Input cancelled.")
                raise

    def get_optional_input(self, prompt, validator, *args):
        """Get optional validated input (can be empty)"""
        try:
            print(prompt, end="")
            value = input().strip()
            if not value:
                return None

            if args:
                is_valid, result = validator(value, *args)
            else:
                is_valid, result = validator(value)

            if is_valid:
                return result
            else:
                print(f"✗ {result}")
                return None
        except KeyboardInterrupt:
            print("\n✗ Input cancelled.")
            return None


def main():
    """Main function to run the Student Management System"""
    try:
        system = StudentSystem()
        system.run()
    except Exception as e:
        print(f"Fatal error: {e}")
        print("Application terminated.")


if __name__ == "__main__":
    main()
