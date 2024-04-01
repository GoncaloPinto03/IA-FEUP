import random, math

# Greedy Algorithm ----------------------------------------------------------------------------------------------------
def greedy(B, L, D, book_scores, libraries, choice):

    days_remaining = D
    signup_process = []
    books_scanned = set()
    total_score = 0

    libraries = greedy_sort_libraries(libraries)

    for library in libraries:

        if  days_remaining < library.signup_days or days_remaining <= 0:
            break

        else:
            days_remaining -= library.signup_days
            books_to_scan = []

            for book in library.books:
                if len(books_to_scan) < days_remaining * library.books_per_day and book.id not in books_scanned:
                    books_to_scan.append(book)
                    books_scanned.add(book.id)
                    total_score += book.score

            signup_process.append((library, books_to_scan))
    
    write_solution(choice, signup_process)

    return total_score

def greedy_sort_libraries(libraries):

    for library in libraries:
        library.sort_books()
    
    libraries.sort(key=lambda lib: sum(book.score for book in lib.books) / lib.signup_days, reverse=True)

    return libraries
# ----------------------------------------------------------------------------------------------------------------------

# Simulated Annealing Algorithm ----------------------------------------------------------------------------------------
def simulated_annealing(B, L, D, book_scores, libraries):

    temperature = 1.0           # Initial temperature
    min_temperature = 0.001     # Minimum temperature
    alpha = 0.9                 # Cooling rate
    n_iterations = 100          # Number of iterations

    curr_solution = [(library, []) for library in libraries if D - library.signup_days >= 0] # Initial solution
    curr_score = score_solution(curr_solution, D)

    while temperature > min_temperature:
        for i in range(n_iterations):
            new_solution = neighbor_solution(curr_solution, libraries, D)
            new_score = score_solution(new_solution, D)
            
            delta = new_score - curr_score
            
            if delta < 0:
                accept_probability = math.exp(delta / temperature)
            else:
                accept_probability = 1

            if accept_probability > random.random():
                curr_solution = new_solution
                curr_score = new_score
                    
        temperature *= alpha

    return curr_score

# Helper functions for Simulated Annealing
def neighbor_solution(solution, libraries, D):

    if not solution:
        return solution
    
    neighbor = solution[:]
    index = random.randrange(len(neighbor))
    library, _ = neighbor[index]
    
    if random.random() < 0.5:
        index_swap = random.randrange(len(neighbor))
        neighbor[index], neighbor[index_swap] = neighbor[index_swap], neighbor[index]
    else:
        random_books = random.sample(library.books, min(len(library.books), library.books_per_day * (D - library.signup_days)))
        neighbor[index] = (library, random_books)
    
    return neighbor

def score_solution(solution, D):

    days_remaining = D
    books_scanned = set()
    total_score = 0

    for library, books in solution:
        if days_remaining <= 0:
            break
        else:
            days_remaining -= library.signup_days
            num_scanned_books = min(days_remaining * library.books_per_day, len(books))
            for book in books[:num_scanned_books]:
                if book.id not in books_scanned:
                    total_score += book.score
                    books_scanned.add(book.id)

    return total_score
# -------------------------------------------------------------------------------------------------------------------------

# Local Search - First Neighbour Algorithm --------------------------------------------------------------------------------
def ls_first_neighbour(B, L, D, book_scores, libraries):

    libraries = ls_sort_libraries(libraries, book_scores)
    
    # Initialize the current solution
    current_libraries = libraries[:]  # Make a copy of libraries
    current_score = greedy(B, L, D, book_scores, libraries)  # Score of the current solution

    # Initialize variables to track the best neighbor
    best_neighbor_score = current_score

    # Iterate over the libraries to find the best neighbor
    for i in range(len(current_libraries)):
        # Calculate the score of the neighbor solution by removing the i-th library
        neighbor_libraries = current_libraries[:i] + current_libraries[i+1:]
        neighbor_score = calculate_neighbor_score(neighbor_libraries, D, book_scores)

        # Compare the scores
        if neighbor_score > best_neighbor_score:
            # Update the best neighbor
            return neighbor_score

    # Return the best score found
    return best_neighbor_score
# ------------------------------------------------------------------------------------------------------------------------

# Local Search - Best Neighbour Algorithm --------------------------------------------------------------------------------
def ls_best_neighbour(B, L, D, book_scores, libraries):

    libraries = ls_sort_libraries(libraries, book_scores)
    
    # Initialize the current solution
    current_libraries = libraries[:]  # Make a copy of libraries
    current_score = greedy(B, L, D, book_scores, libraries)  # Score of the current solution

    # Initialize variables to track the best neighbor
    best_neighbor_score = current_score

    # Iterate over the libraries to find the best neighbor
    for i in range(len(current_libraries)):
        # Calculate the score of the neighbor solution by removing the i-th library
        neighbor_libraries = current_libraries[:i] + current_libraries[i+1:]
        neighbor_score = calculate_neighbor_score(neighbor_libraries, D, book_scores)

        # Compare the scores
        if neighbor_score > best_neighbor_score:
            # Update the best neighbor
            best_neighbor_score = neighbor_score

    # Return the best score found
    return best_neighbor_score
# -------------------------------------------------------------------------------------------------------------------------

# Helper function Local Search
def ls_sort_libraries(libraries, book_scores):

    for library in libraries:
        library.sort_books()  # Sort books in each library based on scores
    libraries.sort(key=lambda lib: sum(book_scores[book.id] for book in lib.books) / lib.signup_days, reverse=True)

    return libraries

def calculate_neighbor_score(libraries, D, book_scores):
    days_remaining = D
    books_scanned = set()
    total_score = 0

    # Loop through each library and determine if it can be signed up within the remaining days
    for library in libraries:
        if days_remaining <= 0 or days_remaining < library.signup_days:
            break  # No more days left to sign up new libraries
        days_remaining -= library.signup_days

        # Calculate the number of books that can be scanned from this library
        for book in library.books:
            if len(books_scanned) < days_remaining * library.books_per_day and book.id not in books_scanned:
                books_scanned.add(book.id)
                total_score += book_scores[book.id]

    return total_score
# -------------------------------------------------------------------------------------------------------------------------

# Genetic Algorithm -------------------------------------------------------------------------------------------------------
def genetic(book_scores, libraries, D, population_size, num_generations, mutation_prob, swap_prob, population_variation):
    # Implement the Genetic algorithm
    # 1. initialize population
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
        population_size, num_generations, mutation_prob, swap_prob, population_variation = get_default_values_for_ga(option)
        
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
# -------------------------------------------------------------------------------------------------------------------------

# Write results on output file --------------------------------------------------------------------------------------------
def write_solution(choice, signup_process):

    print(choice)

    base_name = ''

    if choice == '1':
        base_name = "a_example"
    elif choice == '2':
        base_name = 'b_read_on'
    elif choice == '3':
        base_name = 'c_incunabula'
    elif choice == '4':
        base_name = 'd_tough_choices'
    elif choice == '5':
        base_name = 'e_so_many_books'
    elif choice == '6':
        base_name = 'f_libraries_of_the_world'
    
    output_path = f'output/{base_name}_output.txt'
    with open(output_path, 'w') as file:
        file.write(f"{len(signup_process)}\n")
        for library, books in signup_process:
            file.write(f"{library.id} {len(books)}\n")
            book_ids = ' '.join(str(book.id) for book in books)
            file.write(book_ids + "\n")
