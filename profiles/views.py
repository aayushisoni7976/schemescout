from .models import Profile

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

def login_view(request):
    if request.method == "POST":
        u_name = request.POST.get('username')
        p_word = request.POST.get('password')
        u_email = request.POST.get('email')

        
        user = authenticate(request, username=u_name, password=p_word)

        if user is not None:
           
            login(request, user)
            profile, created = Profile.objects.get_or_create(user=user)
            if not profile.date_of_birth: # Agar date_of_birth None hai
                return redirect('register') # Toh details bharne bhejo
            return redirect('dashboard') # Warna dashboard pe bhejo
            
        else:
            # Naya user banane ka logic (Registration)
            if not User.objects.filter(username=u_name).exists():
                u_email = request.POST.get('email')
                new_user = User.objects.create_user(username=u_name, email=u_email, password=p_word)
                login(request, new_user)
                return redirect('register')
            else:
                return render(request, 'home/profiles/login.html', {'error': 'Ghalat Password!'})
            
    return render(request, 'home/profiles/login.html')

def register_view(request):
    if request.method == "POST":
        # Details uthao form se
        u_dob = request.POST.get('dob')
        u_state = request.POST.get('state')
        u_income = request.POST.get('annualincome')
        u_category = request.POST.get('category')
        u_gender = request.POST.get('gender')
        u_occupation = request.POST.get('occupation')
        u_fullname = request.POST.get('fullname')
        

        profile, created = Profile.objects.get_or_create(user=request.user)

        profile.date_of_birth = request.POST.get('dob')

      
        profile.state = u_state
        profile.annual_income = u_income
        profile.gender = u_gender
        profile.occupation = u_occupation
        profile.category = u_category
        profile.full_name = u_fullname
        profile.save()
        # Yahan aap in details ko save karenge (Database Models mein)
        # Abhi ke liye hum sirf redirect kar rahe hain
     
        return redirect('dashboard')
    return render(request, 'home/profiles/register.html')