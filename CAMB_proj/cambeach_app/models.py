from django.db import models

class Topic(models.Model):
    
    def __str__(self):
        return self