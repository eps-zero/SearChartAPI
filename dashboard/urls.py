from django.urls import path
from .views import *

urlpatterns = [
    path('country-info/', CountryInfoApiView.as_view(), name='country_info'),
    path('country-diagram/', CountryIndicaDiagramApiView.as_view(), name='country_diagram'),
    path('country-rank-difference/', CountryIndicaRankDifferenceApiView.as_view(), name='country_rank_difference'),
    path('average-score/', AverageScoreIndicaApiView.as_view(), name='average_score'),
    path('year-score/', SectorYearScoreApiView.as_view(), name='year_score'),
    path("sector-rank-difference/", SectorRankDifferenceApiView.as_view(), name="country_score"),
    path("sector-average-score/", SectorAverageScoreApiView.as_view(), name="sector_average_score"),
    path("country-score-year/", CountryScoreYearByApiView.as_view(), name="country_score_year"),
    path("country-score-difference/", ScoreDifferenceTwoYearsApiView.as_view(), name="country_score_sector"),
]