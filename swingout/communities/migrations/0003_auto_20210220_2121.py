# Generated by Django 3.1.5 on 2021-02-20 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0002_updaterequest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='style',
            name='style',
            field=models.CharField(choices=[('Balboa', 'Balboa'), ('Blues', 'Blues'), ('Boogie Woogie', 'Boogie Woogie'), ('Carolina Shag', 'Carolina Shag'), ('Charleston', 'Charleston'), ("Chicago Steppin'", "Chicago Steppin'"), ('Collegiate Shag', 'Collegiate Shag'), ('East Coast Swing', 'East Coast Swing'), ('Fusion', 'Fusion'), ('Lindy Hop', 'Lindy Hop'), ('St. Louis Shag', 'St. Louis Shag'), ('West Coast Swing', 'West Coast Swing'), ('Zouk', 'Zouk')], default='Lindy Hop', max_length=32),
        ),
    ]
