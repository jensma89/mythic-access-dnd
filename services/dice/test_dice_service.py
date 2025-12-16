# """
# test_dice_service.py
# 
# Test for dice service - business logic.
# """
# import pytest
# import uuid
# 
# from services.dice.dice_service import DiceService
# from services.dice.dice_service_exceptions import (
#     DiceNotFoundError,
#     DiceCreateError,
#     DiceUpdateError,
#     DiceDeleteError,
#     DiceServiceError
# )
# from models.schemas.dice_schema import DiceCreate, DiceUpdate
# from models.db_models.test_db import get_session as get_test_session
# from repositories.sql_dice_repository import SqlAlchemyDiceRepository
# from repositories.sql_dicelog_repository import SqlAlchemyDiceLogRepository
# 
# 
# def test_create_dice():
#     """Test to create a new dice."""
#     gen = get_test_session()
#     session = next(gen)
# 
#     service = DiceService(
#         repository=SqlAlchemyDiceRepository(session),
#         log_repository=SqlAlchemyDiceLogRepository(session)
#     )
# 
#     suffix = uuid.uuid4().hex[:8]
#     dice_data = DiceCreate(
#         name=f"d20_{suffix}",
#         sides=20
#     )
#     dice = service.create_dice(dice_data)
# 
#     assert dice.name == f"d20_{suffix}"
#     assert dice.sides == 20
#     assert dice.id is not None
# 
# 
# def test_get_dice():
#     """Test to get a dice by ID."""
#     gen = get_test_session()
#     session = next(gen)
# 
#     service = DiceService(
#         repository=SqlAlchemyDiceRepository(session),
#         log_repository=SqlAlchemyDiceLogRepository(session)
#     )
# 
#     suffix = uuid.uuid4().hex[:8]
#     dice_data = DiceCreate(
#         name=f"d12_{suffix}",
#         sides=12
#     )
#     created = service.create_dice(dice_data)
# 
#     result = service.get_dice(created.id)
# 
#     assert result.id == created.id
#     assert result.name == f"d12_{suffix}"
#     assert result.sides == 12
# 
# 
# def test_get_dice_not_found():
#     """Test get dice with non-existent ID."""
#     gen = get_test_session()
#     session = next(gen)
# 
#     service = DiceService(
#         repository=SqlAlchemyDiceRepository(session),
#         log_repository=SqlAlchemyDiceLogRepository(session)
#     )
# 
#     with pytest.raises(DiceNotFoundError):
#         service.get_dice(99999)
# 
# 
# def test_list_dices():
#     """Test to list all dices."""
#     gen = get_test_session()
#     session = next(gen)
# 
#     service = DiceService(
#         repository=SqlAlchemyDiceRepository(session),
#         log_repository=SqlAlchemyDiceLogRepository(session)
#     )
# 
#     suffix1 = uuid.uuid4().hex[:8]
#     dice1_data = DiceCreate(
#         name=f"d6_{suffix1}",
#         sides=6
#     )
#     service.create_dice(dice1_data)
# 
#     suffix2 = uuid.uuid4().hex[:8]
#     dice2_data = DiceCreate(
#         name=f"d8_{suffix2}",
#         sides=8
#     )
#     service.create_dice(dice2_data)
# 
#     dices = service.list_dices(offset=0, limit=100)
# 
#     assert isinstance(dices, list)
# 
# 
# def test_list_dices_with_filter():
#     """Test list dices with offset and limit."""
#     gen = get_test_session()
#     session = next(gen)
# 
#     service = DiceService(
#         repository=SqlAlchemyDiceRepository(session),
#         log_repository=SqlAlchemyDiceLogRepository(session)
#     )
# 
#     suffix = uuid.uuid4().hex[:8]
#     dice_data = DiceCreate(
#         name=f"d10_{suffix}",
#         sides=10
#     )
#     service.create_dice(dice_data)
# 
#     dices = service.list_dices(offset=0, limit=10)
# 
#     assert isinstance(dices, list)
#     assert len(dices) <= 10
# 
# 
# def test_update_dice():
#     """Test to update a dice."""
#     gen = get_test_session()
#     session = next(gen)
# 
#     service = DiceService(
#         repository=SqlAlchemyDiceRepository(session),
#         log_repository=SqlAlchemyDiceLogRepository(session)
#     )
# 
#     suffix = uuid.uuid4().hex[:8]
#     dice_data = DiceCreate(
#         name=f"d4_{suffix}",
#         sides=4
#     )
#     dice = service.create_dice(dice_data)
# 
#     new_suffix = uuid.uuid4().hex[:8]
#     update_data = DiceUpdate(name=f"d4_updated_{new_suffix}")
#     updated = service.update_dice(dice.id, update_data)
# 
#     assert updated is not None
#     assert updated.id == dice.id
#     assert updated.name == f"d4_updated_{new_suffix}"
# 
# 
# def test_update_dice_not_found():
#     """Test update with non-existent dice ID."""
#     gen = get_test_session()
#     session = next(gen)
# 
#     service = DiceService(
#         repository=SqlAlchemyDiceRepository(session),
#         log_repository=SqlAlchemyDiceLogRepository(session)
#     )
# 
#     update_data = DiceUpdate(name="new_name")
# 
#     with pytest.raises((DiceNotFoundError, DiceServiceError)):
#         service.update_dice(99999, update_data)
# 
# 
# def test_delete_dice():
#     """Test to delete a dice."""
#     gen = get_test_session()
#     session = next(gen)
# 
#     service = DiceService(
#         repository=SqlAlchemyDiceRepository(session),
#         log_repository=SqlAlchemyDiceLogRepository(session)
#     )
# 
#     suffix = uuid.uuid4().hex[:8]
#     dice_data = DiceCreate(
#         name=f"d100_{suffix}",
#         sides=100
#     )
#     dice = service.create_dice(dice_data)
# 
#     deleted = service.delete_dice(dice.id)
# 
#     assert deleted is not None
# 
#     # Verify dice is gone
#     with pytest.raises(DiceNotFoundError):
#         service.get_dice(dice.id)
# 
# 
# def test_delete_dice_not_found():
#     """Test delete with non-existent dice ID."""
#     gen = get_test_session()
#     session = next(gen)
# 
#     service = DiceService(
#         repository=SqlAlchemyDiceRepository(session),
#         log_repository=SqlAlchemyDiceLogRepository(session)
#     )
# 
#     with pytest.raises((DiceNotFoundError, DiceDeleteError, DiceServiceError)):
#         service.delete_dice(99999)
