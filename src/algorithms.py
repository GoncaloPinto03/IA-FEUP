# algorithms.py
import copy
import random

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
