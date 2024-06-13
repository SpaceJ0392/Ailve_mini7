from django.db import models


class History(models.Model):

    query = models.TextField(null=False)
    sim1 = models.FloatField(null=False)
    sim2 = models.FloatField(null=False)
    sim3 = models.FloatField(null=False)
    answer = models.TextField(null=False)
    date = models.DateTimeField(auto_now_add=True)
    s_id = models.CharField(max_length=500, null=True)

    def __str__(self) -> str:
        return f"{self.id} {self.query}"


class QaList(models.Model):
    id = models.AutoField(db_column="id", primary_key=True)
    type = models.CharField(max_length=20)
    qa = models.CharField(max_length=500)

    class Meta:
        managed = False
        db_table = "QA_LIST"
