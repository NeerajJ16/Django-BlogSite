from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact
from home.models import ByArticle
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from blog.models import Post
# Create your views here.
def home(request):
    return render(request, 'home/home.html')


def contact(request):
    
    if request.method=='POST':
        name= request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        content=request.POST['content']

        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<3:
            messages.warning(request, 'Please fill form correctly! Thank You.')
        else:    
            contact= Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, 'Thank you for Contacting us. We will connect to you soon!')
    return render(request, 'home/contact.html')
 

def article(request):

    if request.method=='POST':
        name= request.POST['name']
        email=request.POST['email']
        content=request.POST['content']

        if len(name)<2 or len(email)<3 or len(content)<3:
            messages.warning(request, 'Please fill form correctly! Thank You.')
        else:    
            byarticle= ByArticle(name=name, email=email,content=content)
            byarticle.save()
            messages.success(request, 'Thank you for Submitting your Article! We will soon publish your article after verification process!')
    return render(request, 'home/about.html')

def search(request):
    query=request.GET['query']
    allPosts = Post.objects.filter(title__icontains=query) 
    params={'allPosts':allPosts, 'query':query}
    return render(request, 'home/search.html', params)


def handleSignup(request):
    if request.method == 'POST':
        #Get the post parameters
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        #checks for error inputs
        if len(email)<8:
            messages.warning(request, "Inncorrect Email.Please Try Again!")
            return redirect('home')
        
        if pass1 != pass2:
            messages.warning(request, "Passwords Didn't Match!! Try Again")
            return redirect('home')
        
        #Create User
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name  = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Welcome to BlogSite Family! Your Account is Created")
        return redirect('home')

    else:
        return HttpResponse('404 - Not Found')
    
def handleLogin(request):
    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']
        user = authenticate(username=loginusername, password=loginpassword)

        if user is not None:
            login(request, user)
            messages.success(request, "Welcome Back! You are successfully Logged In")
            return redirect('home')
        else:
            messages.warning(request, "Sorry your Credentials didn't matched!!Please do try again or Reach us for password reset:-)")
            return redirect('home')


def handleLogout(request):
        logout(request)
        messages.success(request, "Successfully logged out!!")
        return redirect('home')