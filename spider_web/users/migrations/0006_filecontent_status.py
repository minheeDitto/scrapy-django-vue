# Generated by Django 2.2.6 on 2019-12-04 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20191126_2310'),
    ]

    operations = [
        migrations.AddField(
            model_name='filecontent',
            name='status',
            field=models.CharField(choices=[(1, 'start'), (2, 'pause'), (3, 'stop'), (4, 'unpause')], default='', max_length=15),
        ),
    ]