from django.contrib import admin
from .models import Train, Ticket, Payment

@admin.register(Train)
class TrainAdmin(admin.ModelAdmin):
    list_display = ('name', 'source', 'destination', 'departure_time', 'seats_available')
    search_fields = ('name', 'source', 'destination')

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('pnr', 'user', 'train', 'booked_on', 'seats', 'status')
    search_fields = ('pnr', 'user__username', 'train__name')
    list_filter = ('status',)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'amount', 'status', 'payment_method', 'created_at')
    list_filter = ('status', 'payment_method')
