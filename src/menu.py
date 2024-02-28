import algorithms

# draw main menu function
def drawMainMenu():
    print("\nMenu:")
    print("________________________\n")
    print("1| Scan books from a file")
    print("2| Best score for each file")
    print("3| Credits")
    print("4| Exit")
    print("________________________\n")

# draw select file menu function
def drawSelectFile():
    print("\nSelect a file:")
    print("________________________\n")
    print("1| a_example.txt")
    print("2| b_read_on.txt")
    print("3| c_incunabula.txt")
    print("4| d_tough_choices.txt")
    print("5| e_so_many_books.txt")
    print("6| f_libraries_of_the_world.txt")
    print("7| Go back")
    print("________________________\n")

# draw select algorithm menu function
def drawSelectAlgorithm():
    print("\nSelect Algorithm:")
    print("________________________\n")
    print("1| Greedy")
    print("2| Local Search - First Neighbour")
    print("3| Local Search - Best Neighbour")
    print("4| Local Search - Random Neighbour")
    print("5| Simulated Annealing")
    print("6| Genetic")
    print("7| Go back")
    print("________________________\n")

# select file function
def selectFile():
    while True:
        drawSelectFile()
        choice = input("\nEnter your choice: ")
        if choice == '1':
            print("You've selected a_example.txt")
            selectAlgorithm("a_example.txt")
        elif choice == '2':
            print("You've selected b_read_on.txt")
            selectAlgorithm("b_read_on.txt")
        elif choice == '3':
            print("You've selected c_incunabula.txt")
            selectAlgorithm("c_incunabula.txt")
        elif choice == '4':
            print("You've selected d_tough_choices.txt")
            selectAlgorithm("d_tough_choices.txt")
        elif choice == '5':
            print("You've selected e_so_many_books.txt")
            selectAlgorithm("e_so_many_books.txt")
        elif choice == '6':
            print("You've selected f_libraries_of_the_world.txt")
            selectAlgorithm("f_libraries_of_the_world.txt")
        elif choice == '7':
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")

# select algorithm function
def selectAlgorithm(input_file):
    while True:
        drawSelectAlgorithm()
        choice = input("\nEnter your choice: ")
        if choice == '1':
            print("You've selected Greedy Algorithm")
            algorithms.greedy(input_file)
        elif choice == '2':
            print("You've selected Local Search - First Neighbour Algorithm")
            algorithms.ls_first_neighbour(input_file)
        elif choice == '3':
            print("You've selected Local Search - Best Neighbour Algorithm")
            algorithms.ls_best_neighbour(input_file)
        elif choice == '4':
            print("You've selected Local Search - Random Neighbour Algorithm")
            algorithms.ls_random_neighbour(input_file)
        elif choice == '5':
            print("You've selected Simulated Annealing Algorithm")
            algorithms.simulated_annealing(input_file)
        elif choice == '6':
            print("You've selected Genetic Algorithm")
            algorithms.genetic(input_file)
        elif choice == '7':
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")


def option2():
    print("You've selected Option 2")
    # Add functionality for Option 2 here

# credits function
def credits():
    print("Artificial Intelligence Project 1 - LEIC - FEUP")
    print("Gonçalo Pinto  - up202108693@up.pt")
    print("Gonçalo Santos - up202108839@up.pt")
    print("Rui Carvalho   - up202108807@up.pt")

# run main menu function
def runMainMenu():
    while True:
        drawMainMenu()
        choice = input("Enter your choice: ")

        if choice == '1':
            selectFile()
        elif choice == '2':
            algorithms.bestScores()
        elif choice == '3':
            credits()
        elif choice == '4':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    runMainMenu()
