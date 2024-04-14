# Generated by Django 4.2 on 2024-04-12 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('techcrunch', '0011_alter_author_avatar_image_alter_post_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='avatar_image',
        ),
        migrations.AddField(
            model_name='author',
            name='image',
            field=models.ImageField(blank=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, upload_to='images/'),
        ),
    ]
