# algorithms.py
import copy
import random

def greedy(B, L, D, book_scores, libraries):
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
