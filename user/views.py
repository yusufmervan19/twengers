from django.shortcuts import render,redirect
from .forms import RegisterForm,LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
# Create your views here.
def register(request):

    
    if request.method=="POST":
        form=RegisterForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get("username")
            password=form.cleaned_data.get("password")
            newUser=User(username=username)
            newUser.set_password(password)
            newUser.save()
            login(request,newUser)
            messages.success(request,"Başarıyla Kayıt olundu")

            return redirect("index")
        context={
            "form":form
        }

        return render(request,"register.html",context)
        
        
    else:

        form=RegisterForm()
        context={
            "form":form
        }

        return render(request,"register.html",context)
        



def loginUser(request):
    form=LoginForm(request.POST or None)
    context={"form":form}
    if form.is_valid():
        username=form.cleaned_data.get("username")
        password=form.cleaned_data.get("password")
        user=authenticate(username=username,password=password)
        if user is None:
            messages.warning(request,"Kullanıcı adı veya Parola Yanlış...")
            return render(request,"login.html",context)
        else:
            messages.success(request,"Başarıyla Giriş Yapıldı...")
            login(request,user)
            return redirect("index")
    else:
        return render(request,"login.html",context)
    return render(request,"login.html")




def logoutUser(request):
    logout(request)
    messages.info(request,"Çıkış Yapıldı...")
    return redirect("index")