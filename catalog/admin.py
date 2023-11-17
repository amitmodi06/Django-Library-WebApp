from django.contrib import admin
from .models import Book, Author, Genre,  BookInstance, Language

# Register your models here.

# admin.site.register(Book)
@admin.register(Book)  # this decorator is another way of writing admin.site.register(Book)
class BookAdmin(admin.ModelAdmin):
    pass

# admin.site.register(BookInstance)
@admin.register(BookInstance) 
class BookInstanceAdmin(admin.ModelAdmin):
    pass

# admin.site.register(Author)
# Define the admin class
class AuthorAdmin(admin.ModelAdmin):
    pass

# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)

admin.site.register(Genre)
admin.site.register(Language)