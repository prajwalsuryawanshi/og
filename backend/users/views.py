from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib import messages

# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            messages.success(request,f'Welcome {user.username}, your account has been created successfully!')
            return request('home')
    else: 
        form= UserCreationForm()

    return render(request,'signup.html',{'form':form})

class CustomLoginView(LoginView):
    template_name= 'login.html'

    def form_valid(self,form):
        messages.success(self.request,f'Welcome back, {self.request.user.username}!')
        return super().form_valid(form)