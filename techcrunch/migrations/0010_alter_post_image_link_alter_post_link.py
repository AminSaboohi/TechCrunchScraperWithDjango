# Generated by Django 4.2 on 2024-04-12 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('techcrunch', '0009_alter_autoscrapauthoritem_authors_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image_link',
            field=models.CharField(blank=True, max_length=250, verbose_name='Image link'),
        ),
        migrations.AlterField(
            model_name='post',
            name='link',
            field=models.CharField(blank=True, max_length=250, verbose_name='Link'),
        ),
    ]
