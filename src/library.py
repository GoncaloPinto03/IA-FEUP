class Library:
    def __init__(self, id, books, signup_days, books_per_day):
        self.id = id
        self.books = books
        self.signup_days = signup_days
        self.books_per_day = books_per_day
        self.scannedBooks = []

    def __str__(self):
        return f"{self.name} library with {len(self.books)} books"
    
    # get books that need to be scanned
    def get_books_to_send(self, days, scanned_books):
        remaining = days - self.signup_days
        n_books = self.books_per_day * remaining
        to_send = [book.id for book in self.books if book.id not in scanned_books]  # Get book IDs instead of book objects
        return to_send  # return the list of book IDs to be scanned

    def get_signup_days(self):
        return self.signup_days
    
    def get_books_per_day(self):
        return self.books_per_day
    
    def get_scanned_books(self):
        return self.scannedBooks

    def add_book(self, book):
        self.books.append(book)

    def remove_book(self, book):
        self.books.remove(book)
    
    def display_details(self):
        print(f"Library ID: {self.id}")
        print(f"Number of books: {len(self.books)}")
        print(f"Signup days: {self.signup_days}")
        print(f"Books per day: {self.books_per_day}")
        print("Books:")
        for book in self.books:
            print(book)
            
    def sort_books(self):
        self.books.sort(key=lambda x: x.score, reverse=True)

