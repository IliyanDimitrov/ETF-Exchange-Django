# Generated by Django 4.1.3 on 2022-12-30 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_portfoliopnl'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfoliopnl',
            name='principal',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]