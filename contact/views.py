from django.shortcuts import render, redirect
from .models import Contact, User
from .forms import ContactForm, UserForm
from django.views.generic import ListView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class ContactList(ListView):
    model = Contact
    context_object_name = 'contacts'
    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, *args, **kwargs):
        return super(ContactList, self).dispatch(*args, **kwargs)


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('contact-list')
        else:
            return render(request, 'contact/login.html', {'error' : 'Incorrect username or password'})
    else:
        return render(request, 'contact/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def signup(request):
    if request.method == "POST":
    	error = None
        username = request.POST.get('username', None)
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)

        if username == "" or password == "" or email == "":
            error = "username, email, password can't be blank."
            return render(request, 'contact/register.html', {'error': error})

        try:
            user = User.objects.get(username=username)
        except:
            user = None

        if user is not None:
            error = "username already taken"
            return render(request, 'contact/register.html', {'error': error})

        try:
            user = User.objects.get(email=email)
        except:
            user = None

        if user is not None:
            error = "Email already taken"
            return render(request, 'contact/register.html', {'error': error})

        user = User(username=username, email=email)
        user.set_password(password)
        user.save()
        return redirect('login')
    else:    
        return render(request, 'contact/register.html')