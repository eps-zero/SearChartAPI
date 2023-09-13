from rest_framework import serializers
from dashboard.models import Sect


class SectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sect
        fields = "__all__"
