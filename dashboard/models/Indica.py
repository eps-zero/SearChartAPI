from django.db import models
from .SubSect import Sect, SubSect
import os
from dotenv import load_dotenv

load_dotenv()

class Indica(models.Model):
    class Meta:
        managed = False
        db_table = os.getenv('DB_TABLE_NAME_INDICATOR')  
    
    sector = models.ForeignKey(Sect, db_column='sector', on_delete=models.CASCADE)
    subsector = models.ForeignKey(SubSect, db_column='subsector', on_delete=models.CASCADE)
    indicator = models.CharField(max_length=1000, primary_key=True)

    def __str__(self):        
        return f"{self.subsector}  Indicator: {self.indicator};"