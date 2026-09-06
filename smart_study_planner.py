import os

DATA_FILE = "study_log.txt"
SEPARATOR = "|"


def classify_session(duration):
    if duration < 30:
        return "Short"
    elif duration <= 90:
        return "Medium"
    else:
        return "Long"


def save_sessions(sessions):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        for s in sessions:
            file.write(SEPARATOR.join([s["subject"], s["topic"], s["date"], str(s["duration"])]) + "\n")
    print(f"\nSaved {len(sessions)} session(s) to '{DATA_FILE}'.")


def load_sessions():
    sessions = []
    if not os.path.exists(DATA_FILE):
        return sessions

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            parts = line.split(SEPARATOR)
            if len(parts) != 4:
                continue
            subject, topic, date, duration_str = parts
            try:
                duration = float(duration_str)
            except ValueError:
                continue
            sessions.append({"subject": subject, "topic": topic, "date": date, "duration": duration})

    return sessions


def add_session(sessions):
    print("\n--- Add a Study Session ---")
    subject = input("Subject: ").strip()
    topic = input("Topic covered: ").strip()
    date = input("Date / day label: ").strip()

    duration = None
    while duration is None:
        raw = input("Duration in minutes: ").strip()
        try:
            value = float(raw)
            if value <= 0:
                print("Duration must be a positive number.")
            else:
                duration = value
        except ValueError:
            print("Enter a valid number.")

    sessions.append({"subject": subject, "topic": topic, "date": date, "duration": duration})
    print(f"Session added ({classify_session(duration)}).")


def print_session_table(sessions):
    header = f'{"Subject":<15}{"Topic":<20}{"Date":<15}{"Duration(min)":<15}{"Type":<10}'
    print(header)
    print("-" * len(header))
    for s in sessions:
        print(f'{s["subject"]:<15}{s["topic"]:<20}{s["date"]:<15}{s["duration"]:<15.0f}{classify_session(s["duration"]):<10}')


def view_sessions(sessions):
    print("\n--- All Study Sessions ---")
    if not sessions:
        print("No sessions have been logged yet.")
        return
    print_session_table(sessions)


def search_by_subject(sessions):
    print("\n--- Search Sessions by Subject ---")
    query = input("Enter subject name: ").strip()
    matches = [s for s in sessions if s["subject"].lower() == query.lower()]

    if not matches:
        print(f"No sessions found for subject '{query}'.")
        return

    print_session_table(matches)
    total = sum(s["duration"] for s in matches)
    print(f"\nTotal time on '{query}': {total:.0f} minutes ({total / 60:.2f} hours)")


def study_statistics(sessions):
    print("\n--- Study Statistics ---")
    if not sessions:
        print("No sessions have been logged yet.")
        return

    total_minutes = sum(s["duration"] for s in sessions)
    print(f"Total time studied: {total_minutes / 60:.2f} hours ({total_minutes:.0f} min)")

    subject_totals = {}
    for s in sessions:
        subject_totals[s["subject"]] = subject_totals.get(s["subject"], 0) + s["duration"]

    print("\nPer subject:")
    for subject, minutes in subject_totals.items():
        print(f"  {subject:<15} {minutes / 60:.2f} hours ({minutes:.0f} min)")

    weakest = min(subject_totals, key=subject_totals.get)
    print(f"\nWeakest area: {weakest} ({subject_totals[weakest] / 60:.2f} hours)")

    longest = max(sessions, key=lambda s: s["duration"])
    print(f"Longest session: {longest['subject']} - {longest['topic']} "
          f"({longest['duration']:.0f} min, {classify_session(longest['duration'])})")


def display_menu():
    print("\n===== Smart Study Planner =====")
    print("1. Add a study session")
    print("2. View all sessions")
    print("3. Search sessions by subject")
    print("4. View statistics")
    print("5. Save and exit")


def main():
    sessions = load_sessions()
    print(f"Loaded {len(sessions)} existing session(s)." if sessions else "No existing study log found.")

    while True:
        display_menu()
        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            add_session(sessions)
        elif choice == "2":
            view_sessions(sessions)
        elif choice == "3":
            search_by_subject(sessions)
        elif choice == "4":
            study_statistics(sessions)
        elif choice == "5":
            save_sessions(sessions)
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 5.")


if __name__ == "__main__":
    main()
