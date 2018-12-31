# Generated by Django 2.0.6 on 2018-12-30 22:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ShowIndicators', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=20)),
                ('stock_value', models.FloatField()),
                ('date', models.DateTimeField()),
                ('stock_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ShowIndicators.Securities')),
                ('stratefy_used', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ShowIndicators.Strategies')),
            ],
        ),
    ]
