from django.db import models
from django.contrib.postgres.search import SearchVectorField

class GENDER(models.TextChoices):
	MALE = "M",
	FEMALE = "F",

class STATUS(models.TextChoices):
	PENDING = "PENDING"
	ACCEPTED = "ACCEPTED"
	REJECTED = "REJECTED"

class Candidate(models.Model):
	name = models.TextField()
	age = models.IntegerField()
	gender = models.TextField(choices=GENDER.choices, default=GENDER.MALE)
	email = models.TextField(unique=True)
	phone_number = models.TextField(max_length=10)
	status = models.TextField(choices=STATUS.choices, default=STATUS.PENDING)
	search_vector = SearchVectorField(null=True)