from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from todo import models
from todo.models import Todoo
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

def signup(request):
    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        email = request.POST.get('email')
        pdw = request.POST.get('pwd')
        print(fnm,email,pdw)

        my_user = User.objects.create_user(fnm,email,pdw)
        my_user.save()
        return redirect('/login')


    return render(request, 'signup.html')

def login_user(request):
    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        pwd = request.POST.get('pwd')
        print(fnm, pwd)
        userr = authenticate(request, username=fnm, password=pwd)
        if userr is not None:
            login(request, userr)
            return redirect('/todo')
        else:
            return redirect('/login')

    return render(request, 'login.html')

@login_required(login_url='/login')
def todo(request):
    if request.method == "POST":
        title = request.POST.get('title')
        print(title)
        obj = models.Todoo(title=title, user = request.user)
        obj.save()
        res = models.Todoo.objects.filter(user=request.user).order_by('-date')
        return redirect('/todo', {'res':res})
    res = models.Todoo.objects.filter(user=request.user).order_by('-date')
    return render(request, 'todo.html', {'res':res})

@login_required(login_url='/login')
def edit_todo(request, srno):
    if request.method == "POST":
        title = request.POST.get('title')
        print(title)
        obj = models.Todoo.objects.get(srno = srno)
        obj.title = title
        obj.save()
        return redirect('/todo', {'obj':obj})
    
    obj = models.Todoo.objects.get(srno = srno)
    return render(request, 'edit_todo.html',{'obj':obj} )

def delete_todo(request, srno):
        
    obj = models.Todoo.objects.get(srno = srno)
    obj.delete()
    return redirect('/todo')

def signout(request):
    logout(request)
    return redirect('/login')
    