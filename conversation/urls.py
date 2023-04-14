from django.urls import path
from . import views

app_name="conversation"

urlpatterns=[
    path('conversation/inbox/',views.inbox,name="inbox"),
    path('conversation/<int:pk>/', views.detail, name='detail'),
    path("new/<int:item_pk>",views.new_conversation,name="new")
]