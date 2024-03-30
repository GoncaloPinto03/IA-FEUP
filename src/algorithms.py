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
    # NOTE: check in gpt if the best solution should be inside the for loop or not
    
    population = initialize_population(population_size, len(libraries))
    
    for i in range(num_generations):
        new_population = []
        for _ in range(population_size):
            parents = select_parents(population, 2, D, book_scores, libraries)
            print(parents)
            # offspring = crossover(parents)
            offspring = mutate(offspring, mutation_prob, swap_prob)
            new_population.append(offspring)
        population = new_population

    best_solution = max(population, key=lambda x: calculate_score(x, D, book_scores, libraries))
    best_score = calculate_score(best_solution, D, book_scores, libraries)
    
    return best_solution, best_score



def mutate(solution, mutation_rate, swap_rate):
    if random.random() < mutation_rate:
        i1, i2 = random.sample(range(len(solution), 2))
        i1, i2 = mutate_swap(i1, i2, swap_rate)
        
    return solution


def mutate_swap(i1, i2, swap_rate):
    if random.random() < swap_rate: 
        i1, i2 = i2, i1
        
    return i1, i2


def calculate_score(solution, D, scores, libraries):
    total_score = 0
    scanned_books = set()
    day = 0
    
    for library_index in solution:
        library = libraries[library_index]
        day += library['signup_time']
        
        if day >= D:  # Stop if signup exceeds available days
            break
        remaining_days = D - day
        books_to_scan = min(remaining_days * library['books_per_day'], len(library['books']))
        
        for book in library['books'][:books_to_scan]:
            if book not in scanned_books:
                total_score += scores[book]
                scanned_books.add(book)
                
    return total_score



# shuffles the libraries indices to create a random solution
def initialize_population(population_size, num_libraries):
    # print(population_size)
    # print(num_libraries)
    population = []
    for _ in range(population_size):
        solution = random.sample(range(num_libraries), num_libraries)
        print(solution)
        population.append(solution)
    # print("-------------------")

    return population


# tournament selection of parents by randomly choosing groups and select the best in those groups
# we could also randomly choose a group and pick the best two out of that group I guess
# def select_parents(population, n):
#     p1 = random.sample(population, n)
#     parent1 = sorted(p1, key=lambda x: x.score, reverse=True)[0]
    
#     # rest is the remaining population 
#     rest = [x for x in population if x not in p1]
#     p2 = random.sample(rest, n)
#     parent2 = sorted(p2, key=lambda x: x.score, reverse=True)[0]
    
#     return parent1, parent2

def select_parents(population, num_parents, D, scores, libraries):
    parents = []
    population_size = len(population)
    
    for _ in range(num_parents):
        # Randomly select a subset of individuals (tournament)
        tournament_size = min(5, population_size)  
        tournament = random.sample(population, tournament_size)
        
        # Select the individual with the highest fitness (total score)
        winner = max(tournament, key=lambda x: calculate_score(x, D, scores, libraries))
        parents.append(winner)
        
    return parents


# def select_parents(population, fitness_scores):
#     # Select individuals from the population for mating
#     # You can use different selection strategies here
#     # Example: Roulette wheel selection
#     total_fitness = sum(fitness_scores)
#     probabilities = [fitness / total_fitness for fitness in fitness_scores]
#     parents = np.random.choice(population, size=2, p=probabilities, replace=False)
#     return parents




# call this function in menu
def genetic_options(book_scores, libraries, option, D):
    options = {1: "Use default values", 2: "Personalize values"}
    message = "\nGenetic algorithm uses default values.\nDo you want to continue with the default ones or do you want to personalize the values?\n"
    print(message)
    
    while True:
        for k, v in options.items():
            print(str(k) + "| " + v)
            
        choice = int(input("\nChoose the values to use in genetic algorithm: "))
        population_size, num_generations, mutation_prob, swap_prob, population_variation = get_default_values_for_ga(option)
        
        if (choice == 1): 
            # call genetic algorithm with default values
            return genetic(book_scores, libraries, D, population_size, num_generations, mutation_prob, swap_prob, population_variation)

        elif (choice == 2):
            # call genetic algorithm with personalized values
            population_size = personalized_input_for_ga("\nPopulation Size ", population_size, True, 6, 100)
            num_generations = personalized_input_for_ga("\nNumber of Generations ", num_generations, True, 10, 1000)
            mutation_prob = personalized_input_for_ga("\nMutation Probability ", mutation_prob, False, 0, 1)
            swap_prob = personalized_input_for_ga("\nSwap Probability ", swap_prob, False, 0, 1)
            population_variation = personalized_input_for_ga("\nPopulation Variation ", population_variation, False, 0, 1)
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
    