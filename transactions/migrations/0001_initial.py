# Generated by Django 2.1.4 on 2018-12-27 20:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('budgets', '0004_auto_20181227_0202'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('og_name', models.CharField(max_length=255)),
                ('amount', models.FloatField()),
                ('date', models.DateTimeField()),
                ('budget_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='budgets.Budget')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
