# Generated by Django 3.1.5 on 2021-01-14 20:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Community',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(max_length=36)),
                ('label', models.CharField(max_length=256)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('url', models.CharField(max_length=512)),
            ],
            options={
                'verbose_name_plural': 'Communities',
            },
        ),
        migrations.CreateModel(
            name='Style',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('style', models.CharField(choices=[('1', 'Lindy Hop')], default='1', max_length=1)),
                ('community', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='communities.community')),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emailAddress', models.EmailField(default='', max_length=254)),
                ('phoneNumber', models.CharField(default='', max_length=64)),
                ('url', models.CharField(default='', max_length=512)),
                ('community', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='communities.community')),
            ],
        ),
    ]
