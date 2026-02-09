from django.contrib import admin
from .models import Author, Genre, Book, BookInstance, BookReview

class AuthorAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'display_books']



class BookInstanceInLine(admin.TabularInline):
    model = BookInstance
    extra = 0 # išjungia papildomas tuščias eilutes įvedimui
    can_delete = False
    readonly_fields = ['uuid']
    fields = ['uuid', 'status', 'due_back']

class BookReviewInLine(admin.TabularInline):
    model = BookReview
    extra = 0

class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'display_genre']
    inlines = [BookReviewInLine, BookInstanceInLine]

class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ['book', 'status', 'due_back','uuid']
    list_filter = ['status', 'due_back']
    list_editable = ['due_back', 'status']
    search_fields = ['uuid', 'book__title']

    fieldsets = [
            ('General', {'fields': ('uuid', 'book')}),
            ('Availability', {'fields': ('status', 'due_back', 'reader')}),
        ]

class BookReviewAdmin(admin.ModelAdmin):
    model = BookReview
    list_display = ['book', 'date_created', 'reviewer', 'content']

# Admin modeliai registruojami cia
admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre)
admin.site.register(BookInstance, BookInstanceAdmin)
admin.site.register(BookReview, BookReviewAdmin)
