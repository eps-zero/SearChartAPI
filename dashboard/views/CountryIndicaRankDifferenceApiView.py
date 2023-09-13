from collections import defaultdict
from rest_framework.views import APIView
from dashboard.models import Country, Indica
from dashboard.serializers import CountrySerializer
from rest_framework.response import Response
from django.db.models import Max


class CountryIndicaRankDifferenceApiView(APIView):
    serializer_class = CountrySerializer

    def get(self, request):
        selected_country = request.GET.get("country")
        year1 = request.GET.get("year1")
        year2 = request.GET.get("year2")
        sector = request.GET.get("sector")
        subsector = request.GET.get("subsector")

        queryset = (Country.objects.filter(
            year__in=(year1, year2),
            indicator__sector__sector=sector,
            indicator__subsector__subsector=subsector)
            .prefetch_related("indicator__subsector__sector")
            .values("country", "indicator__indicator", "indicator__sector__sector", "year", "rank")
        )

        country_rank_annotations1 = queryset.filter(country=selected_country, year=year1).values(
            "indicator__indicator", "indicator__sector__sector", "year", "rank")
        country_rank_annotations2 = queryset.filter(country=selected_country, year=year2).values(
            "indicator__indicator", "indicator__sector__sector", "year", "rank")

        max_rank_annotations = queryset.values(
            'indicator__indicator', 'year').annotate(max_rank=Max('rank'))

        max_rank_dict = {(item['indicator__indicator'], item['year'])
                          : item['max_rank'] for item in max_rank_annotations}

        indicator_data = []

        for country_rank1 in country_rank_annotations1:
            for country_rank2 in country_rank_annotations2:
                if (
                    country_rank1['indicator__indicator'] == country_rank2['indicator__indicator']
                ):
                    indicator_name = country_rank1['indicator__indicator']
                    rank1 = country_rank1['rank']
                    rank2 = country_rank2['rank']

                    max_rank1 = max_rank_dict.get((indicator_name, int(year1)))
                    max_rank2 = max_rank_dict.get((indicator_name, int(year2)))

                    score1 = (1 - rank1 / max_rank1) * 100
                    score2 = (1 - rank2 / max_rank2) * 100

                    indicator_info = [
                        country_rank1['indicator__indicator'], round(
                            score2-score1, 2)
                    ]

                    indicator_data.append(indicator_info)

        return Response(indicator_data)
