import json
import datetime
import sys

def load_notes():
    try:
        with open('notes.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_notes(notes):
    with open('notes.json', 'w') as f:
        json.dump(notes, f, indent=2, default=str)

def add_note(title, body):
    notes = load_notes()
    note_id = len(notes) + 1
    note = {
        'id': note_id,
        'title': title,
        'body': body,
        'last_modified': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    notes.append(note)
    save_notes(notes)
    print(f"Note {note_id} added successfully.")

def edit_note(note_id, title=None, body=None):
    notes = load_notes()
    for note in notes:
        if int(note['id']) == note_id:
            if title:
                note['title'] = title
            if body:
                note['body'] = body
            note['last_modified'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            save_notes(notes)
            print(f"Note {note_id} updated successfully.")
            return
    print(f"Note {note_id} not found.")

def delete_note(note_id):
    notes = load_notes()
    new_notes = [note for note in notes if int(note['id']) != note_id]
    if len(new_notes) != len(notes):
        save_notes(new_notes)
        print(f"Note {note_id} deleted successfully.")
    else:
        print(f"Note {note_id} not found.")

def list_notes(since=None):
    notes = load_notes()
    filtered_notes = [note for note in notes if not since or datetime.datetime.strptime(note['last_modified'], '%Y-%m-%d %H:%M:%S') >= since]
    for note in filtered_notes:
        print(f"ID: {note['id']}, Title: {note['title']}, Last Modified: {note['last_modified']}")
        print(f"Body: {note['body']}\n")

def main():
    if len(sys.argv) < 2:
        print("Available commands: add, edit, delete, list, exit")
        command = input("Enter command: ")
    else:
        command = sys.argv[1]

    if command == "add":
        if len(sys.argv) < 4:
            title = input("Enter note title: ")
            body = input("Enter note body: ")
        else:
            title = sys.argv[2]
            body = sys.argv[3]
        add_note(title, body)
    elif command == "edit":
        if len(sys.argv) < 4:
            note_id = input("Enter note ID: ")
            title = input("Enter new note title (leave blank to keep current): ")
            body = input("Enter new note body (leave blank to keep current): ")
        else:
            note_id = sys.argv[2]
            title = sys.argv[3] if len(sys.argv) > 3 else None
            body = sys.argv[4] if len(sys.argv) > 4 else None
        edit_note(note_id, title, body)
    elif command == "delete":
        if len(sys.argv) < 3:
            note_id = input("Enter note ID: ")
        else:
            note_id = sys.argv[2]
        delete_note(note_id)
    elif command == "list":
        since_str = input("Filter notes by date (YYYY-MM-DD, leave blank for all): ")
        since = datetime.datetime.strptime(since_str, '%Y-%m-%d') if since_str else None
        list_notes(since)
    elif command == "exit":
        sys.exit(0)
    else:
        print("Invalid command.")

    main()

if __name__ == "__main__":
    main()