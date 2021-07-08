# Generated by Django 3.2.4 on 2021-07-08 12:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0003_auto_20210707_1647'),
    ]

    operations = [
        migrations.AddField(
            model_name='details',
            name='info',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='details', to='scraper.parentinfo'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='details',
            name='text',
            field=models.TextField(default='default', verbose_name='details'),
            preserve_default=False,
        ),
    ]
