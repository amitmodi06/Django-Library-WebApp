from django.db import models
from django.urls import reverse  # To generate URLS by reversing URL patterns
from django.conf import settings
from datetime import date
import uuid

# Create your models here.
class Genre(models.Model):
    """Model representing a book genre."""

    name = models.CharField(max_length=200, unique=True, help_text="Enter the book genre (e.g. Science Fiction, Poetry etc.)")

    def get_absolute_url(self):
        """Returns the url to access a particular genre instance."""
        return reverse("genre-detail", args=[str(self.id)])
    

    def __str__(self):
        """String for representing the Model object."""
        return self.name
    

class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', 
                               on_delete=models.RESTRICT, 
                               null=True)
    # Foreign Key used because book can only have one author, but authors can have multiple books.
    # null = True will allow database to store a null value if no author is selected
    # on_delete=models.RESTRICT :- will prevent associated author being deleted if referenced book is deleted

    summary = models.TextField(max_length=1000, 
                               help_text="Enter the summary of the book")
    isbn = models.CharField("ISBN", 
                            max_length=13, 
                            unique=True, 
                            help_text='13 character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Genre, 
                                   help_text="Selct a genre for this book")
    # Many-to-many used because a book can have multiple genres and a genre can have many books. 

    language = models.ForeignKey("Language", 
                                 on_delete=models.SET_NULL,
                                 null=True)
    

    class Meta:
        ordering = ['title', 'author']

    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'


    def get_absolute_url(self):
        """Returns the url to access a particular genre instance."""
        return reverse("book-detail", args=[str(self.id)])
    

    def __str__(self) -> str:
        """String for representing the Model object."""
        return self.title
    

class BookInstance(models.Model):
    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""
    id = models.UUIDField(primary_key=True, 
                            default=uuid.uuid4, 
                            help_text="Unique ID for this particular book across whole library")
    # UUIDField is used to set the id field as PK for this model. It will set globally unique value for each instance

    book = models.ForeignKey('Book', 
                                on_delete=models.RESTRICT, 
                                null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    
    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On Loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )
    
    status = models.CharField(max_length=1,
                                choices=LOAN_STATUS,
                                blank=True,
                                default='m',
                                help_text='Book availability')
    

    borrower = models.ForeignKey(settings.AUTH_USER_MODEL, 
                                    on_delete=models.SET_NULL, 
                                    null=True, 
                                    blank=True)

    @property
    def is_overdue(self):
        """Determines if the book is overdue based on due date and current date."""
        return bool(self.due_back and date.today() > self.due_back)


    class Meta:
        ordering = ['due_back']
    
    
    def __str__(self) -> str:
        """String for representing the Model object."""
        return f'{self.id} ({self.book.title})'
    
    def get_absolute_url(self):
        """Returns the url to access a particular book instance."""
        return reverse("bookinstance-detail", args=[str(self.id)])


class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    data_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the URL to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self) -> str:
        return f'{self.first_name}, {self.last_name}'


class Language(models.Model):
    """Model representing language (e.g. English, Hindi etc)"""
    name = models.CharField(max_length=200,
                            unique=True,
                            help_text="Enter the book's natural language (e.g. English, Hindi etc.)")
    
    def get_absolute_url(self):
        """Returns the URL to access a particular author instance."""
        return reverse('language-detail', args=[str(self.id)])

    def __str__(self) -> str:
        """String for representing the Model object (in Admin site etc.)"""
        return self.name