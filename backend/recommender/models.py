from django.db import models

# Create your models here.
class Arxiv(models.Model):
    paper_id = models.CharField(max_length=20)
    submitter = models.CharField(max_length=50)
    author = models.TextField()
    title = models.TextField()
    comments = models.TextField()
    doi = models.TextField()
    abstract = models.TextField()
    date = models.DateField()
    categories = models.TextField()

    def __str__(self):
        return self.title