from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date # DOB calculation ke liye zaroori hai

class Profile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    # Yeh line is profile ko specific user se connect karti hai
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Aapke required fields
    full_name = models.CharField(max_length=100, null=True) # Display ke liye
    
    # Age hata kar Date of Birth add kiya hai
    date_of_birth = models.DateField(null=True, blank=True) 
    
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True)
    state = models.CharField(max_length=50, null=True)
    district = models.CharField(max_length=50, null=True) # Specific schemes ke liye
    occupation = models.CharField(max_length=100, null=True)
    annual_income = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    category = models.CharField(max_length=50, null=True) # General/OBC/SC/ST

    # Extra Fields jo humein Startup Idea ke liye chahiye
    phone_number = models.CharField(max_length=15, null=True, unique=True)
    preferred_language = models.CharField(max_length=20, default='English')
    
    # User ko kitni baar disturb karna hai
    notification_freq = models.CharField(
        max_length=20, 
        choices=[('Weekly', 'Weekly'), ('Instant', 'Instant')], 
        default='Weekly'
    )

    # Dynamic Age calculation logic (Har saal apne aap update hoga)
    @property
    def current_age(self):
        if self.date_of_birth:
            today = date.today()
            return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return 0

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Ensure profile exists before saving
    if hasattr(instance, 'profile'):
        instance.profile.save()