import json
import os

class Student:
    def __init__(self, name, student_id, grade):
        self.name = name
        self.student_id = student_id
        self.grade = grade

    def to_dict(self):
        return {
            'name': self.name,
            'id': self.student_id,
            'grade': self.grade
        }

    @staticmethod
    def from_dict(data):
        return Student(data['name'], data['id'], data['grade'])

class StudentManager:
    def __init__(self, filename='students.json'):
        self.filename = filename
        self.students = self.load_students()

    def load_students(self):
        if not os.path.exists(self.filename):
            return []
        with open(self.filename, 'r') as f:
            try:
                data = json.load(f)
                return [Student.from_dict(s) for s in data]
            except json.JSONDecodeError:
                return []

    def save_students(self):
        with open(self.filename, 'w') as f:
            json.dump([s.to_dict() for s in self.students], f, indent=2)

    def add_student(self, name, student_id, grade):
        if any(s.student_id == student_id for s in self.students):
            print(f"Error: Student ID '{student_id}' already exists.")
            return False
        student = Student(name, student_id, grade)
        self.students.append(student)
        self.save_students()
        print(f"Student '{name}' added.")
        return True

    def update_student(self, student_id, name=None, grade=None):
        for s in self.students:
            if s.student_id == student_id:
                if name:
                    s.name = name
                if grade:
                    s.grade = grade
                self.save_students()
                print(f"Student ID '{student_id}' updated.")
                return True
        print(f"Error: Student ID '{student_id}' not found.")
        return False

    def delete_student(self, student_id):
        for i, s in enumerate(self.students):
            if s.student_id == student_id:
                del self.students[i]
                self.save_students()
                print(f"Student ID '{student_id}' deleted.")
                return True
        print(f"Error: Student ID '{student_id}' not found.")
        return False

    def list_students(self):
        if not self.students:
            print("No student records found.")
            return
        print("{:<10} {:<20} {:<10}".format("ID", "Name", "Grade"))
        print("-"*40)
        for s in self.students:
            print("{:<10} {:<20} {:<10}".format(s.student_id, s.name, s.grade))


def main():
    manager = StudentManager()
    while True:
        print("\nStudent Record Manager")
        print("1. Add Student")
        print("2. Update Student")
        print("3. Delete Student")
        print("4. List Students")
        print("5. Exit")
        choice = input("Select an option (1-5): ")
        if choice == '1':
            name = input("Enter name: ")
            student_id = input("Enter ID: ")
            grade = input("Enter grade: ")
            manager.add_student(name, student_id, grade)
        elif choice == '2':
            student_id = input("Enter ID to update: ")
            name = input("Enter new name (leave blank to keep): ")
            grade = input("Enter new grade (leave blank to keep): ")
            manager.update_student(student_id, name if name else None, grade if grade else None)
        elif choice == '3':
            student_id = input("Enter ID to delete: ")
            manager.delete_student(student_id)
        elif choice == '4':
            manager.list_students()
        elif choice == '5':
            print("Exiting.")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()
