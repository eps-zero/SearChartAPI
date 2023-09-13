from collections import defaultdict
from rest_framework.views import APIView
from dashboard.models import Country, Sect
from dashboard.serializers import CountrySerializer
from rest_framework.response import Response
from django.db.models import Max
from operator import itemgetter


class AverageScoreIndicaApiView(APIView):
    serializer_class = CountrySerializer

    def get(self, request):
        selected_country = request.GET.get("country")
        selected_year = request.GET.get("year")

        sectors = Sect.objects.all().values_list('sector', flat=True)

        queryset = (Country.objects.filter(
            year=selected_year,
            indicator__sector__sector__in=sectors)
            .prefetch_related("indicator__subsector__sector")
            .values("country", "indicator__indicator", "indicator__sector__sector", "year", "rank")
        )

        country_rank_annotations = queryset.filter(country=selected_country).values(
            "indicator__indicator", "indicator__sector__sector", "year", "rank")

        max_rank_annotations = queryset.values(
            'indicator__indicator', 'year').annotate(max_rank=Max('rank'))

        max_rank_dict = {(item['indicator__indicator'], item['year']): item['max_rank'] for item in max_rank_annotations}

        result = []

        for sector in sectors:

            count = 0
            all_percentile = 0

            for item in country_rank_annotations:
                year = item['year']
                indicator_name = item['indicator__indicator']
                rank = item['rank']

                max_rank = max_rank_dict.get((indicator_name, year))

                if item['indicator__sector__sector'] == sector:
                    all_percentile += (1 - (rank / max_rank)) * 100
                    count += 1
                    
            if count:
                percentile_average = all_percentile/count
                result.append({
                    'sector': sector,
                    'average_score': round(percentile_average, 2)
                })

        return Response(result)
