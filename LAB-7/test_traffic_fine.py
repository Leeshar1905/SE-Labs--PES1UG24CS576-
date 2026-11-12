"""
Lab 7 - Fuzz testing of traffic_fine.py with Hypothesis.

Intended behaviour (derived from the code, its prompts and examples):

parse_ticket_id("TF-2024-0456")  -> ("TF", 2024, 456)
    * exactly three parts separated by '-'
    * prefix: one or more letters A-Z / a-z (returned upper-cased)
    * year:   exactly 4 ASCII digits
    * serial: one or more ASCII digits

total_fines("500,1200,300")      -> 2000
    * comma separated, non-negative whole-number amounts
    * total is capped at 10000

speed_excess("72/60")            -> 20
    * "speed/limit", speed >= 0 and limit > 0
    * returns the whole-number percentage over the limit (0 if not over)

For ANY invalid input (wrong type, None, empty, malformed, negative, ...)
each function must return None instead of crashing.
"""

import string

from hypothesis import example, given, settings, strategies as st

from traffic_fine import parse_ticket_id, speed_excess, total_fines

# ---------------------------------------------------------------------------
# Shared strategies
# ---------------------------------------------------------------------------

# Anything a caller might wrongly pass in: text (incl. Unicode), None,
# numbers, bytes, lists, dicts ...
any_input = (
    st.text()
    | st.none()
    | st.integers()
    | st.floats(allow_nan=True, allow_infinity=True)
    | st.booleans()
    | st.binary()
    | st.lists(st.text(), max_size=3)
    | st.dictionaries(st.text(max_size=3), st.integers(), max_size=2)
)

ascii_letters = st.text(alphabet=string.ascii_letters, min_size=1, max_size=5)
ascii_digits = st.text(alphabet=string.digits, min_size=1, max_size=8)

# Characters that Python's int() treats as digits but are NOT 0-9,
# e.g. Arabic-Indic, Devanagari and full-width digits.
unicode_digit = st.characters(categories=["Nd"]).filter(
    lambda c: c not in string.digits
)

FINE_CAP = 10000


# ---------------------------------------------------------------------------
# parse_ticket_id
# ---------------------------------------------------------------------------

def _is_valid_ticket_result(result):
    return (
        isinstance(result, tuple)
        and len(result) == 3
        and isinstance(result[0], str)
        and isinstance(result[1], int)
        and isinstance(result[2], int)
    )


@given(any_input)
@settings(max_examples=300)
def test_parse_ticket_id_no_crash(s):
    """Fuzz with random text / None / other types: must never raise."""
    result = parse_ticket_id(s)
    assert result is None or _is_valid_ticket_result(result)


@given(ascii_letters, st.integers(1000, 9999), ascii_digits)
def test_parse_ticket_id_valid_input(prefix, year, serial):
    """Well-formed IDs are parsed correctly (regression check)."""
    ticket = f"{prefix}-{year}-{serial}"
    assert parse_ticket_id(ticket) == (prefix.upper(), year, int(serial))


@given(st.lists(st.text(alphabet=string.ascii_letters + string.digits),
                max_size=6).filter(lambda parts: len(parts) != 3))
@example(["TF2024"])
@example(["TF", "2024", "0456", "99"])
def test_parse_ticket_id_wrong_number_of_parts(parts):
    """IDs without exactly three '-' separated parts are rejected."""
    assert parse_ticket_id("-".join(parts)) is None


@given(ascii_letters,
       st.text(alphabet=string.ascii_letters + string.punctuation.replace("-", ""),
               min_size=1, max_size=4),
       ascii_digits)
def test_parse_ticket_id_non_numeric_year(prefix, year, serial):
    """A year containing non-digits is rejected instead of crashing."""
    assert parse_ticket_id(f"{prefix}-{year}-{serial}") is None


@given(ascii_letters, st.lists(unicode_digit, min_size=4, max_size=4), ascii_digits)
def test_parse_ticket_id_rejects_unicode_digits(prefix, year_chars, serial):
    """Non-ASCII digits (e.g. '٢٠٢٤') must not be silently accepted as a year."""
    ticket = f"{prefix}-{''.join(year_chars)}-{serial}"
    assert parse_ticket_id(ticket) is None


@given(st.text(alphabet=string.digits + string.punctuation.replace("-", "") + " ",
               max_size=4),
       st.integers(1000, 9999), ascii_digits)
@example("", 2024, "456")
def test_parse_ticket_id_bad_prefix(prefix, year, serial):
    """The prefix must be letters only and not empty."""
    assert parse_ticket_id(f"{prefix}-{year}-{serial}") is None


# ---------------------------------------------------------------------------
# total_fines
# ---------------------------------------------------------------------------

@given(any_input)
@settings(max_examples=300)
def test_total_fines_no_crash(s):
    """Fuzz with random text / None / other types: must never raise."""
    result = total_fines(s)
    assert result is None or (isinstance(result, int) and 0 <= result <= FINE_CAP)


@given(st.lists(st.integers(min_value=0, max_value=20000), min_size=1, max_size=20))
def test_total_fines_valid_input(amounts):
    """Valid CSV of non-negative amounts -> sum, capped at 10000."""
    csv = ",".join(str(a) for a in amounts)
    assert total_fines(csv) == min(sum(amounts), FINE_CAP)


@given(st.lists(st.integers(min_value=-20000, max_value=20000), min_size=1, max_size=10)
       .filter(lambda amounts: any(a < 0 for a in amounts)))
def test_total_fines_rejects_negative_amounts(amounts):
    """A negative fine is invalid - it must not reduce (or flip) the total."""
    csv = ",".join(str(a) for a in amounts)
    assert total_fines(csv) is None


@given(st.sampled_from(["", " ", ",", "500,", ",500", "500,,300", " , "]))
def test_total_fines_empty_values(csv):
    """Empty input or empty items between commas are rejected."""
    assert total_fines(csv) is None


@given(st.lists(unicode_digit, min_size=1, max_size=5))
def test_total_fines_rejects_unicode_digits(chars):
    """Non-ASCII digits are not valid amounts."""
    assert total_fines("100," + "".join(chars)) is None


@given(st.integers(min_value=4301, max_value=6000))
def test_total_fines_extremely_long_amount(num_digits):
    """A huge amount (thousands of digits) is still capped, not a crash."""
    assert total_fines("9" * num_digits) == FINE_CAP


# ---------------------------------------------------------------------------
# speed_excess
# ---------------------------------------------------------------------------

@given(any_input)
@settings(max_examples=300)
def test_speed_excess_no_crash(s):
    """Fuzz with random text / None / other types: must never raise."""
    result = speed_excess(s)
    assert result is None or (isinstance(result, int) and result >= 0)


@given(st.integers(min_value=0, max_value=1000), st.integers(min_value=1, max_value=300))
def test_speed_excess_valid_input(speed, limit):
    """Valid readings give the floor percentage over the limit (0 if not over)."""
    expected = max(0, (speed - limit) * 100 // limit)
    assert speed_excess(f"{speed}/{limit}") == expected


@given(st.integers(min_value=0, max_value=1000))
@example(0)
def test_speed_excess_zero_limit(speed):
    """A speed limit of 0 is invalid - must not raise ZeroDivisionError."""
    assert speed_excess(f"{speed}/0") is None


@given(st.integers(min_value=-1000, max_value=1000),
       st.integers(min_value=-300, max_value=300))
def test_speed_excess_negative_values(speed, limit):
    """Negative speeds or limits are rejected; otherwise result is never negative."""
    result = speed_excess(f"{speed}/{limit}")
    if speed < 0 or limit <= 0:
        assert result is None
    else:
        assert result is not None and result >= 0


@given(st.text(alphabet=string.digits + "/", max_size=10)
       .filter(lambda s: s.count("/") != 1))
@example("72")
@example("72/60/50")
def test_speed_excess_wrong_format(reading):
    """Readings without exactly one '/' are rejected."""
    assert speed_excess(reading) is None


@given(st.lists(unicode_digit, min_size=1, max_size=3))
def test_speed_excess_rejects_unicode_digits(chars):
    """Non-ASCII digits are not valid speeds."""
    assert speed_excess("".join(chars) + "/60") is None


@given(st.integers(min_value=4301, max_value=6000))
def test_speed_excess_extremely_long_number(num_digits):
    """Extremely long numbers must not crash the program."""
    result = speed_excess("9" * num_digits + "/60")
    assert result is None or (isinstance(result, int) and result >= 0)
