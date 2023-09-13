from django.db import models
import os
from dotenv import load_dotenv

load_dotenv()

class Sect(models.Model):
    class Meta:
        managed = False
        db_table = os.getenv('DB_TABLE_NAME_SECTOR') 
    
    sector = models.CharField(max_length=500, primary_key=True)

    def __str__(self):        
        return f"Sector: {self.sector};"
