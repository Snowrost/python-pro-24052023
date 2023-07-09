from rest_framework import serializers

from stock.models import Car


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ["id", "name", "warehouse"]
        read_only_fields = ["created_date", "updated_date"]
