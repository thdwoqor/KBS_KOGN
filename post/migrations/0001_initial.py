# Generated by Django 3.2.8 on 2022-01-08 12:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('radio', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=200)),
                ('contents', models.CharField(max_length=200)),
                ('radio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='radio_uniq_id', to='radio.radio')),
            ],
        ),
    ]