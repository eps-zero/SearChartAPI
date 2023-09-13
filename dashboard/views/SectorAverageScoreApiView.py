from collections import defaultdict
from rest_framework.views import APIView
from dashboard.models import Country, Sect
from dashboard.serializers import CountrySerializer
from rest_framework.response import Response
from django.db.models import Max
from .AverageScoreIndicaApiView import AverageScoreIndicaApiView
import json
from operator import itemgetter


class SectorAverageScoreApiView(APIView):
    serializer_class = CountrySerializer

    def get(self, request):
        selected_country = request.GET.get("country")
        selected_year = request.GET.get("year")

        data = self.get_sector_average_score(
            selected_country, selected_year).data
        total_percentile_average = sum(item["average_score"] for item in data)
        if len(data):
            average_score = total_percentile_average / len(data)
        else:
            average_score = 0

        result = {"country": selected_country,
                  "average_score": round(average_score, 2)}
        return Response(result)

    def get_sector_average_score(self, country, year):

        request = self.request._request
        request.GET = request.GET.copy()
        request.GET["country"] = country
        request.GET["year"] = year

        view = AverageScoreIndicaApiView.as_view()
        response = view(request)

        return response
