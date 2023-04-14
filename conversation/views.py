from django.shortcuts import render,get_object_or_404,redirect
from item.models import Item
from .models import Conversation
from.forms import ConversationMessageForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.
@login_required(login_url="user:login")
def new_conversation(request,item_pk):
    item=get_object_or_404(Item,pk=item_pk)
    conversations=Conversation.objects.filter(item=item, members=request.user)
    if conversations:
        pass
    if request.method=="POST":
        form=ConversationMessageForm(request.POST)
        if form.is_valid():
            conversation=Conversation.objects.create(item=item)
            conversation.members.add(request.user)
            conversation.members.add(item.created_by)
            conversation.save()
            conversation_message=form.save(commit=False)
            conversation_message.conversation=conversation
            conversation_message.created_by=request.user
            conversation_message.save()
            messages.success(request,"Message Sent Successfully")
            return redirect("item:detail",pk=item_pk)
    else:
        form=ConversationMessageForm()
    return render(request,"conversation/new.html",{"form":form})

@login_required(login_url="user:login")
def inbox(request):
    conversations=Conversation.objects.filter(members=request.user)
    return render(request,"conversation/inbox.html",{"conversations":conversations})

@login_required(login_url="user:login")
def detail(request,pk):
    conversation=Conversation.objects.filter(members=request.user).get(pk=pk)
    form=ConversationMessageForm()
    if request.method == "POST":
        form=ConversationMessageForm(request.POST)
        if form.is_valid():
            conversation_message=form.save(commit=False)
            conversation_message.conversation=conversation
            conversation_message.created_by=request.user
            conversation_message.save()
            conversation.save()
            return redirect('conversation:detail',pk=pk)
    return render(request,"conversation/detail.html",{"conversation":conversation,"form":form})




