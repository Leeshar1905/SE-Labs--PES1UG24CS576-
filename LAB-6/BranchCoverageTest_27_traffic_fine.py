
import pytest

from traffic_fine import speeding_fine, license_action, total_penalty


# ==========================================
# BRANCH COVERAGE TESTS - TRAFFIC FINE
# ==========================================


# 1. Speeding fine: test both outcomes of every decision


def test_speed_equal_to_limit():
    assert speeding_fine(60, 60, "city") == 0


def test_speed_below_limit():
    assert speeding_fine(50, 60, "city") == 0


def test_school_zone():
    assert speeding_fine(70, 60, "school") == 2000


def test_highway_zone():
    assert speeding_fine(70, 60, "highway") == 1000


def test_city_zone():
    assert speeding_fine(70, 60, "city") == 500


def test_unknown_zone_uses_default_fine():
    assert speeding_fine(70, 60, "residential") == 500


def test_excess_exactly_40():
    assert speeding_fine(100, 60, "city") == 1000


def test_excess_above_40():
    assert speeding_fine(101, 60, "city") == 1500


def test_excess_exactly_20():
    assert speeding_fine(80, 60, "city") == 500


def test_excess_above_20():
    assert speeding_fine(81, 60, "city") == 1000


# 2. Licence action: test all decision branches


def test_points_below_4():
    assert license_action(3, False, False) == "none"


def test_points_exactly_4():
    assert license_action(4, False, False) == "notice"


def test_points_below_8():
    assert license_action(7, False, False) == "notice"


def test_points_exactly_8():
    assert license_action(8, False, False) == "warning"


def test_repeat_offender():
    assert license_action(8, False, True) == "suspend"


def test_non_repeat_offender():
    assert license_action(8, False, False) == "warning"


def test_points_below_12():
    assert license_action(11, False, False) == "warning"


def test_points_exactly_12_commercial():
    assert license_action(12, True, False) == "revoke"


def test_points_12_non_commercial():
    assert license_action(12, False, False) == "suspend"


def test_points_12_commercial_repeat():
    assert license_action(12, True, True) == "revoke"


# 3. Total penalty: test loop, exception and cap branches


def test_empty_list():
    assert total_penalty([]) == 0


def test_valid_single_fine():
    assert total_penalty([500]) == 500


def test_multiple_valid_fines():
    assert total_penalty([1000, 2000, 3000]) == 6000


def test_negative_fine_raises_error():
    with pytest.raises(ValueError, match="negative fine"):
        total_penalty([-100])


def test_exactly_10000_penalty():
    assert total_penalty([5000, 5000]) == 10000


def test_penalty_above_10000():
    assert total_penalty([6000, 6000]) == 10000
