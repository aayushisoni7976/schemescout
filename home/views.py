from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from profiles.models import Profile
from .models import WhatsAppDocument # <-- Model Import (Zaroori hai)
from .ai_helper import get_scheme_recommendations
from .automation_handler import launch_govt_portal
import json
import re
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse
import requests
import os
from django.conf import settings
from django.core.files import File # <-- WhatsApp save ke liye
from django.core.files.temp import NamedTemporaryFile # <-- WhatsApp save ke liye


# 1. Landing Page
def home (request):
    return render(request, 'home/index.html')

# 2. Redirect Logic
@login_required
def login_redirect_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if not profile.date_of_birth:
        return redirect('register')
    return redirect('dashboard')

# 3. Merged Dashboard (Both Logics Together)
@login_required
def dashboard_view(request):
    profile = request.user.profile 
    ai_response = get_scheme_recommendations(profile)
    
    # --- WhatsApp Docs Fetching (Naya logic, sirf Vault ke liye) ---
    all_docs = WhatsAppDocument.objects.all().order_by('-uploaded_at')

    print("--- RAW AI RESPONSE START ---")
    print(ai_response)
    print("--- RAW AI RESPONSE END ---")

    # --- Cleaning logic (Same as yours) ---
    clean_ai_res = ai_response.replace('```json', '').replace('```', '').replace('[', '').replace(']', '').replace('{', '').replace('}', '').replace('"', '')

    # FIX: Yahan 're.escape' use kiya hai taaki [END_SCHEME] sahi se split ho
    schemes_raw = re.split(r'\[?\s*END_SCHEME\s*\]?', clean_ai_res, flags=re.IGNORECASE)
    schemes_list = []
    
    for block in schemes_raw:
        clean_block = block.strip()
        if len(clean_block) > 30:
            name = re.search(r'(?:NAME|name):\s*(.*)', clean_block)
            desc = re.search(r'(?:DESCRIPTION|description):\s*(.*)', clean_block)
            amount = re.search(r'(?:AMOUNT|amount):\s*(.*)', clean_block)
            match = re.search(r'(?:MATCH_SCORE|match_score):\s*(\d+)', clean_block)
            benefit = re.search(r'(?:BENEFIT|benefit):\s*(.*)', clean_block)
            link = re.search(r'(?:APPLY_LINK|apply_link):\s*(.*)', clean_block)

            schemes_list.append({
                'name': name.group(1).split(',')[0].strip() if name else "Scheme Name",
                'description': desc.group(1).split(',')[0].strip() if desc else "Details loading...",
                'amount': amount.group(1).split(',')[0].strip() if amount else "N/A",
                'match_score': match.group(1).strip() if match else "0",
                'benefit': benefit.group(1).split(',')[0].strip() if benefit else "General",
                'apply_link': link.group(1).split(',')[0].strip() if link else "#",
            })

    context = {
        'profile': profile,
        'ai_suggestions': ai_response,
        'schemes': schemes_list,      
        'schemes_count': len(schemes_list),
        'expiring_soon': 3,
        'documents': all_docs, # <-- Dashboard loop ke liye zaroori
        'docs_count': all_docs.count() # <-- Widget ke liye zaroori
    }
    return render(request, 'home/dash.html', context)

# 4. Automation Logic
@login_required
def apply_now_view(request, scheme_name):
    launch_govt_portal(scheme_name)
    return render(request, 'loading_portal.html', {'scheme': scheme_name})

# 5. WhatsApp Webhook (Now with Database Saving)
@csrf_exempt
@csrf_exempt
def whatsapp_webhook(request):
    if request.method == 'POST':
        print("--- MESSAGE RECEIVED FROM WHATSAPP ---")
        
        # Data nikalna
        msg_body = request.POST.get('Body', '').lower()
        sender = request.POST.get('From')
        user_name = request.POST.get('profile.full_name', 'User') # Dynamic name ke liye
        
        response = MessagingResponse()
        
        # --- 1. Agar User ne Photo bheji hai ---
        if request.POST.get('MediaUrl0'):
            media_url = request.POST.get('MediaUrl0')
            print(f"Downloading image from: {media_url}")

            try:
                # Photo download karne ka process
                img_temp = NamedTemporaryFile(delete=True)
                img_temp.write(requests.get(media_url).content)
                img_temp.flush()

                # Database mein save karna
                # 'sender' number aur download ki hui file save ho rahi hai
                new_doc = WhatsAppDocument(sender_number=sender)
                new_doc.image.save(f"wa_doc_{sender}.jpg", File(img_temp))
                new_doc.save()

                response.message(f"Photo mil gayi {user_name}! Aapke Document Vault mein save kar di hai. ✅ 📸")
            
            except Exception as e:
                print(f"Error saving image: {e}")
                response.message("Sorry, photo save karne mein problem hui. ❌")

        # --- 2. Agar sirf Text message hai ---
        elif 'hi' in msg_body or 'hello' in msg_body:
            response.message(f"Hello {user_name}! You are connected to SchemeScout's WhatsApp service. Send us a photo of your document to save it in your vault")
        
        else:
            response.message(f"Message mil gaya {user_name}! Agar aap photo bhejenge toh main use save kar loonga. 🤖")

        return HttpResponse(str(response), content_type='text/xml')

    return HttpResponse("Webhook is active!")