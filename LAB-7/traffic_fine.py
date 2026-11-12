FINE_CAP = 10000
ASCII_DIGITS = "0123456789"


def _is_ascii_number(text):
    """True if text is one or more of the characters 0-9 (nothing else).

    str.isdigit() is not enough because it also accepts Unicode digits
    such as '٢' or '２', which int() would silently convert.
    """
    return len(text) > 0 and all(ch in ASCII_DIGITS for ch in text)


def _to_int(text):
    """Convert a string of ASCII digits to int, or return None if too long."""
    try:
        return int(text)
    except ValueError:
        # Python refuses to convert strings with more than ~4300 digits.
        return None


def parse_ticket_id(ticket_id):
    """Parse 'PREFIX-YEAR-SERIAL' (e.g. 'TF-2024-0456').

    Returns (PREFIX, year, serial) or None if the ticket ID is invalid.
    """
    if not isinstance(ticket_id, str):
        return None

    parts = ticket_id.strip().split('-')
    if len(parts) != 3:
        return None
    prefix, year, serial = parts

    # Prefix must be plain letters A-Z / a-z.
    if prefix == "" or not (prefix.isascii() and prefix.isalpha()):
        return None
    # Year must be exactly 4 digits, serial at least one digit.
    if len(year) != 4 or not _is_ascii_number(year):
        return None
    if not _is_ascii_number(serial):
        return None

    serial_number = _to_int(serial)
    if serial_number is None:
        return None
    return prefix.upper(), int(year), serial_number


def total_fines(amounts_csv):
    """Add up comma-separated fine amounts (e.g. '500,1200,300').

    Amounts must be non-negative whole numbers. The total is capped at
    10000. Returns None if the input is invalid.
    """
    if not isinstance(amounts_csv, str):
        return None

    total = 0
    for item in amounts_csv.split(','):
        item = item.strip()
        if not _is_ascii_number(item):
            return None          # empty, negative or non-numeric amount
        if len(item.lstrip('0')) > len(str(FINE_CAP)):
            total = FINE_CAP     # far bigger than the cap - no need to convert
        else:
            total += int(item)

    if total > FINE_CAP:
        total = FINE_CAP
    return total


def speed_excess(reading):
    """Percentage over the speed limit for a 'speed/limit' reading.

    e.g. '72/60' -> 20. Returns 0 if the driver was not over the limit and
    None if the reading is invalid (missing '/', negative, limit of 0 ...).
    """
    if not isinstance(reading, str):
        return None

    parts = reading.strip().split('/')
    if len(parts) != 2:
        return None
    speed_text, limit_text = parts[0].strip(), parts[1].strip()

    if not (_is_ascii_number(speed_text) and _is_ascii_number(limit_text)):
        return None
    speed = _to_int(speed_text)
    limit = _to_int(limit_text)
    if speed is None or limit is None or limit == 0:
        return None

    if speed <= limit:
        return 0
    return (speed - limit) * 100 // limit


def main():
    print("==== Running parse_ticket_id ====")
    user_input = input("Enter a ticket ID (e.g. TF-2024-0456): ")
    result = parse_ticket_id(user_input)
    if result is None:
        print("Invalid ticket ID. Expected format PREFIX-YEAR-SERIAL, e.g. TF-2024-0456")
    else:
        print("Ticket Prefix, Year and Serial:", result)

    print("\n==== Running total_fines ====")
    user_input = input("Enter fine amounts as CSV (e.g. 500,1200,300): ")
    result = total_fines(user_input)
    if result is None:
        print("Invalid fine amounts. Use non-negative whole numbers separated by commas.")
    else:
        print("Total Fines:", result)

    print("\n==== Running speed_excess ====")
    user_input = input("Enter speed/limit (e.g. 72/60): ")
    result = speed_excess(user_input)
    if result is None:
        print("Invalid reading. Use speed/limit with non-negative numbers and a limit above 0.")
    else:
        print("Percent Over Limit:", result)


if __name__ == "__main__":
    main()
