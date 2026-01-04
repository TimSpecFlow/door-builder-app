from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import EstimateSerializer


class EstimateView(APIView):
    """Return a simple price estimate based on area and options."""

    MATERIAL_MULTIPLIERS = {
        'wood': 1.0,
        'steel': 1.5,
        'fiberglass': 1.2,
    }

    HARDWARE_COSTS = {
        'hinges': 10,
        'handle': 25,
        'lockset': 40,
    }

    def post(self, request):
        ser = EstimateSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

        data = ser.validated_data
        width = data['width']
        height = data['height']
        material = data.get('material', 'wood')
        hardware = data.get('hardware', [])

        # Simple area-based pricing (square feet)
        area_sqft = (width * height) / 144.0
        base_price_per_sqft = 50.0
        multiplier = self.MATERIAL_MULTIPLIERS.get(material.lower(), 1.0)

        price = area_sqft * base_price_per_sqft * multiplier

        # Add hardware costs
        for h in hardware:
            price += self.HARDWARE_COSTS.get(h.lower(), 0)

        return Response({'estimate': round(price, 2)})
