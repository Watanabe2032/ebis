
import datetime
from django.db import models
from django.utils import timezone

class EbisUserTable(models.Model):
    user_id = models.AutoField(primary_key=True, editable=False)
    fullname = models.CharField(max_length=64, unique=True)
    display_name = models.CharField(max_length=64, unique=True)
    ruby = models.CharField(max_length=64)
    is_esquadra = models.IntegerField(default=1)
    is_filtering = models.IntegerField(default=1)
    usage_start_datetime = models.DateTimeField()
    usage_end_datetime = models.DateTimeField()
    comment = models.CharField(max_length=2048, blank=True, null=True)

    def __str__(self):
        return f"[{self.user_id}] {self.display_name}"


class OwnerTable(models.Model):
    owner_id = models.AutoField(primary_key=True, editable=False)
    fullname = models.CharField(max_length=64, unique=True)
    display_name = models.CharField(max_length=64, unique=True)
    ruby = models.CharField(max_length=64)
    is_filtering = models.IntegerField(default=1)
    comment = models.CharField(max_length=2048, blank=True, null=True)

    def __str__(self):
        return f"[{self.owner_id}] {self.display_name} ({str(self.is_filtering)})"

class StorageTable(models.Model):
    storage_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=64)
    display_name = models.CharField(max_length=64)
    is_filtering = models.IntegerField(default=1)

    def __str__(self):
        return f"[{self.storage_id}] {self.full_name} ({self.is_filtering})"

class EquipmentStateTable(models.Model):
    equipment_state_id = models.AutoField(primary_key=True)
    equipment_state_name = models.CharField(max_length=64)

    def __str__(self):
        return f"[{self.equipment_state_id}] {self.equipment_state_name}"

class EquipmentTable(models.Model):
    equipment_id = models.AutoField(primary_key=True, editable=False)
    owner_id = models.ForeignKey(OwnerTable, on_delete=models.PROTECT)
    storage_id = models.ForeignKey(StorageTable, on_delete=models.PROTECT)
    equipment_state_id = models.ForeignKey(EquipmentStateTable, on_delete=models.PROTECT)
    full_name = models.CharField(max_length=64)
    display_name = models.CharField(max_length=64)
    comment = models.CharField(max_length=2048, blank=True, null=True)

    def __str__(self):
        return f"[{self.equipment_id}] {self.display_name}"

class CategoryTagTable(models.Model):
    category_tag_id = models.AutoField(primary_key=True)
    category_tag_name = models.CharField(max_length=64)
    ruby = models.CharField(max_length=64)

    def __str__(self):
        return f"[{self.category_tag_id}] {self.category_tag_name}"

class EquipmentCategoryTagMappingTable(models.Model):
    mapping_id = models.AutoField(primary_key=True)
    equipment_id = models.ForeignKey(EquipmentTable, on_delete=models.PROTECT)
    category_tag_id = models.ForeignKey(CategoryTagTable, on_delete=models.PROTECT)

    def __str__(self):
        return f"[{self.mapping_id}] {self.equipment_id} --- {self.category_tag_id}"

class BorrowingHistoryTable(models.Model):
    borrowing_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(EbisUserTable, on_delete=models.PROTECT)
    equipment_id = models.ForeignKey(EquipmentTable, on_delete=models.PROTECT)
    borrowind_datetime = models.DateTimeField()
    return_datetime = models.DateTimeField()
    is_returned = models.IntegerField(default=0)

    def __str__(self):
        return f"[{self.borrowing_id}][{self.borrowind_datetime.strftime('%Y-%m-%d %H:%M')}] user:{self.user_id}, equipment:{self.equipment_id}"

