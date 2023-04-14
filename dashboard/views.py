from django.shortcuts import render,get_object_or_404,redirect
from item.models import Item
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
# Create your views here.
from django.contrib.auth.decorators import user_passes_test

def user_can_access_item(user):
    return user.is_authenticated

def user_can_access_dashboard(user):
    return user.is_authenticated and user.is_staff

@login_required(login_url="user:login")
@user_passes_test(user_can_access_dashboard, login_url='user:login')
def index(request):
    items=Item.objects.filter(created_by=request.user)
    return render(request,"dashboard/index.html",{"items":items})
