from rest_framework import serializers

from .models import Pool, Request


class PoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pool
        fields = ["id", "product", "start_at", "end_at", "min_quantity", "created_at", "updated_at"]


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ["id", "pool", "email", "quantity", "created_at"]
        read_only_fields = ["pool"]  # Pool is set automatically in perform_create
