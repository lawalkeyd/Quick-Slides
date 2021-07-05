from django.db import models

# Create your models here.

class ScrapedInfo(models.Model):
    url = models.CharField(max_length=60)
    title = models.CharField(max_length=160)

    class Meta:
        verbose_name = 'Scraped Info'

    def __str__(self):
        return self.title

class ParentInfo(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children')
    title = models.CharField(max_length=160)        

class Images(models.Model):
    info = models.ForeignKey(ParentInfo, on_delete=models.CASCADE, related_name='images')
    images = models.CharField(max_length=120)

class Headings(models.Model):        
    info = models.ForeignKey(ParentInfo, on_delete=models.CASCADE, related_name='headings')
    text = models.CharField(max_length=160)

class Details(models.Model):
    models.TextField(verbose_name='details')