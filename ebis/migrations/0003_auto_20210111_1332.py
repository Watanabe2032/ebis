# Generated by Django 3.1.4 on 2021-01-11 04:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ebis', '0002_auto_20210111_1327'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ownertable',
            old_name='is_filering',
            new_name='is_filtering',
        ),
    ]