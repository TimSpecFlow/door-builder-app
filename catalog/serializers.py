from rest_framework import serializers


class EstimateSerializer(serializers.Serializer):
    width = serializers.FloatField(min_value=0.1)
    height = serializers.FloatField(min_value=0.1)
    material = serializers.CharField(default='wood')
    hardware = serializers.ListField(child=serializers.CharField(), required=False)
