from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.views.generic.edit import FormMixin
from django.contrib.auth.models import User

from .models import Book, Author, Genre, BookInstance
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import BookReviewForm, UserChangeForm, CustomUserCreateForm

def index(request):

    # Suskaičiuokime keletą pagrindinių objektų
    # num_books = Book.objects.count()
    # num_instances = BookInstance.objects.count()

    # Laisvos knygos (tos, kurios turi statusą 'a')
    # num_instances_available = BookInstance.objects.filter(status='a').count()

    # Kiek yra autorių
    # num_authors = Author.objects.count()

    # SESIJOMS Papildome kintamuoju num_visits, įkeliame jį į kontekstą.
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': Book.objects.count(),
        'num_instances': BookInstance.objects.count(),
        'num_instances_available': BookInstance.objects.filter(status='a').count(),
        'num_authors': Author.objects.count(),
        'num_visits': num_visits,

    }

    return render(request, template_name="index.html", context=context)

def authors(request):
    authors = Author.objects.all()
    paginator = Paginator(authors, 3)
    page_number = request.GET.get('page')
    paged_authors= paginator.get_page(page_number)
    context = {
        'authors': paged_authors,
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

class BookDetailView(FormMixin, generic.DetailView):
    model = Book
    template_name = "book.html"
    context_object_name = "book"
    form_class = BookReviewForm

    # nurodome, kur atsidursime komentaro sėkmės atveju.
    def get_success_url(self):
        return reverse("book", kwargs={"pk": self.object.id})

    # standartinis post metodo perrašymas, naudojant FormMixin, galite kopijuoti tiesiai į savo projektą.
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    # štai čia nurodome, kad knyga bus būtent ta, po kuria komentuojame, o vartotojas bus tas, kuris yra prisijungęs.
    def form_valid(self, form):
        form.instance.book = self.get_object()
        form.instance.reviewer = self.request.user
        form.save()
        return super().form_valid(form)


def search(request):
    query = request.GET.get('query')
    book_search_results = Book.objects.filter(Q(title__icontains=query) |
                                              Q(summary__icontains=query) |
                                              Q(isbn__icontains=query) |
                                              Q(author__first_name__icontains=query) |
                                              Q(author__last_name__icontains=query))
    author_search_results = Author.objects.filter(Q(first_name__icontains=query) |
                                                  Q(last_name__icontains=query) |
                                                  Q(description__icontains=query))
    context = {
        'query': query,
        'book_search_results': book_search_results,
        'author_search_results': author_search_results,
    }
    return render(request, template_name="search.html", context=context)


class MyBookInstanceListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = "mybooks.html"
    context_object_name = "instances"

    def get_queryset(self):
        return BookInstance.objects.filter(reader=self.request.user)


# registracijos forma views neturi model
class SignUpView(generic.CreateView):
    form_class = CustomUserCreateForm
    template_name = "signup.html"
    success_url = reverse_lazy('login')

class ProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    form_class = UserChangeForm
    template_name = "profile.html"
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user