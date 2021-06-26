from django.db import models

# Create your models here.
class Images(models.Model):
    images = models.CharField(max_length=120)

class ScrapedInfo(models.Model):
    url = models.CharField(max_length=60)
    title = models.CharField(max_length=20)
    images = models.ForeignKey(Images, on_delete=models.PROTECT, null=True, blank=True)
    text = models.TextField()

    class Meta:
        verbose_name = 'Currency'
        verbose_name_plural = 'Currencies'

    def __str__(self):
        return self.pair
