from django.db import models
from .Sect import Sect
import os
from dotenv import load_dotenv

load_dotenv()

class SubSect(models.Model):
    class Meta:
        managed = False
        db_table = os.getenv('DB_TABLE_NAME_SUBSECTOR')
         
    
    sector = models.ForeignKey(Sect, db_column='sector', on_delete=models.CASCADE)
    subsector = models.CharField(max_length=500, primary_key=True)

    def __str__(self):        
        return f"{self.sector} Subsector: {self.subsector};"