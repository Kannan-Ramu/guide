# Generated by Django 4.0.4 on 2023-03-19 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teamID', models.CharField(max_length=100)),
                ('guide', models.CharField(max_length=100, null=True)),
                ('guide_email', models.CharField(max_length=100, null=True)),
                ('body', models.TextField(null=True)),
                ('published_date', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
    ]
