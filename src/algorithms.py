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




def ls_first_neighbor(B, L, D, book_scores, libraries):
    # Sort libraries based on a heuristic: a ratio of the total score of books to the signup time.
    for library in libraries:
        library.sort_books()  # Sort books in each library based on scores
    libraries.sort(key=lambda lib: sum(book.score for book in lib.books) / lib.signup_days, reverse=True)

    # Initialize the current solution
    current_libraries = libraries[:]  # Make a copy of libraries
    current_score = greedy(B, L, D, book_scores, current_libraries)  # Score of the current solution

    # Calculate the initial score
    library_scores = [sum(book.score for book in library.books) for library in libraries]

    # Iterate over the libraries to find the first neighbor
    for i in range(len(current_libraries)):
        # Calculate the score of the current solution
        current_library_score = library_scores[i]
        
        # Calculate the score of the neighbor solution by removing the i-th library
        neighbor_libraries = current_libraries[:i] + current_libraries[i+1:]
        neighbor_score = current_score - current_library_score

        # Compare the scores
        if neighbor_score > current_score:
            # Update the current solution if the neighbor is better
            current_libraries = neighbor_libraries
            current_score = neighbor_score

    # Return the best solution found
    return current_score



def ls_best_neighbour(B, L, D, book_scores, libraries):
    # Sort libraries based on a heuristic: a ratio of the total score of books to the signup time.
    for library in libraries:
        library.sort_books()  # Sort books in each library based on scores
    libraries.sort(key=lambda lib: sum(book.score for book in lib.books) / lib.signup_days, reverse=True)

    # Initialize the current solution
    current_libraries = libraries[:]  # Make a copy of libraries
    current_score = greedy(B, L, D, book_scores, current_libraries)  # Score of the current solution

    # Calculate the initial score
    library_scores = [sum(book.score for book in library.books) for library in libraries]

    # Initialize variables to track the best neighbor
    best_neighbor_libraries = None
    best_neighbor_score = current_score

    # Iterate over the libraries to find the best neighbor
    for i in range(len(current_libraries)):
        # Calculate the score of the current solution
        current_library_score = library_scores[i]
        
        # Calculate the score of the neighbor solution by removing the i-th library
        neighbor_libraries = current_libraries[:i] + current_libraries[i+1:]
        neighbor_score = current_score - current_library_score

        # Compare the scores
        if neighbor_score > best_neighbor_score:
            # Update the best neighbor
            best_neighbor_libraries = neighbor_libraries
            best_neighbor_score = neighbor_score

    # Return the best score found
    return best_neighbor_score



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