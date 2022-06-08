from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import AbstractUser
import markdown2 as mk
# Create your models here.

class User(AbstractBaseUser):
    pass

class Procedimiento(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField(blank=False)

    def serialize(self):
        content = mk.markdown(self.content)
        # title = str(self.title).lower()
        title = str(self.title)
        return {
            'title':title,
            'content':content,
        }

    def __str__(self):
        return f'title: {self.title}'
