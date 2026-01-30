import random

def select_difficulty():
    print("1. Easy (1 - 50)")
    print("2. Medium (1 - 100)")
    print("3. Hard (1 - 500)")
    
    choice = input("Select difficulty (1-3): ")
    
    if choice == "1":
        return 50
    elif choice == "3":
        return 500
    else:
        return 100

def play_game(max_range):
    target = random.randint(1, max_range)
    attempts = 0
    
    print(f"I have picked a number between 1 and {max_range}.")

    while True:
        user_input = input("Enter your guess: ")
        
        if not user_input.isdigit():
            print("Invalid input. Please enter a number.")
            continue
            
        guess = int(user_input)
        attempts += 1
        
        if guess < target:
            print("Higher")
        elif guess > target:
            print("Lower")
        else:
            print(f"Correct! You found the number in {attempts} attempts.")
            return attempts

def main():
    best_score = float('inf')
    
    while True:
        print("--- Number Guessing Game ---")
        if best_score != float('inf'):
            print(f"Best Score (Fewest Attempts): {best_score}")
            
        limit = select_difficulty()
        current_score = play_game(limit)
        
        if current_score < best_score:
            best_score = current_score
            print("New Record Set!")
            
        replay = input("Do you want to play again? (yes/no): ")
        if replay.lower() != "yes":
            break

if __name__ == "__main__":
    main()