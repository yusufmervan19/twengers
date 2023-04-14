from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from .models import Item,Category
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import NewItem
from django.db.models import Q #Ürün Açıklamasından arama için
# Create your views here.
from django.contrib.auth.decorators import user_passes_test

def user_can_access_item(user):
    return user.is_authenticated

def user_can_access_dashboard(user):
    return user.is_authenticated and user.is_staff


def detail(request,pk):
    item=get_object_or_404(Item,pk=pk)
    related_items=Item.objects.filter(category=item.category,is_sold=False).exclude(pk=pk)[0:3]
    return render(request,"detail.html",{"item":item,"related_items":related_items})

@login_required(login_url="user:login")
def delete(request,pk):
    item=get_object_or_404(Item,pk=pk,created_by=request.user)
    item.delete()
    messages.success(request,"Ürün Başarıyla Silindi")
    return redirect("dashboard:index")


@login_required(login_url="user:login")
def edit(request,pk):
    item=get_object_or_404(Item,pk=pk,created_by=request.user)
    form=NewItem(request.POST or None,request.FILES or None,instance=item)
    if form.is_valid():
        item=form.save(commit=False)
        item.author=request.user
        item.save()
        messages.success(request,"Ürün Başarıyla Değiştirildi")
        return redirect("dashboard:index")
    return render(request,"update.html",{"form":form})


@login_required(login_url="user:login")
@user_passes_test(user_can_access_dashboard, login_url='user:login')
def new(request):
    form=NewItem(request.POST or None,request.FILES or None)
    if form.is_valid():
        item=form.save(commit=False)
        item.created_by=request.user
        item.save()
        messages.success(request,"Ürün Başarıyla Eklendi")
        return redirect("index")
    return render(request,"form.html",{"form":form})


def items(request):
    query=request.GET.get('query','')
    categories=Category.objects.all()
    category_id=request.GET.get("category",0)
    items=Item.objects.filter(is_sold=False)
    if category_id:
        items=items.filter(category_id=category_id)

    if query:
        items=items.filter(Q(name__icontains=query)|Q(description__icontains=query))

    return render(request,"items.html",{"items":items,"query":query,"categories":categories,"category_id":int(category_id)})


