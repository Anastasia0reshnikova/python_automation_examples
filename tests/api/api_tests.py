import pytest


def test_add_new_pet():
    pass

def test_get_pet_by_id():
    pass

@pytest.mark.parametrize("status", ["available", "pending", "sold"])
def test_find_pet_by_status(status):
    pass