def main_menu():
    print("\nMenu:")
    print("________________________\n")
    print("1| Option 1      ")
    print("2| Option 2")
    print("3| Option 3")
    print("4| Exit                ")
    print("________________________\n")

    

def option1():
    print("You've selected Option 1")
    # Add functionality for Option 1 here

def option2():
    print("You've selected Option 2")
    # Add functionality for Option 2 here

def option3():
    print("You've selected Option 3")
    # Add functionality for Option 3 here

def run_menu():
    while True:
        main_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            option1()
        elif choice == '2':
            option2()
        elif choice == '3':
            option3()
        elif choice == '4':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    run_menu()
