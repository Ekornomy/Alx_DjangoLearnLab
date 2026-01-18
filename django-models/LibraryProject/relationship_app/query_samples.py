def get_books_by_author(author_name):
    from .models import Author, Book
    author = Author.objects.get(name=author_name)
    books = Book.objects.filter(author=author)
    return books

def get_books_in_library(library_name):
    from .models import Library
    library = Library.objects.get(name=library_name)
    books = library.books.all()
    return books

def get_librarian_for_library(library_name):
    from .models import Library, Librarian
    library = Library.objects.get(name=library_name)
    librarian = Librarian.objects.get(library=library)
    return librarian
