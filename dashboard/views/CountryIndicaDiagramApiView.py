from collections import defaultdict
from rest_framework.views import APIView
from dashboard.models import Country, Indica
from dashboard.serializers import CountrySerializer
from rest_framework.response import Response
from django.db.models import Max


class CountryIndicaDiagramApiView(APIView):
    serializer_class = CountrySerializer

    def get(self, request):
        selected_country = request.GET.get("country")
        sector = request.GET.get("sector")
        subsector = request.GET.get("subsector")

        queryset = (Country.objects.filter(
            indicator__sector__sector=sector,
            indicator__subsector__subsector=subsector)
            .prefetch_related("indicator__subsector__sector")
            .values("country", "indicator__indicator", "indicator__sector__sector", "year", "rank")
        )

        country_rank_annotations = queryset.filter(country=selected_country).values(
            "indicator__indicator", "indicator__sector__sector", "year", "rank")

        max_rank_annotations = queryset.values(
            'indicator__indicator', 'year').annotate(max_rank=Max('rank'))

        max_rank_dict = {(item['indicator__indicator'], item['year'])
                          : item['max_rank'] for item in max_rank_annotations}

        indicator_data = defaultdict(list)

        for item in country_rank_annotations:
            year = item['year']
            indicator_name = item['indicator__indicator']
            rank = item['rank']

            max_rank = max_rank_dict.get((indicator_name, year))

            score = round((1 - rank / max_rank) * 100, 2)

            indicator_info = {
                "year": year,
                "score": score,
            }

            indicator_data[indicator_name].append(indicator_info)

        response_data = [{"indicator": key, "data": value}
                         for key, value in indicator_data.items()]

        return Response(response_data)
