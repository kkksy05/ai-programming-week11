from bug3_logic import find_max, count_pass


def test_find_max():
    assert find_max([70, 85, 60, 95]) == 95
    assert find_max([10, 20, 30]) == 30


def test_count_pass():
    assert count_pass([70, 85, 95]) == 3
    assert count_pass([60, 60, 59]) == 2