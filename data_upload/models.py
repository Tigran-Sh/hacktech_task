from django.db import models


class Person(models.Model):
    class Meta:
        db_table = "persons"

    name = models.CharField(max_length=255)
    email = models.EmailField(unique=False)
    phone_number = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"
