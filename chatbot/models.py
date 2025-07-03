from django.db import models

from university_chatbot.settings import LANGUAGES

class QueryLog(models.Model):
    question = models.TextField()
    sql = models.TextField()
    results = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    language = models.CharField(max_length=2, choices=LANGUAGES)

    def __str__(self):
        return f"Query at {self.created_at}"