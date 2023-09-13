from rest_framework import serializers
from dashboard.models import Country


class RankDiffrenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ("country", "rank", "year")
