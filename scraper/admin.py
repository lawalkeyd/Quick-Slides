from django.contrib import admin
from .models import ScrapedInfo, Images, ParentInfo, Headings, Details

# Register your models here.

admin.site.register(ScrapedInfo)
admin.site.register(Images)
admin.site.register(ParentInfo)
admin.site.register(Headings)
admin.site.register(Details)