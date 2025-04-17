from Game import snake_and_the_ladder
from jumping_square_game import flappy
from math_game import math_quiz

def menu():
    while True:
        print("\nWelcome! Please select an option:")
        print("[S] To play Snake and the ladder")
        print("[F] To play Jumping Square")
        print("[M] To play Math Quiz")
        print("[] To play")
        print("[E] To Exit\n")

        choice = input("Enter your choice: \n").upper()
        match choice:
            case 'S':
                snake_and_the_ladder()
            case 'F':
                flappy()
            case 'M':
                math_quiz()
            case 'E':
                print("Goodbye!")
                break
            case _:
                print("Invalid choice! Please choose a valid option from the menu.")

menu()