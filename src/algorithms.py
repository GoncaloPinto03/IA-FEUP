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
def genetic(book_scores, libraries, D, population_size, num_generations, mutation_prob, swap_prob, population_variation):
    # Implement the Genetic algorithm
    # 1. initialize population (w/ greedy)
    # 2. traverse generations and populations 
    # 3. select parents
    # 4. crossover
    # 5. mutate
    # 6. calculate best solution
    
    population = initialize_population(population_size, len(libraries))
    
    for i in range(num_generations):
        new_population = []
        for _ in range(population_size):
            parents = select_parents(population, 2, D, book_scores, libraries)
            offspring = crossover(parents)
            offspring = mutate(offspring, mutation_prob, swap_prob)
            new_population.append(offspring)
            print(f"Generation {i + 1} of {num_generations} - Best score: {choose_best_score(D, libraries, book_scores, offspring)}")
        population = new_population

    best_solution = max(population, key=lambda x: choose_best_score(D, libraries, book_scores, x))
    best_score = choose_best_score(D, libraries, book_scores, best_solution)
    
    return best_score

def mutate(solution, mutation_rate, swap_rate):
    if random.random() < mutation_rate:
        i1, i2 = random.sample(range(len(solution)), 2)
        i1, i2 = mutate_swap(i1, i2, swap_rate)
        solution[i1], solution[i2] = solution[i2], solution[i1]
        
    return solution

def mutate_swap(i1, i2, swap_rate):
    if random.random() < swap_rate: 
        i1, i2 = i2, i1
        
    return i1, i2

def crossover(parents):
    crossover_point = random.randint(1, len(parents[0]) - 1)
    offspring = parents[0][:crossover_point] + [gene for gene in parents[1] if gene not in parents[0][:crossover_point]]
    
    return offspring

def initialize_population(population_size, num_libraries):
    population = []
    for _ in range(population_size):
        solution = random.sample(range(num_libraries), num_libraries)
        population.append(solution)
    
    return population

def select_parents(population, num_parents, D, book_scores, libraries):
    parents = []
    population_size = len(population)
    
    for _ in range(num_parents):
        tournament_size = min(5, population_size)
        tournament = random.sample(population, tournament_size)
        winner = max(tournament, key=lambda x: choose_best_score(D, libraries, book_scores, x))
        parents.append(winner)
        
    return parents

def choose_best_score(D, libraries, book_scores, solution):
    total_score = 0
    scanned_books = set()  # Keep track of scanned books to avoid counting duplicates
    day = 0  # Initialize the day counter

    # Iterate through libraries in the solution
    for library_index in solution:
        library = libraries[library_index]
        signup_days = library.get_signup_days()

        # Update the day counter after accounting for library signup time
        day += signup_days

        if day >= D:
            break  # Stop processing if the signup time exceeds the available days

        remaining_days = D - day  # Calculate remaining days after signup

        # Determine the number of books that can be scanned from this library within remaining days
        books_to_scan = min(remaining_days * library.get_books_per_day(), len(library.books))

        # Iterate through books in the library
        for book in library.books[:books_to_scan]:
            if book.id not in scanned_books:  # Check if the book hasn't been scanned yet
                total_score += book_scores[book.id]  # Add the score of the book to the total score
                scanned_books.add(book.id)  # Add the book to the set of scanned books

    return total_score


def genetic_options(book_scores, libraries, option, D):
    choices = {1: "Use default values", 2: "Personalize values"}
    print("\nGenetic algorithm uses default values.")
    print("Do you want to continue with the default ones or do you want to personalize the values?\n")
    
    while True:
        for k, v in choices.items():
            print(f"{k}| {v}")
            
        choice = int(input("\nChoose the values to use in genetic algorithm: "))
        #print("Option value before calling get_default_values_for_ga:", option)  # Debug output
        population_size, num_generations, mutation_prob, swap_prob, population_variation = get_default_values_for_ga(option)
        #print("Option value after calling get_default_values_for_ga:", option)  # Debug output
        #print("Default values retrieved:", population_size, num_generations, mutation_prob, swap_prob, population_variation)  # Debug output
        
        if choice == 1: 
            return genetic(book_scores, libraries, D, population_size, num_generations, mutation_prob, swap_prob, population_variation)

        elif choice == 2:
            population_size = personalized_input_for_ga("Population Size", population_size, True, 6, 100)
            num_generations = personalized_input_for_ga("Number of Generations", num_generations, True, 10, 1000)
            mutation_prob = personalized_input_for_ga("Mutation Probability", mutation_prob, False, 0, 1)
            swap_prob = personalized_input_for_ga("Swap Probability", swap_prob, False, 0, 1)
            population_variation = personalized_input_for_ga("Population Variation", population_variation, False, 0, 1)

            return genetic(book_scores, libraries, D, population_size, num_generations, mutation_prob, swap_prob, population_variation)
        
        else: 
            print("Invalid option. Choose a valid one.\n")    
            
def personalized_input_for_ga(value, default_value, is_int, min_value, max_value):
    user_value = input(value + "(default = " + str(default_value) + "): " )
    
    while True:
        user_value = int(user_value) if is_int else float(user_value)
                
        if user_value < min_value or user_value > max_value:
            user_value = input("Invalid input, please insert a valid one (min: " + str(min_value) + ", max: " + str(max_value) + "): ")
        else:
            break

    return user_value

# function that given an input file returns the values for population size, number of generations, mutation and swap
# probabilities and population variation
def get_default_values_for_ga(option):
    option = int(option)
    print (option)
    if option == 1:
        return (50, 1000, 0.2, 0.2, 0.2)
    elif option == 2:
        return (50, 1000, 0.2, 0.2, 0.2)
    elif option == 3:
        return (10, 10, 0.05, 0.05, 0.01)
    elif option == 4:
        return (10, 10, 0.05, 0.05, 0.001)
    elif option == 5:
        return (20, 500, 0.2, 0.2, 0.2)
    elif option == 6:
        return (20, 100, 0.2, 0.2, 0.2)
    else:
        print("Option not found. Returning default values." + str(option))
        return (50, 1000, 0.2, 0.2, 0.2)



    