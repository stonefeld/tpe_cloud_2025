from rest_framework import permissions, viewsets
from django.shortcuts import get_object_or_404

from .models import Pool, Request
from .serializers import PoolSerializer, RequestSerializer


class PoolViewSet(viewsets.ModelViewSet):
    queryset = Pool.objects.select_related("product").all()
    serializer_class = PoolSerializer
    permission_classes = [permissions.AllowAny]


class RequestViewSet(viewsets.ModelViewSet):
    serializer_class = RequestSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        pool_id = self.kwargs.get('pool_pk')
        return Request.objects.filter(pool_id=pool_id).select_related("pool")
    
    def perform_create(self, serializer):
        pool_id = self.kwargs.get('pool_pk')
        pool = get_object_or_404(Pool, pk=pool_id)
        serializer.save(pool=pool)
