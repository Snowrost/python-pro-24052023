from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from stock.tasks import long_calculation


class TaskView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        result = long_calculation.apply_async(args=[request.data["x"], request.data["y"]])
        return Response(data=str(result), status=204)
