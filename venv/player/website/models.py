from typing import Any
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Record(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	first_name = models.CharField(max_length=50)
	last_name =  models.CharField(max_length=50)
	email =  models.CharField(max_length=100)
	phone = models.CharField(max_length=15)
	address =  models.CharField(max_length=100)
	city =  models.CharField(max_length=50)
	state =  models.CharField(max_length=50)
	zipcode =  models.CharField(max_length=20)

	def __str__(self):
		return(f"{self.first_name} {self.last_name}")

class image_test(models.Model):
    name = models.CharField(max_length=64,default='test')
    image = models.ImageField(upload_to='images/')

class team_names(models.Model):
    team_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    def __str__(self):
          return self.name
    
class grader_names(models.Model):
    grader_id = models.AutoField(primary_key=True)
    grader_name = models.CharField(max_length=100)
    def __str__(self):
          return self.grader_name
    
class cardz(models.Model):
	card_id = models.AutoField(primary_key=True)
	year = models.PositiveIntegerField(null=True)
	set_name = models.CharField(max_length=500)
	player_name = models.CharField(max_length=500)
	autographed = models.BooleanField(default=False,null=True)
	graded = models.BooleanField(default=False,null=True)
	grade = models.PositiveIntegerField(null=True)
	parallel = models.BooleanField(default=False,null=True)
	parallel_number = models.IntegerField(null=True)
	parallel_name = models.CharField(max_length=500,null=True)
	average_price = models.DecimalField(max_digits=10, decimal_places=2)
	card_img_url = models.CharField(max_length=500,null=True)
	search_criteria = models.CharField(max_length=500)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True,null=True)
	grader = models.ForeignKey(grader_names, on_delete=models.CASCADE,null=True, blank=True) 
	user = models.ForeignKey(User, on_delete=models.CASCADE) 
	team = models.ForeignKey(team_names, on_delete=models.CASCADE) 

class card_user_table(models.Model):
	card_id = models.AutoField(primary_key=True)
	year = models.PositiveIntegerField(null=True)
	set_name = models.CharField(max_length=500)
	player_name = models.CharField(max_length=500)
	autographed = models.BooleanField(default=False,null=True)
	graded = models.BooleanField(default=False,null=True)
	grade = models.PositiveIntegerField(null=True)
	parallel = models.BooleanField(default=False,null=True)
	parallel_name = models.CharField(max_length=500,null=True)
	parallel_number = models.IntegerField(null=True)
	average_price = models.DecimalField(max_digits=10, decimal_places=2)
	card_img_url = models.CharField(max_length=500,null=True)
	search_criteria = models.CharField(max_length=500)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True,null=True)
	grader = models.ForeignKey(grader_names, on_delete=models.CASCADE,null=True, blank=True) 
	user = models.ForeignKey(User, on_delete=models.CASCADE) 
	team = models.ForeignKey(team_names, on_delete=models.CASCADE) 
      



class years(models.Model):
    year_id = models.AutoField(primary_key=True)
    year = models.PositiveIntegerField()

    def __str__(self):
        return str(self.year)