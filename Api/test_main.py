from main import User
import pytest
from tinydb import TinyDB,table
from tinydb.storages import MemoryStorage

@pytest.fixture
def setup_db():
    User.DB = TinyDB(storage=MemoryStorage)

@pytest.fixture
def user(setup_db):
    U = User(first_name="Berte",
             last_name="Siaka",
             address="77028 Jerome Springs West Barbaramouth, MO 48836",
             phone_number= "(996)433-1002"
             )
    U.save()
    return U


def test_full_name(user):
    assert user.full_name == "Berte Siaka"


def test_db_instance(user):
    assert isinstance(user.db_instance, table.Document)
    assert user.db_instance['first_name'] == 'Berte'
    assert user.db_instance['last_name'] == 'Siaka'
    assert user.db_instance['address'] == '77028 Jerome Springs West Barbaramouth, MO 48836'
    assert user.db_instance['phone_number'] == '(996)433-1002'


def test__check_phone_number(setup_db):
    good_user = User(first_name="Berte",
             last_name="Siaka",
             address="77028 Jerome Springs West Barbaramouth, MO 48836",
             phone_number= "(996)433-1002"
                     )

    bad_user = User(first_name="Berte",
                     last_name="Paul",
                     address="77028 Jerome Springs West Barbaramouth, MO 48836",
                     phone_number="(996)433-10089"
                     )
    with pytest.raises(ValueError) as err:
        bad_user._check_phone_number()

    assert "invalide" in str(err.value)




def test__check_name():
    assert False


def test_exists(user):
    assert user.exists() is True


def test_delete():
    assert False


def test_save():
    assert False
