
import pytest

from traffic_fine import speeding_fine, license_action, total_penalty


# ==========================================
# CODE COVERAGE TESTS - TRAFFIC FINE
# ==========================================


# 1. Tests for speeding_fine()


def test_no_speeding():
    assert speeding_fine(50, 60, "city") == 0


def test_school_zone_fine():
    assert speeding_fine(70, 60, "school") == 2000


def test_highway_zone_fine():
    assert speeding_fine(70, 60, "highway") == 1000


def test_city_zone_fine():
    assert speeding_fine(70, 60, "city") == 500


def test_speed_excess_above_20():
    assert speeding_fine(85, 60, "city") == 1000


def test_speed_excess_above_40():
    assert speeding_fine(110, 60, "city") == 1500


# 2. Tests for license_action()


def test_clean_record():
    assert license_action(2, False, False) == "none"


def test_notice_action():
    assert license_action(4, False, False) == "notice"


def test_warning_action():
    assert license_action(8, False, False) == "warning"


def test_repeat_offender_suspension():
    assert license_action(8, False, True) == "suspend"


def test_commercial_driver_revocation():
    assert license_action(12, True, False) == "revoke"


def test_non_commercial_driver_suspension():
    assert license_action(12, False, False) == "suspend"


# 3. Tests for total_penalty()


def test_empty_fine_list():
    assert total_penalty([]) == 0


def test_single_fine():
    assert total_penalty([500]) == 500


def test_multiple_fines():
    assert total_penalty([500, 1000, 1500]) == 3000


def test_negative_fine():
    with pytest.raises(ValueError, match="negative fine"):
        total_penalty([500, -100, 200])


def test_penalty_limit():
    assert total_penalty([6000, 5000]) == 10000
