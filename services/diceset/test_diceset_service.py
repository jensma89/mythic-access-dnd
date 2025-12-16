# """
# test_diceset_service.py
# 
# Test for diceset service - business logic.
# """
# import pytest
# import uuid
# 
# from services.diceset.diceset_service import DiceSetService
# from services.diceset.diceset_service_exceptions import (
#     DiceSetNotFoundError,
#     DiceSetCreateError,
#     DiceSetUpdateError,
#     DiceSetDeleteError,
#     DiceSetServiceError
# )
# from models.schemas.diceset_schema import DiceSetCreate, DiceSetUpdate
# from models.db_models.test_db import get_session as get_test_session
# from repositories.sql_dice_repository import SqlAlchemyDiceRepository
# from repositories.sql_diceset_repository import SqlAlchemyDiceSetRepository
# from repositories.sql_dicelog_repository import SqlAlchemyDiceLogRepository
# from auth.test_helpers import create_test_user, create_test_campaign
# from services.dnd_class.class_service import ClassService
# from models.schemas.dice_schema import DiceCreate
# from services.dice.dice_service import DiceService
# from repositories.sql_class_repository import SqlAlchemyClassRepository
# from models.schemas.class_schema import ClassCreate
# 
# 
# def test_create_diceset():
#     """Test to create a new dice set."""
#     gen = get_test_session()
#     session = next(gen)
# 
#     user = create_test_user(session)
#     campaign = create_test_campaign(session, user)
# 
#     # Create a class for the dice set
#     class_service = ClassService(
#         class_repo=SqlAlchemyClassRepository(session),
#         diceset_repo=SqlAlchemyDiceSetRepository(session),
#         dicelog_repo=SqlAlchemyDiceLogRepository(session)
#     )
#     suffix = uuid.uuid4().hex[:8]
#     class_data = ClassCreate(
#         name=f"Test Class {suffix}",
#         dnd_class="Wizard",
#         race="Elf",
#         campaign_id=campaign.id
#     )
#     class_data.set_user(user.id)
#     dnd_class = class_service.create_class(class_data)
# 
#     # Create dice set
#     service = DiceSetService(
#         dice_repo=SqlAlchemyDiceRepository(session),
#         diceset_repo=SqlAlchemyDiceSetRepository(session),
#         dicelog_repo=SqlAlchemyDiceLogRepository(session)
#     )
# 
#     set_suffix = uuid.uuid4().hex[:8]
#     diceset_data = DiceSetCreate(
#         name=f"Test DiceSet {set_suffix}",
#         dnd_class_id=dnd_class.id,
#         campaign_id=campaign.id,
#         dice_ids=[]
#     )
#     diceset_data.set_user(user.id)
# 
#     diceset = service.create_diceset(diceset_data)
# 
#     assert diceset.name == f"Test DiceSet {set_suffix}"
#     assert diceset.id is not None
# 
# 
# def test_get_diceset():
#     """Test to get a dice set by ID."""
#     gen = get_test_session()
#     session = next(gen)
# 
#     user = create_test_user(session)
#     campaign = create_test_campaign(session, user)
# 
#     # Create a class
#     class_service = ClassService(
#         class_repo=SqlAlchemyClassRepository(session),
#         diceset_repo=SqlAlchemyDiceSetRepository(session),
#         dicelog_repo=SqlAlchemyDiceLogRepository(session)
#     )
#     suffix = uuid.uuid4().hex[:8]
#     class_data = ClassCreate(
#         name=f"Test Class {suffix}",
#         dnd_class="Rogue",
#         race="Halfling",
#         campaign_id=campaign.id
#     )
#     class_data.set_user(user.id)
#     dnd_class = class_service.create_class(class_data)
# 
#     service = DiceSetService(
#         dice_repo=SqlAlchemyDiceRepository(session),
#         diceset_repo=SqlAlchemyDiceSetRepository(session),
#         dicelog_repo=SqlAlchemyDiceLogRepository(session)
#     )
# 
#     set_suffix = uuid.uuid4().hex[:8]
#     diceset_data = DiceSetCreate(
#         name=f"Get Test DiceSet {set_suffix}",
#         dnd_class_id=dnd_class.id,
#         campaign_id=campaign.id
#     )
#     diceset_data.set_user(user.id)
#     created = service.create_diceset(diceset_data)
# 
#     result = service.get_diceset(created.id)
# 
#     assert result.id == created.id
#     assert result.name == f"Get Test DiceSet {set_suffix}"
# 
# 
# def test_get_diceset_not_found():
#     """Test get dice set with non-existent ID."""
#     gen = get_test_session()
#     session = next(gen)
# 
#     service = DiceSetService(
#         dice_repo=SqlAlchemyDiceRepository(session),
#         diceset_repo=SqlAlchemyDiceSetRepository(session),
#         dicelog_repo=SqlAlchemyDiceLogRepository(session)
#     )
# 
#     with pytest.raises(DiceSetNotFoundError):
#         service.get_diceset(99999)
# 
# 
# def test_list_dicesets():
#     """Test to list all dice sets."""
#     gen = get_test_session()
#     session = next(gen)
# 
#     user = create_test_user(session)
#     campaign = create_test_campaign(session, user)
# 
#     # Create a class
#     class_service = ClassService(
#         class_repo=SqlAlchemyClassRepository(session),
#         diceset_repo=SqlAlchemyDiceSetRepository(session),
#         dicelog_repo=SqlAlchemyDiceLogRepository(session)
#     )
#     suffix = uuid.uuid4().hex[:8]
#     class_data = ClassCreate(
#         name=f"Test Class {suffix}",
#         dnd_class="Cleric",
#         race="Dwarf",
#         campaign_id=campaign.id
#     )
#     class_data.set_user(user.id)
#     dnd_class = class_service.create_class(class_data)
# 
#     service = DiceSetService(
#         dice_repo=SqlAlchemyDiceRepository(session),
#         diceset_repo=SqlAlchemyDiceSetRepository(session),
#         dicelog_repo=SqlAlchemyDiceLogRepository(session)
#     )
# 
#     set1_suffix = uuid.uuid4().hex[:8]
#     diceset1_data = DiceSetCreate(
#         name=f"List DiceSet 1 {set1_suffix}",
#         dnd_class_id=dnd_class.id,
#         campaign_id=campaign.id
#     )
#     diceset1_data.set_user(user.id)
#     service.create_diceset(diceset1_data)
# 
#     set2_suffix = uuid.uuid4().hex[:8]
#     diceset2_data = DiceSetCreate(
#         name=f"List DiceSet 2 {set2_suffix}",
#         dnd_class_id=dnd_class.id,
#         campaign_id=campaign.id
#     )
#     diceset2_data.set_user(user.id)
#     service.create_diceset(diceset2_data)
# 
#     dicesets = service.list_dicesets(offset=0, limit=100)
# 
#     assert isinstance(dicesets, list)
# 
# 
# def test_list_dicesets_with_filter():
#     """Test list dice sets with offset and limit."""
#     gen = get_test_session()
#     session = next(gen)
# 
#     user = create_test_user(session)
#     campaign = create_test_campaign(session, user)
# 
#     # Create a class
#     class_service = ClassService(
#         class_repo=SqlAlchemyClassRepository(session),
#         diceset_repo=SqlAlchemyDiceSetRepository(session),
#         dicelog_repo=SqlAlchemyDiceLogRepository(session)
#     )
#     suffix = uuid.uuid4().hex[:8]
#     class_data = ClassCreate(
#         name=f"Test Class {suffix}",
#         dnd_class="Fighter",
#         race="Human",
#         campaign_id=campaign.id
#     )
#     class_data.set_user(user.id)
#     dnd_class = class_service.create_class(class_data)
# 
#     service = DiceSetService(
#         dice_repo=SqlAlchemyDiceRepository(session),
#         diceset_repo=SqlAlchemyDiceSetRepository(session),
#         dicelog_repo=SqlAlchemyDiceLogRepository(session)
#     )
# 
#     set_suffix = uuid.uuid4().hex[:8]
#     diceset_data = DiceSetCreate(
#         name=f"filtered_diceset_{set_suffix}",
#         dnd_class_id=dnd_class.id,
#         campaign_id=campaign.id
#     )
#     diceset_data.set_user(user.id)
#     service.create_diceset(diceset_data)
# 
#     dicesets = service.list_dicesets(offset=0, limit=10)
# 
#     assert isinstance(dicesets, list)
#     assert len(dicesets) <= 10
# 
# 
# def test_update_diceset():
#     """Test to update a dice set."""
#     gen = get_test_session()
#     session = next(gen)
# 
#     user = create_test_user(session)
#     campaign = create_test_campaign(session, user)
# 
#     # Create a class
#     class_service = ClassService(
#         class_repo=SqlAlchemyClassRepository(session),
#         diceset_repo=SqlAlchemyDiceSetRepository(session),
#         dicelog_repo=SqlAlchemyDiceLogRepository(session)
#     )
#     suffix = uuid.uuid4().hex[:8]
#     class_data = ClassCreate(
#         name=f"Test Class {suffix}",
#         dnd_class="Ranger",
#         race="Elf",
#         campaign_id=campaign.id
#     )
#     class_data.set_user(user.id)
#     dnd_class = class_service.create_class(class_data)
# 
#     service = DiceSetService(
#         dice_repo=SqlAlchemyDiceRepository(session),
#         diceset_repo=SqlAlchemyDiceSetRepository(session),
#         dicelog_repo=SqlAlchemyDiceLogRepository(session)
#     )
# 
#     set_suffix = uuid.uuid4().hex[:8]
#     diceset_data = DiceSetCreate(
#         name=f"update_test_{set_suffix}",
#         dnd_class_id=dnd_class.id,
#         campaign_id=campaign.id
#     )
#     diceset_data.set_user(user.id)
#     diceset = service.create_diceset(diceset_data)
# 
#     new_suffix = uuid.uuid4().hex[:8]
#     update_data = DiceSetUpdate(name=f"updated_diceset_{new_suffix}")
#     updated = service.update_diceset(diceset.id, update_data)
# 
#     assert updated is not None
#     assert updated.id == diceset.id
# 
# 
# def test_update_diceset_not_found():
#     """Test update with non-existent dice set ID."""
#     gen = get_test_session()
#     session = next(gen)
# 
#     service = DiceSetService(
#         dice_repo=SqlAlchemyDiceRepository(session),
#         diceset_repo=SqlAlchemyDiceSetRepository(session),
#         dicelog_repo=SqlAlchemyDiceLogRepository(session)
#     )
# 
#     update_data = DiceSetUpdate(name="new_name")
# 
#     with pytest.raises((DiceSetNotFoundError, DiceSetServiceError)):
#         service.update_diceset(99999, update_data)
# 
# 
# def test_delete_diceset():
#     """Test to delete a dice set."""
#     gen = get_test_session()
#     session = next(gen)
# 
#     user = create_test_user(session)
#     campaign = create_test_campaign(session, user)
# 
#     # Create a class
#     class_service = ClassService(
#         class_repo=SqlAlchemyClassRepository(session),
#         diceset_repo=SqlAlchemyDiceSetRepository(session),
#         dicelog_repo=SqlAlchemyDiceLogRepository(session)
#     )
#     suffix = uuid.uuid4().hex[:8]
#     class_data = ClassCreate(
#         name=f"Test Class {suffix}",
#         dnd_class="Monk",
#         race="Human",
#         campaign_id=campaign.id
#     )
#     class_data.set_user(user.id)
#     dnd_class = class_service.create_class(class_data)
# 
#     service = DiceSetService(
#         dice_repo=SqlAlchemyDiceRepository(session),
#         diceset_repo=SqlAlchemyDiceSetRepository(session),
#         dicelog_repo=SqlAlchemyDiceLogRepository(session)
#     )
# 
#     set_suffix = uuid.uuid4().hex[:8]
#     diceset_data = DiceSetCreate(
#         name=f"Delete Test DiceSet {set_suffix}",
#         dnd_class_id=dnd_class.id,
#         campaign_id=campaign.id
#     )
#     diceset_data.set_user(user.id)
#     diceset = service.create_diceset(diceset_data)
# 
#     deleted = service.delete_diceset(diceset.id)
# 
#     assert deleted is not None
# 
#     # Verify dice set is gone
#     with pytest.raises(DiceSetNotFoundError):
#         service.get_diceset(diceset.id)
# 
# 
# def test_delete_diceset_not_found():
#     """Test delete with non-existent dice set ID."""
#     gen = get_test_session()
#     session = next(gen)
# 
#     service = DiceSetService(
#         dice_repo=SqlAlchemyDiceRepository(session),
#         diceset_repo=SqlAlchemyDiceSetRepository(session),
#         dicelog_repo=SqlAlchemyDiceLogRepository(session)
#     )
# 
#     with pytest.raises((DiceSetNotFoundError, DiceSetDeleteError, DiceSetServiceError)):
#         service.delete_diceset(99999)
