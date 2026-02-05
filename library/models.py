from django.db import models
import uuid
from django.contrib.auth.models import User
from django.utils import timezone
from tinymce.models import HTMLField


class Genre(models.Model):
    name = models.CharField(verbose_name="Name", max_length=200)

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(verbose_name="First Name", max_length=100)
    last_name = models.CharField(verbose_name="Last Name", max_length=100)
    description = HTMLField(verbose_name="Description", max_length=4000, default="")

    class Meta:
        verbose_name = "Autorius"
        verbose_name_plural = "Autoriai"

    def display_books(self):
        return ', '.join(book.title for book in self.books.all())

    display_books.short_description = "Books"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Book(models.Model):
    title = models.CharField(verbose_name="Title", max_length=200)
    author = models.ForeignKey(to="Author",
                               verbose_name="Author",
                               on_delete=models.SET_NULL,
                               null=True,
                               blank=True,
                               related_name="books")
    summary = models.TextField(verbose_name="Summary", max_length=1000, help_text="Short Book summary")
    genre = models.ManyToManyField(to='Genre', verbose_name="Genres")
    isbn = models.CharField(verbose_name="ISBN", max_length=13)
    cover = models.ImageField(verbose_name="Cover Image", upload_to="covers", blank=True, null=True)

    def display_genre(self):
        return ", ".join(genre.name for genre in self.genre.all())

    display_genre.short_description = "Genre"

    def __str__(self):
        return self.title

class BookInstance(models.Model):
    uuid = models.UUIDField(verbose_name="ID", default=uuid.uuid4())
    book = models.ForeignKey(to="Book",
                             verbose_name="Book",
                             on_delete=models.SET_NULL,
                             null=True,
                             blank=True,
                             related_name="instances")
    due_back = models.DateField(verbose_name="Available On", null=True, blank=True)
    reader = models.ForeignKey(to=User, verbose_name="Reader", on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
    ('d', 'Administrated'),
    ('t', 'Taken'),
    ('a', 'Available'),
    ('r', 'Reserved'),
    )

    status = models.CharField(verbose_name="Status", max_length=1, choices=LOAN_STATUS, blank=True, default='d')

    def is_overdue(self):
        return self.due_back and timezone.now().date() > self.due_back

    def __str__(self):
        return str(self.uuid)