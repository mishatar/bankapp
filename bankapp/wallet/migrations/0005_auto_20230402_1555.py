# Generated by Django 3.2.16 on 2023-04-02 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0004_account_balance'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Wallet',
        ),
        migrations.AddField(
            model_name='account',
            name='balance_eur',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
        migrations.AddField(
            model_name='account',
            name='balance_usd',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
    ]
