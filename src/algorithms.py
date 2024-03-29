# algorithms.py
import copy
import random, math

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

def simulated_annealing2(B, L, D, book_scores, libraries, initial_temperature=100, cooling_rate=0.95, iterations=1000):
    current_solution = generate_random_solution(B, L, D, libraries)
    current_score = calculate_score(current_solution, book_scores, libraries, D)

    best_solution = current_solution
    best_score = current_score

    temperature = initial_temperature

    for i in range(iterations):
        # Cooling schedule
        temperature = temp_sched(temperature, cooling_rate)

        # Generate a random neighboring solution
        new_solution = generate_neighbour_solution(current_solution, libraries)

        # Calculate the score for the new solution
        new_score = calculate_score(new_solution, book_scores, libraries, D)

        # Evaluate the energy difference between the current and new solutions
        delta_E = new_score - current_score

        # If the new solution is better or with a probability based on temperature, accept it
        if delta_E > 0 or Prob(current_score, new_score, temperature) >= random.random():
            current_solution = new_solution
            current_score = new_score

        # Update the best solution if needed
        if current_score > best_score:
            best_solution = current_solution
            best_score = current_score

    return best_score

def temp_sched(temperature, cooling_rate):
    # Adjust temperature here (e.g., geometric cooling, linear cooling, etc.)
    # Example: geometric cooling
    return temperature * cooling_rate

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

def Prob(current_score, new_score, temperature):
    # Calculate the probability of accepting the new solution given its performance change and the current temperature
    return math.exp((new_score - current_score) / temperature)




def simulated_annealing(B, L, D, book_scores, libraries):

    current_solution = initial_solution(D, libraries)
    current_score = score_solution(current_solution, D)
    
    T = 1.0
    T_min = 0.001
    alpha = 0.9

    while T > T_min:
        i = 1
        while i <= 100:
            new_solution = neighbor_solution(current_solution, libraries, D)
            new_score = score_solution(new_solution, D)
            
            # Calculate change in score
            delta = new_score - current_score
            
            # Acceptance probability
            acceptance_probability = math.exp(delta / T) if delta < 0 else 1
            
            # Decide if we should accept the new solution
            if acceptance_probability > random.random():
                current_solution = new_solution
                current_score = new_score
            
            i += 1
        
        T *= alpha  # Cool down the temperature

    return current_score

# Helper functions

def initial_solution(D, libraries):
    return [(library, []) for library in libraries if D - library.signup_days >= 0]


def neighbor_solution(solution, libraries, D):
    # Make a random change in the solution to generate a neighbor
    if not solution:
        return solution
    
    neighbor = solution[:]
    idx = random.randrange(len(neighbor))
    library, _ = neighbor[idx]
    
    # Randomly decide to change the order of the library signup or change the books
    if random.random() < 0.5:
        # Swap two libraries' positions
        idx_swap = random.randrange(len(neighbor))
        neighbor[idx], neighbor[idx_swap] = neighbor[idx_swap], neighbor[idx]
    else:
        # Change the books to scan in the library
        random_books = random.sample(library.books, min(len(library.books), library.books_per_day * (D - library.signup_days)))
        neighbor[idx] = (library, random_books)
    
    return neighbor

def score_solution(solution, D):
    score = 0
    books_scanned = set()
    days_remaining = D
    for library, books in solution:
        days_remaining -= library.signup_days
        if days_remaining <= 0:
            break
        # Calculate how many books can actually be scanned
        num_scanned_books = min(days_remaining * library.books_per_day, len(books))
        for book in books[:num_scanned_books]:
            if book.id not in books_scanned:
                score += book.score
                books_scanned.add(book.id)
    return score

def ls_first_neighbour(B, L, D, book_scores, libraries):
    # Sort libraries based on a heuristic: a ratio of the total score of books to the signup time.
    for library in libraries:
        library.sort_books()  # Sort books in each library based on scores
    libraries.sort(key=lambda lib: sum(book_scores[book.id] for book in lib.books) / lib.signup_days, reverse=True)
    # Initialize the current solution
    current_libraries = libraries[:]  # Make a copy of libraries
    current_score = 0

    # Initialize remaining days
    remaining_days = D

    # Iterate over the libraries to find the first neighbor
    for i, library in enumerate(current_libraries):
        signup_days = library.signup_days

        # Calculate the score of the neighbor solution by removing the i-th library
        books_to_scan = min(library.books_per_day * remaining_days, len(library.books))
        if books_to_scan > 0:
            neighbor_libraries = current_libraries[:i] + current_libraries[i+1:]
            neighbor_score = sum(book.score for book in library.books[:books_to_scan])
            if neighbor_score > current_score:
                # Update the current solution
                current_score = neighbor_score
                current_libraries = neighbor_libraries
                print("Found a better neighbor")

        # Update remaining days after signing up the current library
        remaining_days -= signup_days

        if remaining_days <= 0:
            break

    print("Did not find a better neighbor")
    return current_score



def ls_best_neighbour(B, L, D, book_scores, libraries):
    # Sort libraries based on a heuristic: a ratio of the total score of books to the signup time.
    for library in libraries:
        library.sort_books()  # Sort books in each library based on scores
    libraries.sort(key=lambda lib: sum(book_scores[book.id] for book in lib.books) / lib.signup_days, reverse=True)
    
    # Initialize the current solution
    current_libraries = libraries[:]  # Make a copy of libraries
    #current_score = greedy(B, L, D, book_scores, current_libraries)  # Score of the current solution
    current_score = 0

    # Calculate the initial score
    library_scores = [sum(book.score for book in library.books) for library in libraries]

    # Initialize variables to track the best neighbor
    best_neighbor_libraries = None
    best_neighbor_score = current_score

     # Initialize remaining days
    remaining_days = D

    scanned_books = []

    # Iterate over the libraries to find the first neighbor
    for i in range(len(current_libraries)):
        # Calculate the score of the neighbor solution by removing the i-th library
        if current_libraries[i].books_per_day * remaining_days < len(current_libraries[i].get_books(D,scanned_books)):
            if len(current_libraries) > 1:
                neighbor_libraries = current_libraries[:i] + current_libraries[i+1:]
                neighbor_score = 0
                for j in range(len(neighbor_libraries)):
                    neighbor_score = sum(book.score for book in current_libraries[j].books)
                if neighbor_score > current_score:
                    # Update the best neighbor
                    best_neighbor_libraries = neighbor_libraries
                    best_neighbor_score = neighbor_score
            else:
                neighbor_score = 0
        else:
            print("Not enough days to scan books")
        
        # Calculate the days required to sign up the library
        signup_days = current_libraries[i].signup_days

        # Calculate the remaining days after signing up the current library
        remaining_days -= signup_days

        # Check if there are remaining days for scanning books
        if remaining_days <= 0:
            break



    # Return the best score found
    print ("Did not find a better neighbor")
    return best_neighbor_score

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

