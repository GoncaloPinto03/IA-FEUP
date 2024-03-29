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

def ls_first_neighbour(B, L, D, book_scores, libraries):
    # Implement the Local Search - First Neighbour algorithm
    pass

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

