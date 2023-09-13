from collections import defaultdict
from rest_framework.views import APIView
from dashboard.models import Country
from dashboard.serializers import CountrySerializer
from rest_framework.response import Response
from .SectorAverageScoreApiView import SectorAverageScoreApiView
from operator import itemgetter
from django.db.models import Avg, Max


class ScoreDifferenceTwoYearsApiView(APIView):
    serializer_class = CountrySerializer

    def get(self, request):
        selected_country = request.GET.get("country")
        year1 = request.GET.get("year1")
        year2 = request.GET.get("year2")

        response1 = self.get_sector_average_score(selected_country, year1)
        response2 = self.get_sector_average_score(selected_country, year2)

        data1 = response1.data
        data2 = response2.data

        results = {
            "country": selected_country,
            "score_difference": round(data2['average_score'] - data1['average_score'], 2),
        }

        return Response(results)

    def get_sector_average_score(self, country, year):
        # Создаем запрос к первому представлению для заданного года
        request = self.request._request
        request.GET = request.GET.copy()
        request.GET["country"] = country
        request.GET["year"] = year

        # Используем класс SectorAverageScoreApiView для обработки запроса
        view = SectorAverageScoreApiView.as_view()
        response = view(request)

        return response
