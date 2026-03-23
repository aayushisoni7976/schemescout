from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    # Yeh line is profile ko specific user se connect karti hai
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Aapke required fields
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], null=True)
    state = models.CharField(max_length=50, null=True)
    occupation = models.CharField(max_length=100, null=True)
    annual_income = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    category = models.CharField(max_length=50, null=True) # General/OBC/SC/ST

    def __str__(self):
        return f"{self.user.username}'s Profile"