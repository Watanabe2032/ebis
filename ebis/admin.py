from django.contrib import admin

# Register your models here.

from .models import EbisUserTable
admin.site.register(EbisUserTable)

from .models import OwnerTable
admin.site.register(OwnerTable)

from .models import StorageTable
admin.site.register(StorageTable)

from .models import EquipmentStateTable
admin.site.register(EquipmentStateTable)

from .models import EquipmentTable
admin.site.register(EquipmentTable)

from .models import CategoryTagTable
admin.site.register(CategoryTagTable)

from .models import EquipmentCategoryTagMappingTable
admin.site.register(EquipmentCategoryTagMappingTable)

from .models import BorrowingHistoryTable
admin.site.register(BorrowingHistoryTable)
