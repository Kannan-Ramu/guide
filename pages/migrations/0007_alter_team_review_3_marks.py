# Generated by Django 4.2 on 2023-05-04 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0006_alter_team_review_2_marks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='review_3_marks',
            field=models.IntegerField(default=10),
        ),
    ]
