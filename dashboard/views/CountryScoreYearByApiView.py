from collections import defaultdict
from rest_framework.views import APIView
from dashboard.models import Country, Sect
from dashboard.serializers import CountrySerializer
from rest_framework.response import Response
from .SectorAverageScoreApiView import SectorAverageScoreApiView
from django.db.models import Max
from operator import itemgetter


class CountryScoreYearByApiView(APIView):
    serializer_class = CountrySerializer

    def get(self, request):
        country = request.GET.get("country")
        sectors = Sect.objects.all().values_list('sector', flat=True)

        queryset = (Country.objects.all()
                    .prefetch_related("indicator__subsector__sector")
                    .values("country", "indicator__indicator", "indicator__sector__sector", "year", "rank")
                    )

        country_rank_annotations = queryset.filter(country=country).values(
            "indicator__indicator", "indicator__sector__sector", "year", "rank")

        max_rank_annotations = queryset.values(
            'indicator__indicator', 'year').annotate(max_rank=Max('rank'))

        max_rank_dict = {(item['indicator__indicator'], item['year'])
                          : item['max_rank'] for item in max_rank_annotations}

        percentile_by_year_sector = defaultdict(lambda: defaultdict(list))
        for sector in sectors:
            for item in country_rank_annotations:
                indicator_name = item['indicator__indicator']
                sector_name = item['indicator__sector__sector']
                rank = item['rank']
                year = item['year']

                if sector == sector_name:
                    max_rank = max_rank_dict.get((indicator_name, year))

                    percentile = (1 - (rank / max_rank)) * 100

                    percentile_by_year_sector[year][sector].append(percentile)

        result = []

        for year, sector_percentile_list in percentile_by_year_sector.items():
            year_result = []
            for sector, percentile_list in sector_percentile_list.items():
                if percentile_list:
                    percentile_average = sum(
                        percentile_list) / len(percentile_list)
                    year_result.append({
                        'sector': sector,
                        'score': round(percentile_average, 2)
                    })

            year_average = sum(item["score"]
                               for item in year_result)/len(year_result)
            result.append({
                'year': year,
                'score': round(year_average, 2)
            })

        sorted_result = sorted(result, key=lambda x: x['year'])
        return Response(sorted_result)
