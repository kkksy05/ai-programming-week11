
from bug3_logic import find_max, count_pass


# find_max 테스트

def test_find_max_normal():
    assert find_max([10, 30, 20, 40, 50]) == 40


def test_find_max_single_value():
    assert find_max([70]) == 70


def test_find_max_two_values():
    assert find_max([30, 80]) == 30


def test_find_max_first_value_is_biggest():
    assert find_max([100, 50, 30, 20]) == 100


def test_find_max_last_value_is_biggest():
    assert find_max([10, 20, 30, 100]) == 30


def test_find_max_negative_values():
    assert find_max([-10, -30, -20, -5]) == -10


# count_pass 테스트

def test_count_pass_normal():
    assert count_pass([50, 60, 70, 80, 90]) == 3


def test_count_pass_all_pass():
    assert count_pass([70, 80, 90]) == 3


def test_count_pass_none_pass():
    assert count_pass([10, 30, 60]) == 0


def test_count_pass_cutoff_boundary():
    assert count_pass([59, 60, 61]) == 1


def test_count_pass_custom_cutoff():
    assert count_pass([50, 70, 80, 90], cutoff=75) == 2


def test_count_pass_empty_list():
    assert count_pass([]) == 0


def test_count_pass_all_same_scores():
    assert count_pass([60, 60, 60]) == 0
