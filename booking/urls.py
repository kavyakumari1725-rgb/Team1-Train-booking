from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.create_account, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('search/', views.search_trains, name='search_trains'),
    path('book/<int:train_id>/', views.book_ticket, name='book_ticket'),
    path('tickets/', views.my_tickets, name='my_tickets'),
    path('ticket/<str:pnr>/', views.ticket_detail, name='ticket_detail'),
]
