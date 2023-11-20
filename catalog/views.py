from django.shortcuts import render
from .models import Book, BookInstance, Author, Genre, Language

# Create your views here.
def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    #The 'all()' is implied by default
    num_authors = Author.objects.count()

    # Books with the word "The" in it
    num_books_with_letter_The = Book.objects.filter(title__icontains='The').count()


    context = {
        'num_books' : num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_books_with_letter_The' : num_books_with_letter_The
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)