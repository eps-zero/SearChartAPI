from django.db import models
from .Indica import Indica
import os
from dotenv import load_dotenv

load_dotenv()

class Country(models.Model):
    class Meta:
        managed = False
        db_table = os.getenv('DB_TABLE_NAME_COUNTRIES')  
     
    year = models.IntegerField()
    indicator = models.ForeignKey(Indica, db_column='indicator', on_delete=models.CASCADE)
    country = models.CharField(max_length=100)
    country_code = models.CharField(max_length=5)
    amount = models.IntegerField()
    rank = models.IntegerField()

    def __str__(self):
        return f"Country: {self.country}; Year: {self.year}; {self.indicator} Rank: {self.rank};"

    
