from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Train, Ticket, Payment

def home(request):
    return redirect('search_trains')

def create_account(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created. Please log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'booking/create_account.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('search_trains')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'booking/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def search_trains(request):
    trains = Train.objects.all()
    source = destination = ''
    if request.method == 'POST':
        source = request.POST.get('source', '')
        destination = request.POST.get('destination', '')
        trains = trains.filter(source__icontains=source, destination__icontains=destination)
    return render(request, 'booking/search.html', {
        'trains': trains,
        'source': source,
        'destination': destination,
    })

@login_required
def book_ticket(request, train_id):
    train = get_object_or_404(Train, id=train_id)
    if request.method == 'POST':
        try:
            seats = int(request.POST.get('seats', '1'))
        except ValueError:
            seats = 1
        if seats <= 0:
            messages.error(request, 'Seats must be at least 1')
        elif seats > train.seats_available:
            messages.error(request, 'Not enough seats available')
        else:
            ticket = Ticket.objects.create(user=request.user, train=train, seats=seats)
            train.seats_available -= seats
            train.save()
            amount = seats * 100  # simple price logic
            payment = Payment.objects.create(ticket=ticket, amount=amount, status='SUCCESS')
            messages.success(request, f'Ticket booked! PNR: {ticket.pnr}')
            return redirect('ticket_detail', pnr=ticket.pnr)
    return render(request, 'booking/book.html', {'train': train})

@login_required
def ticket_detail(request, pnr):
    ticket = get_object_or_404(Ticket, pnr=pnr, user=request.user)
    return render(request, 'booking/ticket_detail.html', {'ticket': ticket})

@login_required
def my_tickets(request):
    tickets = Ticket.objects.filter(user=request.user).order_by('-booked_on')
    return render(request, 'booking/my_tickets.html', {'tickets': tickets})
