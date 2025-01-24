import os
from django.db import models
from django.conf import settings

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    file_name = models.CharField(max_length=255, default="anambra_history_book.pdf")
    embedding_id = models.CharField(max_length=255, unique=True)

    @property
    def file_path(self):
        return os.path.join(settings.BASE_DIR, 'chatbot', 'books', self.file_name)

    def __str__(self):
        return self.title
    

class BookChunk(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='chunks')
    chunk_id = models.IntegerField()
    content = models.TextField()

    class Meta:
        unique_together = ('book', 'chunk_id')

    def __str__(self):
        return f"{self.book.title} - Chunk {self.chunk_id}"
