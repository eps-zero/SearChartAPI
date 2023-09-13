from collections import defaultdict
from rest_framework.views import APIView
from dashboard.models import Country
from dashboard.serializers import CountrySerializer
from rest_framework.response import Response
from django.db.models import Max 


class SectorYearScoreApiView(APIView):
    serializer_class = CountrySerializer

    def get(self, request):
        sector = request.GET.get("sector")
        country = request.GET.get("country")

        queryset = (Country.objects.filter(
            indicator__sector__sector=sector)
            .prefetch_related("indicator__subsector__sector")
            .values("country", "indicator__indicator", "indicator__sector__sector", "year", "rank")
        )

        country_rank_annotations = queryset.filter(country=country).values(
            "indicator__indicator", "indicator__sector__sector", "year", "rank")

        max_rank_annotations = queryset.values(
            'indicator__indicator', 'year').annotate(max_rank=Max('rank'))

        max_rank_dict = {(item['indicator__indicator'], item['year']): item['max_rank'] for item in max_rank_annotations}

        percentile_by_year = defaultdict(dict)

        for item in country_rank_annotations:
            indicator_name = item['indicator__indicator']
            rank = item['rank']
            year = item['year']

            max_rank = max_rank_dict.get((indicator_name, year))

            if year not in percentile_by_year:
                percentile_by_year[year] = []

            percentile = (1 - (rank / max_rank)) * 100
            percentile_by_year[year].append(percentile)

        result = []

        for year, percentile_list in percentile_by_year.items():
            if percentile_list:
                percentile_average = sum(
                    percentile_list) / len(percentile_list)
                result.append({
                    'year': year,
                    'score': round(percentile_average, 2)
                })
        sorted_result = sorted(result, key=lambda x: x['year'])
        return Response(sorted_result)
