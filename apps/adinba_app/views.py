from django.shortcuts import render, redirect, HttpResponse
from django.db import models
from models import *
from django.contrib import messages
import re
import bcrypt
import datetime
import time

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$')

# Create your views here.

def index(request):
    featured_events = Event.objects.filter(pending = False).order_by('created_at')[:2]
    content = {
        'featured_events': featured_events
    }
    return render(request, 'adinba_app/index.html', content)

def admin_dashboard(request):
    return render(request, 'adinba_app/admin_dashboard.html')

def admin_pending(request):
    pending_events = Event.objects.filter(pending = True)
    content = {
        'pending_events': pending_events
    }
    return render(request, 'adinba_app/pending.html', content)

def owner_dashboard(request):
    return render(request, 'adinba_app/owner_dashboard.html')

def user_dashboard(request):
    return render(request, 'adinba_app/owner_dashboard.html')

def events(request):
    events = Event.objects.filter(pending = False)
    content = {
        'events': events
    }
    return render(request, 'adinba_app/event.html', content)

def approve_event(request):
    approve = Event.objects.get(id = request.POST['id'])
    approve.pending = False
    approve.save()
    messages.success(request, "Successfully approved this event!")
    return redirect(admin_pending)

def login(request):
    if 'user' in request.session:
        messages.error(request, "You are already logged in!")
        return redirect(index)
    return render(request, 'adinba_app/login.html')

def process_login(request):
    user = User.objects.filter(email = request.POST['email'])
    if not user:
        messages.error(request, 'Invalid Login Information!')
        return redirect(index)
    else:
        if bcrypt.checkpw(request.POST['password'].encode(), user[0].password.encode()):
            # messages.success(request, 'Successfully Logged In!')
            # request.session['user'] = user
            session_user = {
                'first_name': user[0].first_name,
                'last_name': user[0].last_name,
                'email': user[0].email,
                'business_owner': user[0].business_owner,
                'id': user[0].id
            }
            request.session['user'] = session_user
            if request.session['user']['id'] == 1:
                return redirect(admin_dashboard)
            if request.session['user']['business_owner'] == True:
                return redirect(owner_dashboard)
            else:
                return redirect(index)
        else:
            messages.error(request, 'Invalid Login Information!')
            return redirect(login)

def register(request):
    if 'user' in request.session:
        messages.error(request, "You are already logged in! Please contact an admin if you forgot your password!")
        return redirect(index)
    return render(request, 'adinba_app/register.html')

def process_registration(request):
    error = False
    if len(request.POST['first_name']) < 2 or len(request.POST['first_name']) < 2:
        messages.error(request, 'First and Last names must be longer than 2 characters!')
        error = True
    if not request.POST['first_name'].isalpha() or not request.POST['last_name'].isalpha():
        messages.error(request, 'First and last must be alphabets!')
        error = True
    if not EMAIL_REGEX.match(request.POST['email']):
        messages.error(request, 'Please enter a valid e-mail address!')
        error = True
    emails = User.objects.filter(email = request.POST['email'])
    if emails:
        messages.error(request, 'This email is already taken!')
        error = True
    if not PASSWORD_REGEX.match(request.POST['password']):
        messages.error(request, 'Password must be 8 or more characters, contain at least 1 upper case and 1 number!')
        error = True
    if request.POST['password'] != request.POST['password_confirm']:
        messages.error(request, 'Passwords must match!')
        error = True
    if error:
        return redirect(register)
    else: 
        # print bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        User.objects.create(primary_number = '', secondary_number = '', business_owner = False, first_name = request.POST['first_name'], last_name = request.POST['last_name'],email = request.POST['email'], password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()))
        # request.session['user'] = User.objects.last()
        session_user = {
            'first_name': request.POST['first_name'],
            'last_name': request.POST['last_name'],
            'email': request.POST['email'],
            'id': User.objects.last().id
        }
        request.session['user'] = session_user
        messages.success(request, "Thank you for registering to Adinba.com! You can request to be verified as a business owner to start promoting your business!")
        return redirect(index)

def logout(request):
    if 'user' in request.session:
        request.session.pop('user')
        messages.success(request, 'Successfully Logged Out!')
    return redirect(index)

def terms(request):
    return render(request, 'adinba_app/terms.html')

def privacy(request):
    return render(request, 'adinba_app/privacy.html')