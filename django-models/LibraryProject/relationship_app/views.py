from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Book
from .models import Library

def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('list_books')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User

def admin_check(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def librarian_check(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def member_check(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Member'

@user_passes_test(admin_check)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

@user_passes_test(librarian_check)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

@user_passes_test(member_check)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')
