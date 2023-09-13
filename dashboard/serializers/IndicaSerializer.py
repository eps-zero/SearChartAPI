from rest_framework import serializers
from dashboard.models import Indica


class IndicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indica
        fields = "__all__"
