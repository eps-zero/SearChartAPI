from collections import defaultdict
from rest_framework.views import APIView
from dashboard.models import Country
from dashboard.serializers import CountrySerializer
from rest_framework.response import Response
from django.db.models import Max
from operator import itemgetter


class SectorRankDifferenceApiView(APIView):
    serializer_class = CountrySerializer

    def get(self, request):
        country = request.GET.get("country")
        year1 = request.GET.get("year1")  # First year
        year2 = request.GET.get("year2")  # Second year

        queryset = (Country.objects.filter(
            year__in=(year1, year2))
            .prefetch_related("indicator__subsector__sector")
            .values("country", "indicator__indicator", "indicator__sector__sector", "year", "rank")
        )

        country_rank_annotations1 = queryset.filter(country=country, year=year1).values(
            "indicator__indicator", "indicator__sector__sector", "year", "rank")
        country_rank_annotations2 = queryset.filter(country=country, year=year2).values(
            "indicator__indicator", "indicator__sector__sector", "year", "rank")

        max_rank_annotations = queryset.values(
            'indicator__indicator', 'year').annotate(max_rank=Max('rank'))

        max_rank_dict = {(item['indicator__indicator'], item['year']): item['max_rank'] for item in max_rank_annotations}

        indicator_data = []

        percentile_by_sector1 = defaultdict(dict)

        for country_rank1 in country_rank_annotations1:
            indicator_name = country_rank1['indicator__indicator']
            sector_name = country_rank1['indicator__sector__sector']
            rank1 = country_rank1['rank']

            max_rank1 = max_rank_dict.get((indicator_name, int(year1)))

            score1 = (1 - rank1 / max_rank1) * 100

            if sector_name not in percentile_by_sector1:
                percentile_by_sector1[sector_name] = []

            percentile_by_sector1[sector_name].append(score1)

        percentile_by_sector2 = defaultdict(dict)

        for country_rank2 in country_rank_annotations2:
            indicator_name = country_rank2['indicator__indicator']
            sector_name = country_rank2['indicator__sector__sector']
            rank2 = country_rank2['rank']

            max_rank2 = max_rank_dict.get((indicator_name, int(year2)))

            score2 = (1 - rank2 / max_rank2) * 100

            if sector_name not in percentile_by_sector2:
                percentile_by_sector2[sector_name] = []

            percentile_by_sector2[sector_name].append(score2)

        for sector_name1, percentile_list1 in percentile_by_sector1.items():
            for sector_name2, percentile_list2 in percentile_by_sector2.items():
                if percentile_list1 and percentile_list2 and sector_name1 == sector_name2:
                    percentile_average1 = sum(
                        percentile_list1) / len(percentile_list1)
                    percentile_average2 = sum(
                        percentile_list2) / len(percentile_list2)
                    indicator_info = [
                        sector_name1, round(
                            percentile_average2-percentile_average1, 2)
                    ]

                    indicator_data.append(indicator_info)

        return Response(indicator_data)
