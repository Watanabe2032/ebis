# Generated by Django 3.1.4 on 2021-01-11 02:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryTagTable',
            fields=[
                ('category_tag_id', models.AutoField(primary_key=True, serialize=False)),
                ('category_tag_name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='EbisUserTable',
            fields=[
                ('user_id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('fullname', models.CharField(max_length=64, unique=True)),
                ('display_name', models.CharField(max_length=64, unique=True)),
                ('is_esquadra', models.IntegerField(default=1)),
                ('usage_start_datetime', models.DateTimeField()),
                ('usage_end_datetime', models.DateTimeField()),
                ('comment', models.CharField(max_length=2048)),
            ],
        ),
        migrations.CreateModel(
            name='EquipmentStateTable',
            fields=[
                ('equipment_state_id', models.AutoField(primary_key=True, serialize=False)),
                ('equipment_state_name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='OwnerTable',
            fields=[
                ('owner_id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('fullname', models.CharField(max_length=64, unique=True)),
                ('display_name', models.CharField(max_length=64, unique=True)),
                ('is_filering', models.IntegerField(default=1)),
                ('comment', models.CharField(max_length=2048)),
            ],
        ),
        migrations.CreateModel(
            name='StorageTable',
            fields=[
                ('storage_id', models.AutoField(primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=64)),
                ('display_name', models.CharField(max_length=64)),
                ('is_filtering', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='EquipmentTable',
            fields=[
                ('equipment_id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=64)),
                ('display_name', models.CharField(max_length=64)),
                ('comment', models.CharField(max_length=2048)),
                ('equipment_state_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ebis.equipmentstatetable')),
                ('owner_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ebis.ownertable')),
                ('storage_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ebis.storagetable')),
            ],
        ),
        migrations.CreateModel(
            name='EquipmentCategoryTagMappingTable',
            fields=[
                ('mapping_id', models.AutoField(primary_key=True, serialize=False)),
                ('category_tag_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ebis.categorytagtable')),
                ('equipment_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ebis.equipmenttable')),
            ],
        ),
        migrations.CreateModel(
            name='BorrowingHistoryTable',
            fields=[
                ('borrowing_id', models.AutoField(primary_key=True, serialize=False)),
                ('borrowind_datetime', models.DateTimeField()),
                ('return_datetime', models.DateTimeField()),
                ('is_returned', models.IntegerField(default=0)),
                ('equipment_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ebis.equipmenttable')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ebis.ebisusertable')),
            ],
        ),
    ]
