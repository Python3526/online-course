# Generated by Django 5.0.7 on 2024-08-01 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('slug', models.SlugField(blank=True, max_length=200, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('level', models.CharField(choices=[('Beginner', 'Beginner'), ('Junior', 'Junior'), ('Middle ', 'Middle'), ('Senior', 'Senior'), ('Expert', 'Expert')], default='Junior', max_length=100)),
                ('twitter_link', models.CharField(blank=True, max_length=150, null=True)),
                ('facebook_link', models.CharField(blank=True, max_length=150, null=True)),
                ('linkedin_link', models.CharField(blank=True, max_length=150, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/teachers')),
            ],
        ),
    ]
