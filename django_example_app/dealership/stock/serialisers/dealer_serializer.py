from rest_framework import serializers

from stock.models import Dealer

from .user_serializer import UserSerializer


class DealerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dealer
        fields = ["id", "name", "owner"]

    def to_representation(self, instance):
        self.fields["owner"] = UserSerializer(read_only=True)
        return super(DealerSerializer, self).to_representation(instance)
