"""
Sample queries demonstrating Django ORM relationships:
- ForeignKey
- ManyToManyField
- OneToOneField
"""

def get_books_by_author(author_name):
    """
    Query all books by a specific author using ForeignKey relationship.
    
    Example usage:
        books = get_books_by_author('J.K. Rowling')
    """
    from .models import Author, Book
    
    # Method 1: Using reverse relationship from Author
    try:
        author = Author.objects.get(name=author_name)
        books = author.books.all()  # Uses related_name='books'
        return books
    except Author.DoesNotExist:
        return Book.objects.none()
    
    # Alternative: Direct filter on Book model
    # return Book.objects.filter(author__name=author_name)

def get_books_in_library(library_name):
    """
    List all books in a library using ManyToMany relationship.
    
    Example usage:
        books = get_books_in_library('Central Library')
    """
    from .models import Library
    
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()  # Access through ManyToManyField
        return books
    except Library.DoesNotExist:
        return []

def get_librarian_for_library(library_name):
    """
    Retrieve the librarian for a library using OneToOne relationship.
    
    Example usage:
        librarian = get_librarian_for_library('Central Library')
    """
    from .models import Library
    
    try:
        library = Library.objects.get(name=library_name)
        # Access through OneToOne reverse relationship (uses related_name='librarian')
        librarian = library.librarian
        return librarian
    except Library.DoesNotExist:
        return None
    except Library.librarian.RelatedObjectDoesNotExist:
        # This exception occurs if no librarian is assigned to the library
        return None

# Example of how to use these functions
if __name__ == "__main__":
    print("This module contains ORM query examples.")
    print("To use these functions, run them in Django shell:")
    print("1. python manage.py shell")
    print("2. from relationship_app.query_samples import *")
    print("3. Call the functions with appropriate parameters")
