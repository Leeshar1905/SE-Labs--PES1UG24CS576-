def parse_ticket_id(ticket_id):
    prefix, year, serial = ticket_id.split('-')
    return prefix.upper(), int(year), int(serial)

def total_fines(amounts_csv):
    amounts = [int(a) for a in amounts_csv.split(',')]
    total = sum(amounts)
    if total > 10000:
        total = 10000
    return total

def speed_excess(reading):
    speed, limit = reading.split('/')
    return (int(speed) - int(limit)) * 100 // int(limit)

def main():
    print("==== Running parse_ticket_id ====")
    user_input = input("Enter a ticket ID (e.g. TF-2024-0456): ")
    result = parse_ticket_id(user_input)
    print("Ticket Prefix, Year and Serial:", result)

    print("\n==== Running total_fines ====")
    user_input = input("Enter fine amounts as CSV (e.g. 500,1200,300): ")
    result = total_fines(user_input)
    print("Total Fines:", result)

    print("\n==== Running speed_excess ====")
    user_input = input("Enter speed/limit (e.g. 72/60): ")
    result = speed_excess(user_input)
    print("Percent Over Limit:", result)

if __name__ == "__main__":
    main()
