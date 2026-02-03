from django.shortcuts import render
from .models import Book, Author, Genre, BookInstance
from django.views import generic
from django.core.paginator import Paginator

def index(request):

    # Suskaičiuokime keletą pagrindinių objektų
    # num_books = Book.objects.count()
    # num_instances = BookInstance.objects.count()

    # Laisvos knygos (tos, kurios turi statusą 'a')
    # num_instances_available = BookInstance.objects.filter(status='a').count()

    # Kiek yra autorių
    # num_authors = Author.objects.count()

    context = {
        'num_books': Book.objects.count(),
        'num_instances': BookInstance.objects.count(),
        'num_instances_available': BookInstance.objects.filter(status='a').count(),
        'num_authors': Author.objects.count(),

    }

    return render(request, template_name="index.html", context=context)

def authors(request):
    authors = Author.objects.all()
    paginator = Paginator(authors, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'authors': Author.objects.all(),
    }
    return render(request, template_name="authors.html", context=context)

def author(request, author_id):
    context = {
        'author': Author.objects.get(id=author_id),
        # 'author': Author.objects.get(id=first_name),
    }
    return render(request, template_name="author.html", context=context)

class BookListView(generic.ListView):
    model = Book
    template_name = "books.html"
    context_object_name = "books"
    paginate_by = 3

class BookDetailView(generic.DetailView):
    model = Book
    template_name = "book.html"
    context_object_name = "book"


