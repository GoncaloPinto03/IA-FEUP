import random, math

# Greedy Algorithm
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

# Simulated Annealing Algorithm
def simulated_annealing(B, L, D, book_scores, libraries):

    temperature = 1.0           # Initial temperature
    min_temperature = 0.001     # Minimum temperature
    alpha = 0.9                 # Cooling rate

    current_solution = initial_solution(D, libraries)
    current_score = score_solution(current_solution, D)

    while temperature > min_temperature:
        iteration = 1
        while iteration <= 100:
            new_solution = neighbor_solution(current_solution, libraries, D)
            new_score = score_solution(new_solution, D)
            
            # Calculate change in score
            delta = new_score - current_score
            
            # Acceptance probability
            acceptance_probability = math.exp(delta / temperature) if delta < 0 else 1
            
            # Decide if we should accept the new solution
            if acceptance_probability > random.random():
                current_solution = new_solution
                current_score = new_score
            
            iteration += 1
        
        temperature *= alpha  # Cool down the temperature

    return current_score

# Helper functions for Simulated Annealing
def initial_solution(D, libraries):
    return [(library, []) for library in libraries if D - library.signup_days >= 0]

def neighbor_solution(solution, libraries, D):
    # Make a random change in the solution to generate a neighbor
    if not solution:
        return solution
    
    neighbor = solution[:]
    index = random.randrange(len(neighbor))
    library, _ = neighbor[index]
    
    # Randomly decide to change the order of the library signup or change the books
    if random.random() < 0.5:
        # Swap two libraries' positions
        idx_swap = random.randrange(len(neighbor))
        neighbor[index], neighbor[idx_swap] = neighbor[idx_swap], neighbor[index]
    else:
        # Change the books to scan in the library
        random_books = random.sample(library.books, min(len(library.books), library.books_per_day * (D - library.signup_days)))
        neighbor[index] = (library, random_books)
    
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

# Local Search - First Neighbour Algorithm
def ls_first_neighbour(B, L, D, book_scores, libraries):
    # Sort libraries based on a heuristic: a ratio of the total score of books to the signup time.
    for library in libraries:
        library.sort_books()  # Sort books in each library based on scores
    libraries.sort(key=lambda lib: sum(book_scores[book.id] for book in lib.books) / lib.signup_days, reverse=True)
    
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

# Local Search - Best Neighbour Algorithm
def ls_best_neighbour(B, L, D, book_scores, libraries):
    # Sort libraries based on a heuristic: a ratio of the total score of books to the signup time.
    for library in libraries:
        library.sort_books()  # Sort books in each library based on scores
    libraries.sort(key=lambda lib: sum(book_scores[book.id] for book in lib.books) / lib.signup_days, reverse=True)
    
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

# Helper function Local Search
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

def ls_random_neighbour(B, L, D, book_scores, libraries):
    # Implement the Local Search - Random Neighbour algorithm
    pass

def genetic(B, L, D, book_scores, libraries):
    # Implement the Genetic algorithm
    pass


