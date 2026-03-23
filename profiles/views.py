from cProfile import Profile

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
            return redirect('home')
        else:
           
            if not User.objects.filter(username=u_name).exists():
                
                new_user = User.objects.create_user(username=u_name, email=u_email, password=p_word)
                new_user.save()
                
                
                login(request, new_user)
                
               
                return redirect('register') 
            else:
                
                return render(request, 'home/profiles/login.html', {'error': 'Ghalat Password! Kripya sahi password dalein.'})
            
    return render(request, 'home/profiles/login.html')

def register_view(request):
    if request.method == "POST":
        # Details uthao form se
        u_age = request.POST.get('age')
        u_state = request.POST.get('state')
        u_income = request.POST.get('annualincome')
        u_category = request.POST.get('category')
        u_gender = request.POST.get('gender')
        u_occupation = request.POST.get('occupation')
        

        profile, created = Profile.objects.get_or_create(user=request.user)
        profile.age = u_age
        profile.state = u_state
        profile.annual_income = u_income
        profile.gender = u_gender
        profile.occupation = u_occupation
        profile.save()
        # Yahan aap in details ko save karenge (Database Models mein)
        # Abhi ke liye hum sirf redirect kar rahe hain
        return redirect('home')

    return render(request, 'home/profiles/register.html')