# algorithms.py
import copy
import random

def greedy2(B, L, D, book_scores, libraries):
    # Implement the Greedy algorithm
    day = 0
    solution = [-1 for i in range(D)]
    scanned_books_set = set()
    scanned_books_dict = dict()
    all_libraries = copy.deepcopy(libraries)

    while day < D and len(all_libraries) > 0:
        lib_id, books = choose_best_score(D - day, all_libraries, book_scores, scanned_books_set)  # gets the best library to sign up
        if lib_id == -1:
            break
        lib = libraries[lib_id]
        scanned_books_dict[lib_id] = books
        scanned_books_set.update(books)
        for _ in range(lib.signup_days):  # stores in the solution the chosen library
            solution[day] = lib_id
            day += 1

        all_libraries = [l for l in all_libraries if l.id != lib.id]  # removes chosen library from the list of available libraries

    while len(solution) < D:
        solution.append(-1)

    return solution, score(scanned_books_set, book_scores), scanned_books_dict


def greedy(B, L, D, book_scores, libraries):

    # Sort libraries based on a heuristic: a ratio of the total score of books to the signup time.
    for library in libraries:
        library.sort_books()  # Sort books in each library based on scores
    libraries.sort(key=lambda lib: sum(book.score for book in lib.books) / lib.signup_days, reverse=True)

    # Days remaining to sign up libraries and scan books
    days_remaining = D
    signup_process = []  # To keep track of the signup process
    books_scanned = set()  # To keep track of the books that have been scanned
    total_score = 0  # Initialize total score

    # Loop through each library and determine if it can be signed up within the remaining days
    for library in libraries:
        if days_remaining <= 0 or days_remaining < library.signup_days:
            break  # No more days left to sign up new libraries
        days_remaining -= library.signup_days
        
        # Calculate the number of books that can be scanned from this library
        books_to_scan = []
        for book in library.books:
            if len(books_to_scan) < days_remaining * library.books_per_day and book.id not in books_scanned:
                books_to_scan.append(book)
                books_scanned.add(book.id)
                total_score += book.score
        signup_process.append((library, books_to_scan))

    '''
    # Write the results to the output file
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_path = f'proj/output/{base_name}_greedy.txt'
    with open(output_path, 'w') as file:
        # Write the number of libraries to sign up
        file.write(f"{len(signup_process)}\n")
        for library, books in signup_process:
        # Write the library ID and the number of books to scan
            file.write(f"{library.id} {len(books)}\n")
            # Write the book IDs in the order they are scanned
            book_ids = ' '.join(str(book.id) for book in books)
            file.write(book_ids + "\n")

    '''
    return total_score

def ls_first_neighbour(B, L, D, book_scores, libraries):
    # Implement the Local Search - First Neighbour algorithm
    pass

def ls_best_neighbour(B, L, D, book_scores, libraries):
    # Implement the Local Search - Best Neighbour algorithm
    pass

def ls_random_neighbour(B, L, D, book_scores, libraries):
    # Implement the Local Search - Random Neighbour algorithm
    pass

def simulated_annealing(B, L, D, book_scores, libraries):
    # Implement the Simulated Annealing algorithm
    pass

def bestScores():
    # Implement the best scores algorithm
    pass

# calculates the total score of the libraries
def score(books, scores):
    return sum([scores[b] for b in books])

# given a list of libraries, number of remaining days and the books already scanned, finds the best library to sign up (compares scores)
def choose_best_score(days, libraries, scores, scanned_books):
    best_score = 0
    best_books = []
    best_lib = None
    for library in libraries:
        if library.signup_days > days:
            continue
        books = library.get_books_to_send(days, scanned_books)
        if books is None:   # all books are already scanned
            print(f"Books for library {library.id} is None!")
        s = score(books, scores) / library.signup_days
        if s > best_score:
            best_lib = library.id
            best_score = s
            best_books = books

    if best_lib is None:
        return -1, best_books

    return best_lib, best_books


# def genetic(B, L, D, book_scores, libraries):
#     # Implement the Genetic algorithm
#     pass

#--------------------------------------------------------------------------------------
def genetic(population, book_scores, libraries, mutation_prob, swap_prob, population_variation):
    # Implement the Genetic algorithm
    pass

# call this function in menu
def genetic_options(book_scores, libraries, option):
    options = {1: "Use default values", 2: "Personalized values"}
    message = "\nGenetic algorithm uses default values.\nDo you want to continue with the default ones or do you want to personalize the values?\n"
    print(message)
    
    while True:
        for k, v in options.items():
            print(str(k) + "| " + v)
            
        choice = int(input("\nChoose the values to use in genetic algorithm: "))
        if (choice == 1): 
            # call genetic algorithm with default values
            population_size, generations, mutation_prob, swap_prob, population_variation = get_parameters_for_ga(option)
            return genetic(population_size, book_scores, libraries, mutation_prob, swap_prob, population_variation)

        elif (choice == 2):
            # call genetic algorithm with personalized values
            population_size = personalized_input_for_ga("\nPopulation Size: ", population_size, True, 6, 100)
            generations = personalized_input_for_ga("\nNumber of Generations: ", generations, True, 10, 1000)
            mutation_prob = personalized_input_for_ga("\nMutation Probability: ", mutation_prob, False, 0, 1)
            swap_prob = personalized_input_for_ga("\nSwap Probability: ", swap_prob, False, 0, 1)
            population_variation = personalized_input_for_ga("\nPopulation Variation: ", population_variation, False, 0, 1)
            return genetic(population_size, book_scores, libraries, mutation_prob, swap_prob, population_variation)
        else: 
            print("Invalid option. Choose a valid one.\n")
        
            
def personalized_input_for_ga(value, default_value, is_int, min_value, max_value):
    user_value = input(value + "(default = )" + str(default_value) + ":" )
    
    while True:
        user_value = int(user_value) if is_int else float(user_value)
                
        if user_value < min_value or user_value > max_value:
            user_value = input("Invalid input, please insert a valid one (min: " + str(min_value) + ", max: " + str(max_value) + "): ")
        else:
            break

    return user_value

# function that given an input file returns the values for population size, number of generations, mutation and swap
# probabilities and population variation
def get_parameters_for_ga(option):
    population_size = 50        # "./dataset/a_example.txt"
    generations = 1000
    mutation_prob = 0.2
    swap_prob = 0.2
    population_variation = 0.2

    # all the below values were chosen after a battery of tests
    if option == 2:             # "./dataset/b_read_on.txt"
        population_size = 50
        generations = 1000
        mutation_prob = 0.2
        swap_prob = 0.2
        population_variation = 0.2
        
    elif option == 3:           # "./dataset/c_incunabula.txt"
        population_size = 10
        generations = 10
        mutation_prob = 0.05
        swap_prob = 0.05
        population_variation = 0.01
        
    elif option == 4:           # "./dataset/d_tough_choices.txt"
        population_size = 10
        generations = 10
        mutation_prob = 0.05
        swap_prob = 0.05
        population_variation = 0.001
        
    elif option == 5:           # "./dataset/e_so_many_books.txt"
        population_size = 20
        generations = 500
        mutation_prob = 0.2
        swap_prob = 0.2
        population_variation = 0.2
        
    elif option == 6:           # "./dataset/f_libraries_of_the_world.txt"
        population_size = 20
        generations = 100
        mutation_prob = 0.2
        swap_prob = 0.2
        population_variation = 0.2

    return population_size, generations, mutation_prob, swap_prob, population_variation
    