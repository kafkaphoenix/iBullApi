# Generated by Django 3.1.3 on 2022-02-12 21:26

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Trade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(
                    max_length=4,
                    validators=[django.core.validators.RegexValidator(regex='^(buy|sell)$')]
                )),
                ('user_id', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('symbol', models.CharField(max_length=10)),
                ('shares', models.PositiveIntegerField(
                    validators=[
                        django.core.validators.MinValueValidator(1),
                        django.core.validators.MaxValueValidator(100)
                    ]
                )),
                ('price', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('timestamp', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0)])),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]