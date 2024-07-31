# Generated by Django 5.0.7 on 2024-07-31 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_course_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/categories'),
        ),
        migrations.AddField(
            model_name='course',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/courses'),
        ),
        migrations.AlterField(
            model_name='course',
            name='video',
            field=models.FileField(upload_to='videos/courses'),
        ),
    ]
