from django.db import models

class History(models.Model):
    
    query = models.TextField(null=False)
    sim1 = models.FloatField(null=False)    
    sim2 = models.FloatField(null=False)    
    sim3 = models.FloatField(null=False)    
    answer = models.TextField(null=False)
    date = models.DateTimeField(auto_now_add=False)
    s_id = models.CharField(max_length=500, null=True)
    
    def __str__(self) -> str:
        return f'{self.id} {self.query}'