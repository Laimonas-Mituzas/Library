from django.db import models
import uuid


class Genre(models.Model):
    name = models.CharField(verbose_name="Name", max_length=200)

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(verbose_name="First Name", max_length=100)
    last_name = models.CharField(verbose_name="Last Name", max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Book(models.Model):
    title = models.CharField(verbose_name="Title", max_length=200)
    author = models.ForeignKey(to="Author", verbose_name="Author", on_delete=models.SET_NULL, null=True, blank=True)
    summary = models.TextField(verbose_name="Summary", max_length=1000, help_text="Short Book summary")
    genre = models.ManyToManyField(to='Genre', verbose_name="Genres")
    isbn = models.CharField(verbose_name="ISBN", max_length=13)

    def __str__(self):
        return self.title

class BookInstance(models.Model):
    uuid = models.UUIDField(verbose_name="UUID", default=uuid.uuid4())
    book = models.ForeignKey(to="Book", verbose_name="Book", on_delete=models.SET_NULL, null=True, blank=True, related_name="instances")

    LOAN_STATUS = (
    ('d', 'Administrated'),
    ('t', 'Taken'),
    ('a', 'Available'),
    ('r', 'Reserved'),
    )

    status = models.CharField(verbose_name="Status", max_length=1, choices=LOAN_STATUS, blank=True, default='d')

    def __str__(self):
        return str(self.uuid)