# Generated by Django 2.2.6 on 2019-11-26 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20191029_2003'),
    ]

    operations = [
        migrations.AddField(
            model_name='filecontent',
            name='settings_path',
            field=models.CharField(default='', max_length=50, verbose_name='配置文件'),
        ),
        migrations.AddField(
            model_name='filecontent',
            name='spider_class',
            field=models.CharField(default='', max_length=50, verbose_name='爬虫类'),
        ),
    ]
