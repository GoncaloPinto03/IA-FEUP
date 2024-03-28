import algorithms
import book
import library
import datetime

def get_elapsed_time(t):
    return datetime.datetime.now() - t

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

def read_input_file(input_file):
    with open(input_file, 'r') as file:
        # Read the first line
        B, L, D = map(int, file.readline().strip().split())
        
        # Read the second line to get scores of individual books
        book_scores = list(map(int, file.readline().strip().split()))

        # Read library information
        libraries = []
        for _ in range(L):
            Nj, Tj, Mj = map(int, file.readline().strip().split())
            books_in_library = list(map(int, file.readline().strip().split()))
            books = [book.Book(book_id, book_scores[book_id]) for book_id in books_in_library]
            libraries.append(library.Library(_, books, Tj, Mj))

        return B, L, D, book_scores, libraries


# select file function
def selectFile():
    while True:
        drawSelectFile()
        choice = input("\nEnter your choice: ")
        files = ["./dataset/a_example.txt", "./dataset/b_read_on.txt", "./dataset/c_incunabula.txt", "./dataset/d_tough_choices.txt", "./dataset/e_so_many_books.txt", "./dataset/f_libraries_of_the_world.txt"]
        if choice in map(str, range(1, len(files) + 1)):
            input_file = files[int(choice) - 1]
            print(f"You've selected {input_file}")
            B, L, D, book_scores, libraries = read_input_file(input_file)
            # Now you have all the necessary data, you can use it as required
            # print("Number of books:", B)
            # print("Number of libraries:", L)
            # print("Number of days:", D)
            # print("Book scores:", book_scores)
            # print("Libraries:", libraries)
            # for lib in libraries:
            #     lib.display_details()  # Print details of each library
            # Pass B, L, D, book_scores, libraries to your algorithms if needed
            selectAlgorithm(B, L, D, book_scores, libraries)
        elif choice == '7':
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")

# select algorithm function
def selectAlgorithm(B, L, D, book_scores, libraries):
    while True:
        drawSelectAlgorithm()
        choice = input("\nEnter your choice: ")
        if choice == '1':
            print("You've selected Greedy Algorithm")
            t = datetime.datetime.now()
            score = algorithms.greedy(B, L, D, book_scores, libraries)
            print("\n-----------------------------")
            print("         Solution")
            print("-----------------------------")

            print("Score:", score)  # prints total score
            print("Elapsed Time:", str(get_elapsed_time(t)))  # prints elapsed time
        elif choice == '2':
            print("You've selected Local Search - First Neighbour Algorithm")
            t = datetime.datetime.now()
            score1 = algorithms.ls_first_neighbor(B, L, D, book_scores, libraries)
            score2 = algorithms.greedy(B, L, D, book_scores, libraries)
            print("\n-----------------------------")
            print("         Solution")
            print("-----------------------------")

            print("Score:", score1)  # prints total score
            if score1 > score2:
                print("Found a better solution")
            else:
                print("Did not find a better solution")

            print("Elapsed Time:", str(get_elapsed_time(t)))  # prints elapsed time
            
        elif choice == '3':
            print("You've selected Local Search - Best Neighbour Algorithm")
            t = datetime.datetime.now()
            score1 = algorithms.ls_best_neighbour(B, L, D, book_scores, libraries)
            score2 = algorithms.greedy(B, L, D, book_scores, libraries)
            print("\n-----------------------------")
            print("         Solution")
            print("-----------------------------")

            print("Score:", score1)  # prints total score
            
        elif choice == '4':
            print("You've selected Local Search - Random Neighbour Algorithm")
            t = datetime.datetime.now()
            score1 = algorithms.ls_random_neighbour(B, L, D, book_scores, libraries)
            score2 = algorithms.greedy(B, L, D, book_scores, libraries)
            print("\n-----------------------------")
            print("         Solution")
            print("-----------------------------")

            print("Score:", score1)  # prints total score
            

            print("Elapsed Time:", str(get_elapsed_time(t)))  # prints elapsed time
            
        elif choice == '5':
            print("You've selected Simulated Annealing Algorithm")
            algorithms.simulated_annealing(B, L, D, book_scores, libraries)
        elif choice == '6':
            print("You've selected Genetic Algorithm")
            algorithms.genetic(B, L, D, book_scores, libraries)
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