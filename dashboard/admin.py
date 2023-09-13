from django.contrib import admin
from dashboard.models import Sect, SubSect, Indica, Country

@admin.register(Sect)
class CountryRatingAdmin(admin.ModelAdmin):
    list_display = ('sector',)
    search_fields = ('sector',)

@admin.register(SubSect)
class CountryRatingAdmin(admin.ModelAdmin):
    list_display = ('sector', 'subsector')
    list_filter = ('sector',)
    search_fields = ('sector', 'subsector')

@admin.register(Country)
class CountryRatingAdmin(admin.ModelAdmin):
    list_display = ('country', 'country_code', 'year', 'indicator', 'amount','rank')
    list_filter = ('country', 'year', 'indicator', 'rank')
    search_fields = ('country', 'year', 'indicator')


@admin.register(Indica)
class CountryRatingAdmin(admin.ModelAdmin):
    list_display = ('sector', 'subsector', 'indicator')
    list_filter = ('sector', 'subsector')
    search_fields = ('sector', 'subsector', 'indicator')

