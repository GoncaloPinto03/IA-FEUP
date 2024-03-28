# algorithms.py
import copy
import random, math

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
    return total_score

def simulated_annealing(B, L, D, book_scores, libraries, initial_temperature=1000, cooling_rate=0.95, iterations=1000):
    current_solution = generate_random_solution(B, L, D, libraries)
    current_score = calculate_score(current_solution, book_scores, libraries, D)

    best_solution = current_solution
    best_score = current_score

    temperature = initial_temperature

    for i in range(iterations):
        new_solution = generate_neighbour_solution(current_solution, libraries)
        new_score = calculate_score(new_solution, book_scores, libraries, D)

        delta_score = new_score - current_score

        if delta_score > 0 or random.random() < math.exp(delta_score / temperature):
            current_solution = new_solution
            current_score = new_score

        if current_score > best_score:
            best_score = current_score

        temperature *= cooling_rate

    return best_score

def generate_random_solution(B, L, D, libraries):
    days_remaining = D
    solution = [-1] * D
    libraries_to_signup = random.sample(range(L), L)
    for lib_id in libraries_to_signup:
        lib = libraries[lib_id]
        signup_days = lib.get_signup_days()
        if signup_days > days_remaining:
            break
        solution[D - days_remaining:D - days_remaining + signup_days] = [lib_id] * signup_days
        days_remaining -= signup_days
    return solution

def generate_neighbour_solution(current_solution, libraries):
    neighbour_solution = current_solution.copy()
    lib_ids = [i for i, lib_id in enumerate(current_solution) if lib_id != -1]
    if len(lib_ids) < 2:
        return current_solution
    lib1_id, lib2_id = random.sample(lib_ids, 2)
    neighbour_solution[lib1_id], neighbour_solution[lib2_id] = neighbour_solution[lib2_id], neighbour_solution[lib1_id]
    return neighbour_solution

def calculate_score(solution, book_scores, libraries, D):
    scanned_books = set()
    total_score = 0
    for lib_id in solution:
        if lib_id == -1:
            continue
        for book_id in libraries[lib_id].get_books(D, scanned_books):
            total_score += book_scores[book_id]
            scanned_books.add(book_id)
    return total_score


'''
# function to calculate the if the solution is accepted with a certain probability
def accept_with_probability(delta, t):
    r = random.randrange(0, 1)
    f = math.exp(delta / t)
    if f >= r:
        return True
    else:
        return False
    

# function that optimizes the given solution with the random neighbour algorithm
def random_neighbour(B, L, D, libraries, scores, n_days, heuristic):
    unique_libraries = set(B)  # gets all the libraries ids
    if -1 in unique_libraries:
        unique_libraries.remove(-1)

    current_lib = random.choice(list(unique_libraries))  # choose a random library

    day = 0
    books2lib = dict()
    scanned_books = set()
    new_list = []

    while day < B.index(current_lib):
        lib = B[day]
        books2lib[lib] = solution.books2lib[lib]
        scanned_books.update(books2lib[lib])
        for _ in range(libraries[lib].signup_days):
            new_list.append(lib)
            day += 1

    remaining_days = libraries[current_lib].signup_days + solution.libraries_list.count(-1)
    all_libraries = [lib for lib in libraries if
                     lib.id not in solution.libraries_list and lib.signup_days <= remaining_days]

    if len(all_libraries) == 0:
        return solution

    if heuristic:  # if we want to apply the heuristic
        lib_id, books = choose_best_score(n_days - day, all_libraries, scores, scanned_books)
    else:
        lib_id = random.choice(all_libraries).id
        books = libraries[lib_id].get_books(remaining_days, scanned_books)
    new_day = day
    if lib_id != -1:
        books2lib[lib_id] = books
        scanned_books.update(books)
        for _ in range(libraries[lib_id].signup_days):
            new_list.append(lib_id)
            new_day += 1

    day += libraries[current_lib].signup_days

    while day < n_days:
        lib = solution.libraries_list[day]
        if lib == -1:
            break
        books2lib[lib] = libraries[lib].get_books(n_days - new_day, scanned_books)
        scanned_books.update(books2lib[lib])
        for _ in range(libraries[lib].signup_days):
            new_list.append(lib)
            new_day += 1
            day += 1

    while len(new_list) < n_days:  # if the new solution does not occupy n_days we fill it with -1
        new_list.append(-1)

    new_score = score(scanned_books, scores)

    return new_list, new_score, books2lib


# stabilizes at 140 iterations
def cooling_function(t):
    temp = 300
    return temp / (1 + t * t)


# function that optimizes the given solution with the simulated annealing algorithm
def simulated_annealing(B, L, D, libraries, scores, n_days):
    not_accepted = 0
    time = 0
    bestB, bestL, bestD = B, L, D

    while not_accepted < 200:
        new_solution = random_neighbour(B, L, D, libraries, scores, n_days, True)  # gets new solution using random_descendent on previous found solution
        t = cooling_function(time)
        if t < 0.001:
            break  # no need to keep trying to "cool down"
        delta = new_solution.score - solution.score

        if delta <= 0 and not accept_with_probability(delta, t):
            not_accepted += 1
        else:
            solution = new_solution
            if solution.score > best_solution.score:
                best_solution = solution
            print("Accepted:", solution.score)

        time += 1

    return best_solution
'''


def ls_first_neighbour(B, L, D, book_scores, libraries):
    # Initialize current solution
    current_solution = initialize_solution(B, L, D, libraries)
    current_score = calculate_score_neighbor(current_solution, book_scores, D)

    # Main loop
    while True:
        # Generate a neighboring solution
        neighbor_solution = generate_neighbor(current_solution)

        # Calculate the score of the neighboring solution
        neighbor_score = calculate_score_neighbor(neighbor_solution, book_scores, D)

        # If the neighboring solution is better, update the current solution
        if neighbor_score > current_score:
            current_solution = neighbor_solution
            current_score = neighbor_score
        else:
            # If no improvement found, break the loop
            break

    return current_score

def initialize_solution(B, L, D, libraries):
    # This function initializes a solution by randomly selecting libraries to sign up
    # and scanning books from those libraries
    # You can implement this based on your specific requirements and constraints
    
    # Example:
    selected_libraries = random.sample(libraries, min(len(libraries), D))  # Randomly select libraries up to D
    return selected_libraries

def generate_neighbor(solution):
    # This function generates a neighboring solution by modifying the current solution
    # You can implement this based on your specific requirements and constraints
    
    # Example:
    new_solution = solution[:]  # Create a copy of the current solution
    # Modify the solution, e.g., swap libraries, remove/add books, etc.
    # Implement your logic here
    
    return new_solution


def calculate_score_neighbor(solution, book_scores, remaining_days):
    total_score = 0
    scanned_books = set()  # Initialize scanned books set
    for library in solution:
        for book_id in library.get_books(remaining_days, scanned_books):
            total_score += book_scores[book_id]
            scanned_books.add(book_id)  # Update scanned books set
    return total_score




def ls_best_neighbour(B, L, D, book_scores, libraries):
    # Implement the Local Search - Best Neighbour algorithm
    pass

def ls_random_neighbour(B, L, D, book_scores, libraries):
    # Implement the Local Search - Random Neighbour algorithm
    pass

def genetic(B, L, D, book_scores, libraries):
    # Implement the Genetic algorithm
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
        books = library.get_books(days, scanned_books)
        if books is None:
            print(f"Books for library {library.id} is None!")
        s = score(books, scores) / library.signup_days
        if s > best_score:
            best_lib = library.id
            best_score = s
            best_books = books

    if best_lib is None:
        return -1, best_books

    return best_lib, best_books
