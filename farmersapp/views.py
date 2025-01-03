from django.http import JsonResponse
from django.shortcuts import render, redirect
import openai
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Chat
from django.utils import timezone
import urllib.request
import json

openai_api_key = '##'
openai.api_key = openai_api_key


def ask_openai(message):
    response = openai.chat.completions.create(
        model = "gpt-3.5-turbo",
        #prompt = message, 
        #max_tokens=150, 
        #n=1, 
        #stop=None,
        #temperature=0.7,
        messages=[
            {"role": "system", "content": "You are an agriculture expert,you only answer questions related to agriculture only. Yoy ignore the rest of the questions by giving a polite response. You can respond to greeting and weather forecast related questions"},
            {"role": "user", "content": message},
        ]
    )
    
    answer = response.choices[0].message.content.strip()
    return answer 


def chatbot(request):
    chats = Chat.objects.filter(user=request.user)
    if request.method == "POST":
        message = request.POST.get('message')
        response = ask_openai(message)
        
        chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatbot.html', {'chats': chats})

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('dashboard')
        else:
            error_message = 'Invalid Username or Password'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.first_name = fname
                user.last_name = lname
                
                user.save()
                auth.login(request, user)
                return redirect('dashboard')
            except:
                error_message = 'Please try again'
                return render(request, 'register.html', {'error_message': error_message})
        else:
            error_message = 'Passwords dont match'
            return render(request, 'register.html', {'error_message': error_message})
    return render(request, 'register.html')
        #if User.objects.filter(username=username):
            #error_message = 'Username already exists'
            #return render(request, 'register.html', {'error_message': error_message})
        #if password1 != password2:
            #error_message = 'Passwords do not match'
            #return render(request, 'register.html', {'error_message': error_message})
        #if User.objects.filter(email=email):
            #error_message ='Email already exist'
            #return render(request, 'register.html', {'error_message': error_message})
        
        #user = User.objects.create_user(username, email, password1)
        #user.first_name = fname
        #user.last_name = lname
           
        #user.save()
        #auth.login(request, user)
        #return redirect('dashboard')
        
            

def logout(request): 
    auth.logout(request)
    return redirect('login')

def dashboard(request):
    return render(request, 'dashboard.html')

def forecast(request):
        if request.method == 'POST':
           city = request.POST['city']

           source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q=' +
                                        city + '&units=metric&appid#').read()
           list_of_data = json.loads(source)
           
           data ={
               "country_code": str(list_of_data['sys']['country']),
               #"coordinate": int(list_of_data)['coord']['lon'] + ', '+ int(list_of_data['coord']['lat']),
               #"temp": float(list_of_data['main']['temp'] + ' C'),
               "pressure": str(list_of_data['main']['pressure']),
               "humidity": str(list_of_data['main']['humidity']),
               'main': str(list_of_data['weather'][0]['main']),
               'description':str(list_of_data['weather'][0]['description']),
               'icon': list_of_data['weather'][0]['icon'],
               
           }
           #print(data)
           return render(request, 'forecast.html', data)
        else:
            data = {}
            
        return render(request, "forecast.html", data)

           
     
