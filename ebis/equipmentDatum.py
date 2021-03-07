
import datetime
from django.db import models
from django.utils import timezone

from .models import EbisUserTable
from .models import OwnerTable
from .models import StorageTable
from .models import EquipmentStateTable
from .models import EquipmentTable
from .models import CategoryTagTable
from .models import EquipmentCategoryTagMappingTable
from .models import BorrowingHistoryTable

class equipmentDatum:
    def __init__(self, equipmentId, equipmentTable=EquipmentTable.objects.none()):
        self.equipmentTable = equipmentTable
        if equipmentTable is None:
            self.equipmentTable = EquipmentTable.objects.filter(equipment_id=equipmentId)
        
        self.categoryTagIdList = list(EquipmentCategoryTagMappingTable.objects.filter(equipment_id=equipmentId).values_list('category_tag_id', flat=True))
        self.categoryTags = CategoryTagTable.objects.filter(category_tag_id__in=self.categoryTagIdList).order_by('ruby')

        # self.borrowingHistories = BorrowingHistoryTable.objects.filter(equipment_id=equipmentId)
        # self.latestBorrowingHistory = None
        # if self.borrowingHistories.Exist():
        #     self.latestBorrowingHistory = borrowingHistories.filter(borrowing_id=[borrowingHistories.aggregate(models.Max('borrowing_id'))])

        self.atelicBorrowingHistories = BorrowingHistoryTable.objects.filter(is_returned=0, equipment_id=equipmentId)
    
    