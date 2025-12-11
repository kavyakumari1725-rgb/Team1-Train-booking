from rest_framework import viewsets, permissions
from .models import Train, Ticket
from .serializers import TrainSerializer, TicketSerializer

class TrainViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Train.objects.all()
    serializer_class = TrainSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = super().get_queryset()
        source = self.request.query_params.get('source')
        destination = self.request.query_params.get('destination')
        if source:
            qs = qs.filter(source__icontains=source)
        if destination:
            qs = qs.filter(destination__icontains=destination)
        return qs

class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
