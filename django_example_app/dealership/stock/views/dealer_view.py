from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from stock.models import Dealer
from stock.permissions import IsOwner
from stock.serialisers import DealerSerializer


class DealerView(APIView):
    permission_classes = [IsOwner, IsAuthenticated]

    def get(self, request, pk=None):
        if not pk:
            dealers = Dealer.objects.filter(owner=request.user)
            serializer = DealerSerializer(dealers, many=True)
            return Response(serializer.data)

        dealer = get_object_or_404(Dealer, pk=pk)
        self.check_object_permissions(self.request, dealer)
        return Response(DealerSerializer(dealer).data)
