# book class
class Book:
    def __init__(self, id, score):
        self.id = id
        self.score = score

    def __str__(self):
        return f"Book {self.id} with score {self.score}"
    
    def get_score(self):
        return self.score
    
