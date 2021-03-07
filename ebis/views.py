
# 文字列からの数値抽出用
import re
import textwrap
import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from .equipmentDatum import equipmentDatum

from .models import EbisUserTable
from .models import OwnerTable
from .models import StorageTable
from .models import EquipmentStateTable
from .models import EquipmentTable
from .models import CategoryTagTable
from .models import EquipmentCategoryTagMappingTable
from .models import BorrowingHistoryTable


def ebisHome(request):
    return render(request, 'ebis/ebis-home.html', {})

def searchEquipment(request):
    params = {}
    params['ownerList'] = OwnerTable.objects.filter(is_filtering=1).order_by('ruby')
    params['storageList'] = StorageTable.objects.filter(is_filtering=1)
    params['equipmentStateList'] = EquipmentStateTable.objects.all()
    params['categoryTagList'] = CategoryTagTable.objects.all().order_by('ruby')
    params['userList'] = EbisUserTable.objects.filter(is_filtering=1).order_by('ruby')

    if request.method == "POST":
        searchWordParams = request.POST.getlist('searchWordParams', None)
        params['searchWordParams'] = searchWordParams
        ownerParams = request.POST.getlist('ownerParams', None)
        ownerParams = [int(s) for s in ownerParams]
        params['ownerParams'] = ownerParams
        userParams = request.POST.getlist('userParams', None)
        userParams = [int(s) for s in userParams]
        params['userParams'] = userParams
        equipmentStateParams = request.POST.getlist('equipmentStateParams', None)
        equipmentStateParams = [int(s) for s in equipmentStateParams]
        params['equipmentStateParams'] = equipmentStateParams
        categoryTagParams = request.POST.getlist('categoryTagParams', None)
        categoryTagParams = [int(s) for s in categoryTagParams]
        params['categoryTagParams'] = categoryTagParams
        equipmentList = EquipmentTable.objects.none()

        if ownerParams:
            equipmentList = equipmentList.union(EquipmentTable.objects.filter(owner_id__in=ownerParams))

        if userParams:
            equipmentIdList = BorrowingHistoryTable.objects.filter(is_returned=0, user_id__in=userParams).values_list('equipment_id', flat=True)
            equipmentList = equipmentList.union(EquipmentTable.objects.filter(equipment_id__in=equipmentIdList))

        if equipmentStateParams:
            equipmentList = equipmentList.union(EquipmentTable.objects.filter(equipment_state_id__in=equipmentStateParams))

        if categoryTagParams:
            selectedCategoryTagMappings = EquipmentCategoryTagMappingTable.objects.filter(category_tag_id__in=categoryTagParams)
            selectedEquipmentIdList = list(selectedCategoryTagMappings.values_list('equipment_id', flat=True))
            equipmentList = equipmentList.union(EquipmentTable.objects.filter(equipment_id__in=selectedEquipmentIdList))

        if not searchWordParams[0]:
            print('searchWordParams is None')
        elif equipmentList.exists():
            equipmentList = equipmentList.filter(display_name__icontains=searchWordParams[0])
        else:
            equipmentList = EquipmentTable.objects.filter(display_name__icontains=searchWordParams[0])

        equipmentData = []
        for equipment in equipmentList:
            datum = equipmentDatum(equipmentId=equipment.equipment_id, equipmentTable=equipment)
            equipmentData.append(datum)
        params['equipmentDatumList'] = equipmentData

    return render(request, 'ebis/search-equipment.html', params)


def addEquipment(request):
    params = {}
    params['ownerList'] = OwnerTable.objects.filter(is_filtering=1).order_by('ruby')
    params['storageList'] = StorageTable.objects.filter(is_filtering=1)
    params['equipmentStateList'] = EquipmentStateTable.objects.all()
    params['categoryTagList'] = CategoryTagTable.objects.all().order_by('ruby')
    params['commentTemplate'] = textwrap.dedent(
'''SN:000010

付属品
・電源ケーブル
・HDMIケーブル

備考
2020.1.5 使用開始
2020.1.6 HDMIケーブルを紛失
2021.1.12 電源ケーブルのシールドが破れる。代替品に交換
2022.1.20 電源が入らなくなったため破棄''')
    
    if request.method == "POST":
        fullname = request.POST.get('fullname', None)
        params['postFullname'] = fullname
        if not fullname:
            params['message'] = '正式名を入力してください'
        elif EquipmentTable.objects.filter(full_name=fullname).exists():
            params['message'] = '正式名 "' + fullname + '" は既に登録されています。\n別の名前を設定してください。'

        displayName = request.POST.get('displayName', None)
        params['postDisplayName'] = displayName
        if not displayName:
            params['message'] = '表示名を入力してください'
        elif EquipmentTable.objects.filter(display_name=displayName).exists():
            params['message'] = '表示名 "' + displayName + '" は既に登録されています。\n別の名前を設定してください。'

        ownerId = request.POST.get('ownerId', None)
        params['postOwnerId'] = int(ownerId)

        storageId = request.POST.get('storageId', None)
        params['postStorageId'] = int(storageId)

        equipmentStateId = request.POST.get('equipmentStateId', None)
        params['postEquipmentStateId'] = int(equipmentStateId)

        categoryTagIds = request.POST.getlist('categoryTagIds', None)
        categoryTagIds = [int(s) for s in categoryTagIds]
        params['postCategoryTagIds'] = categoryTagIds

        equipmentComment = request.POST.get('equipmentComment', None)
        params['postEquipmentComment'] = equipmentComment

        if 'equipmentAdditionButton' in request.POST and not 'message' in params:
            newEquipment = EquipmentTable(
                owner_id = OwnerTable(owner_id=ownerId),
                storage_id = StorageTable(storage_id=storageId),
                equipment_state_id = EquipmentStateTable(equipment_state_id=equipmentStateId),
                full_name = fullname,
                display_name = displayName,
                comment = equipmentComment,
            )
            newEquipment.save()

            for categoryTagId in categoryTagIds:
                newMapping = EquipmentCategoryTagMappingTable(
                    equipment_id = EquipmentTable.objects.get(equipment_id=newEquipment.equipment_id),
                    category_tag_id = CategoryTagTable.objects.get(category_tag_id=categoryTagId),
                )
                newMapping.save()

    return render(request, 'ebis/add-equipment.html', params)

def editEquipment(request):
    params = {}

    if request.method == "POST":
        params['ownerList'] = OwnerTable.objects.filter(is_filtering=1).order_by('ruby')
        params['storageList'] = StorageTable.objects.filter(is_filtering=1)
        params['equipmentStateList'] = EquipmentStateTable.objects.all()
        params['categoryTagList'] = CategoryTagTable.objects.all().order_by('ruby')
        equipmentId = None
        isSearching = False

        # 検索画面からの遷移時
        if request.POST.get('equipmentEditButtonFromSearchEquipment', ''):
            equipmentId = request.POST.get('equipmentEditButtonFromSearchEquipment', '').replace('equipmentEditButtonFromSearchEquipment', '')
            isSearching = True

        # 検索ボタンが押された時
        elif request.POST.get('equipmentSearchButton', ''):
            equipmentId = request.POST.get('equipmentId', None)
            isSearching = True
        
        if isSearching:
            params['equipmentId'] = equipmentId
            if equipmentId and type(equipmentId) is str:
                equipmentId = re.sub("\\D", "", equipmentId)
            if not equipmentId or not equipmentId.isdecimal():
                params['searchMessage'] = '無効な備品IDです。\n変更する備品のIDを指定してください。'
                return render(request, 'ebis/edit-equipment.html', params)

            equipmentId = int(equipmentId)
            equipment = EquipmentTable.objects.filter(equipment_id=equipmentId)
            if not equipment.exists():
                params['searchMessage'] = '指定した備品IDは存在しません。\n有効な備品IDを指定してください。'
            else:
                params['searchMessage'] = '設定変更を行う場合は、備品IDを編集しないでください。'
                datum = equipmentDatum(equipmentId=equipment[0].equipment_id, equipmentTable=equipment[0])
                params['equipmentFullname'] = datum.equipmentTable.full_name
                params['equipmentDisplayName'] = datum.equipmentTable.display_name
                params['equipmentOwnerId'] = datum.equipmentTable.owner_id.owner_id
                params['equipmentStorageId'] = datum.equipmentTable.storage_id.storage_id
                params['equipmentStateId'] = datum.equipmentTable.equipment_state_id.equipment_state_id
                params['equipmentComment'] = datum.equipmentTable.comment
                params['equipmentCategoryTagIds'] = [int(s.category_tag_id) for s in datum.categoryTags]
                params['isEquipmentData'] = '1'


        # 変更ボタンが押された時
        elif request.POST.get('equipmentEditButton', ''):
            print('equipmentEditButton')
            fullname = request.POST.get('fullname', None)
            displayName = request.POST.get('displayName', None)
            ownerId = int(request.POST.get('ownerId', None))
            storageId = int(request.POST.get('storageId', None))
            equipmentStateId = int(request.POST.get('equipmentStateId', None))
            categoryTagIds = request.POST.getlist('categoryTagIds', None)
            categoryTagIds = [int(s) for s in categoryTagIds]
            equipmentComment = request.POST.get('equipmentComment', None)

            params['equipmentFullname'] = fullname
            params['equipmentDisplayName'] = displayName
            params['equipmentOwnerId'] = ownerId
            params['equipmentStorageId'] = storageId
            params['equipmentStateId'] = equipmentStateId
            params['equipmentCategoryTagIds'] = categoryTagIds
            params['equipmentComment'] = equipmentComment
            params['isEquipmentData'] = '1'
            params['searchMessage'] = '設定変更を行う場合は、備品IDを編集しないでください。'

            equipmentId = None
            isEuipment = False
            try:
                equipmentId = request.POST.get('equipmentEditButton', '').replace('equipmentEditButton', '')
                params['equipmentId'] = equipmentId
                equipmentId = int(equipmentId)
                equipment = EquipmentTable.objects.filter(equipment_id=equipmentId)
                isEuipment = equipment.exists()
                equipment = equipment[0]
            except:
                isEuipment = False

            if not isEuipment:
                params['editMessage'] = '設定変更に失敗しました。\n設定変更を行う場合は、備品IDを編集しないでください。'
                return render(request, 'ebis/edit-equipment.html', params)

            equipment.full_name = fullname
            equipment.display_name = displayName
            equipment.owner_id = OwnerTable.objects.get(owner_id=ownerId)
            equipment.storate_id = StorageTable.objects.get(storage_id=storageId)
            equipment.equipment_state_id = EquipmentStateTable.objects.get(equipment_state_id=equipmentStateId)
            equipment.comment = equipmentComment
            equipment.save()

            # カテゴリータグマッピングの追加、削除
            increasingCategories = []
            decreasingCategories = []
            currentCategories = list(EquipmentCategoryTagMappingTable.objects.filter(equipment_id=equipmentId).values_list('category_tag_id', flat=True))

            for id in categoryTagIds:
                if not id in currentCategories:
                    increasingCategories.append(id)
            for id in currentCategories:
                if not id in categoryTagIds:
                    decreasingCategories.append(id)

            for id in increasingCategories:
                newMapping = EquipmentCategoryTagMappingTable(
                    equipment_id = equipment,
                    category_tag_id = CategoryTagTable.objects.get(category_tag_id=id),
                )
                newMapping.save()
            
            for id in decreasingCategories:
                mapping = EquipmentCategoryTagMappingTable.objects.get(equipment_id=equipmentId, category_tag_id=id)
                mapping.delete()
                
            params['editMessage'] = '備品ID: ' + str(equipmentId) + ' の設定を変更しました。'

    # リンクで遷移してきた時
    else:
        params['searchMessage'] = '変更する備品のIDを指定してください。'

    return render(request, 'ebis/edit-equipment.html', params)


def editCategoryTag(request):
    params = {}
    params['categoryTagList'] = CategoryTagTable.objects.all().order_by('ruby')

    if request.POST.get('categoryTagAdditionButton', ''):
        tagName = request.POST.get('categoryTagName', '')
        tagRuby = request.POST.get('categoryTagRuby', '')
        print('[editCategoryTag] new tag: ' + tagName)
        print('[editCategoryTag] new ruby: ' + tagRuby)
        params['postCategoryTagName'] = tagName
        params['postCategoryTagRuby'] = tagRuby

        existingTags = CategoryTagTable.objects.filter(category_tag_name=tagName)
        if existingTags.exists():
            params['message'] = 'カテゴリーの追加に失敗しました。\n' + tagName + ' は既に存在します。別のカテゴリー名を設定してください。'
            return render(request, 'ebis/edit-category-tag.html', params)
        
        try:
            newCategoryTag = CategoryTagTable(
                category_tag_name = tagName,
                ruby = tagRuby
            )
            newCategoryTag.save()
            params['userList'] = EbisUserTable.objects.filter(is_filtering=1).order_by('ruby')
            params['message'] = 'カテゴリー \"' + tagName + '\" の追加が完了しました。'
        except:
            params['message'] = 'カテゴリーの登録に失敗しました。\n管理者に報告してください。'

    return render(request, 'ebis/edit-category-tag.html', params)

def editEquipmentUser(request):
    params = {}
    params['userList'] = EbisUserTable.objects.filter(is_filtering=1).order_by('ruby')
    params['selectedEquipmentId'] = None
    params['resultMessage'] = '備品IDを指定してください'

    if request.method == "POST":
        equipmentId = None

        # 使用者変更ボタン押下時
        if request.POST.get('borrowerEditButton', ''):
            equipmentId = request.POST.get('borrowerEditButton', '').replace('borrowerEditButton', '')
            try:
                equipmentId = int(equipmentId)
            except:
                params['resultMessage'] = '備品IDを正常に取得できませんでした。\n管理者に報告してください。'
                params['errorMessage'] = 'err: ' + request.POST.get('borrowerEditButton', '')
                return render(request, 'ebis/edit-equipment-user.html', params)

            selectedUserIdStr = request.POST.get('selectedUser', None)
            if not selectedUserIdStr:
                params['resultMessage'] = 'ユーザーIDを正常に取得できませんでした。\n管理者に報告してください。'
                return render(request, 'ebis/edit-equipment-user.html', params)

            imcompletedHistory = BorrowingHistoryTable.objects.filter(is_returned=0, equipment_id=equipmentId)
            if imcompletedHistory.exists():
                imcompletedHistory = imcompletedHistory[0]

            # 使用者なし を選択時
            if selectedUserIdStr == '-1':
                if not imcompletedHistory:
                    params['resultMessage'] = '備品ID:' + equipmentId + ' はすでに誰も使用していない状態です。'
                    return render(request, 'ebis/edit-equipment-user.html', params)
                imcompletedHistory.is_returned = 1
                imcompletedHistory.return_datetime = timezone.now()
                imcompletedHistory.save()
                params['resultMessage'] = '備品ID:' + str(equipmentId) + ' を返却しました。'

            # 新たに借りる時
            else:
                # 現在の使用者と選択したユーザが同じ時
                if imcompletedHistory and int(selectedUserIdStr) == imcompletedHistory.user_id:
                    params['resultMessage'] = '備品ID:' + equipmentId + ' はすでに' + imcompletedHistory.user_id.display_name + 'が使用中です。'
                    return render(request, 'ebis/edit-equipment-user.html', params)

                # 返却処理
                if imcompletedHistory:
                    imcompletedHistory.is_returned = 1
                    imcompletedHistory.return_datetime = timezone.now()
                    imcompletedHistory.save()

                newHistory = BorrowingHistoryTable(
                        # borrowing_id = models.AutoField(primary_key=True)
                        user_id = EbisUserTable(user_id=selectedUserIdStr),
                        equipment_id = EquipmentTable(equipment_id=int(equipmentId)),
                        borrowind_datetime = timezone.now(),
                        return_datetime = timezone.now() + timezone.timedelta(days=365),
                        is_returned = 0,
                )
                newHistory.save()
                params['resultMessage'] = '備品ID:' + str(equipmentId) + ' の使用者を変更しました。'

        if request.POST.get('userEditButton', ''):
            equipmentId = request.POST.get('userEditButton', '').replace('userEditButton', '')
            equipmentId = int(equipmentId)
        else:
            equipmentId = request.POST.get('equipmentId', None)

        if type(equipmentId) is str:
            equipmentId = re.sub("\\D", "", equipmentId)
        if equipmentId:
            equipmentId = int(equipmentId)
            params['selectedEquipmentId'] = equipmentId
            equipment = EquipmentTable.objects.filter(equipment_id=equipmentId)
            if not equipment.exists():
                params['resultMessage'] = '指定した備品IDは存在しません'
            else:
                datum = equipmentDatum(equipmentId=equipment[0].equipment_id, equipmentTable=equipment[0])
                params['equipmentDatum'] = datum

    return render(request, 'ebis/edit-equipment-user.html', params)

def showBorrowingHistory(request):
    params = {}
    params['selectedEquipmentId'] = None
    params['resultMessage'] = '備品IDを指定してください'

    if request.method == "POST":
        equipmentId = request.POST.get('equipmentId', None)
        if type(equipmentId) is str:
            equipmentId = re.sub("\\D", "", equipmentId)
            if equipmentId:
                equipmentId = int(equipmentId)

        if not equipmentId:
            params['resultMessage'] = '無効な備品IDです。\n備品IDには整数を入力してください。'
            return render(request, 'ebis/show-borrowing-history.html', params)

        equipment = EquipmentTable.objects.get(equipment_id=equipmentId)
        if not equipment:
            params['resultMessage'] = '指定した備品IDは存在しません'
            return render(request, 'ebis/show-borrowing-history.html', params)

        datum = equipmentDatum(equipmentId=equipment.equipment_id, equipmentTable=equipment)
        params['equipmentDatum'] = datum

        borrowingHistoryList = BorrowingHistoryTable.objects.filter(equipment_id=equipment).order_by('borrowind_datetime')
        params['borrowingHistoryList'] = borrowingHistoryList

    return render(request, 'ebis/show-borrowing-history.html', params)
