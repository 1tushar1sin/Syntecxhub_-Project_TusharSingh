def is_input_valid(expression):
    valid_chars = "0123456789.+-*/ "
    for char in expression:
        if char not in valid_chars:
            return False
    return True

def calculate_expression(expression):
    if not is_input_valid(expression):
        return " invalid operator detected, can't perform calculation"

    try:
        return eval(expression)
    except ZeroDivisionError:
        return "Error: Division by zero is not allowed"
    except Exception:
        return "Error: Invalid calculation format"

def show_menu():
    print("")
    print("Calculator Menu")
    print("Supported Operators: +, -, *, /")
    print("")


import msvcrt

def run():
    show_menu()
    while True:
        user_input = input("Enter calculation (e.g. 23+26*7/2): ")

        if user_input.lower() == "exit":
            break
        if user_input.strip() == "":
            continue

        result = calculate_expression(user_input)
        print("Result:", result)
        print("new calculation (Press Enter for new calculation, Esc to exit)")

        while True:
            key = msvcrt.getch()
            if key == b'\r':
                break
            elif key == b'\x1b':
                print("Exiting calculator.")
                return

if __name__ == "__main__":
    run()