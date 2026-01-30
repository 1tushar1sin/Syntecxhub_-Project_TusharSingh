import json
import os

FILE_NAME = "tasks.json"

def load_tasks():
    if not os.path.exists(FILE_NAME):
        return []
    try:
        with open(FILE_NAME, 'r') as file:
            return json.load(file)
    except (json.JSONDecodeError, IOError):
        return []

def save_tasks(tasks):
    try:
        with open(FILE_NAME, 'w') as file:
            json.dump(tasks, file, indent=4)
    except IOError:
        print("Error saving tasks to file.")

def add_task(tasks):
    title = input("Enter task title: ").strip()
    if not title:
        print("Task title cannot be empty.")
        return

    due_date = input("Enter due date (YYYY-MM-DD) or leave blank: ").strip()
    tags_input = input("Enter tags (comma separated) or leave blank: ").strip()
    
    tags = [t.strip() for t in tags_input.split(",")] if tags_input else []

    task = {
        "title": title,
        "done": False,
        "due_date": due_date,
        "tags": tags
    }
    
    tasks.append(task)
    save_tasks(tasks)
    print("Task added.")

def view_tasks(tasks):
    print("\n--- Current Tasks ---")
    if not tasks:
        print("No tasks found.")
    else:
        for index, task in enumerate(tasks):
            status = "[x]" if task["done"] else "[ ]"
            date_str = f" (Due: {task['due_date']})" if task["due_date"] else ""
            tags_str = f" [Tags: {', '.join(task['tags'])}]" if task["tags"] else ""
            print(f"{index + 1}. {status} {task['title']}{date_str}{tags_str}")
    print("---------------------")

def delete_task(tasks):
    view_tasks(tasks)
    if not tasks:
        return

    try:
        idx = int(input("Enter number to delete: ")) - 1
        if 0 <= idx < len(tasks):
            removed = tasks.pop(idx)
            save_tasks(tasks)
            print(f"Deleted: {removed['title']}")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")

def mark_done(tasks):
    view_tasks(tasks)
    if not tasks:
        return

    try:
        idx = int(input("Enter number to mark done: ")) - 1
        if 0 <= idx < len(tasks):
            tasks[idx]["done"] = True
            save_tasks(tasks)
            print("Task marked as done.")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")

def main():
    tasks = load_tasks()
    
    while True:
        print("\nTodo List Menu")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Mark Task Done")
        print("4. Delete Task")
        print("5. Exit")
        
        choice = input("Choose option (1-5): ").strip()
        
        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            view_tasks(tasks)
        elif choice == "3":
            mark_done(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()