import pickle
from action import (
    add_contact,
    change_contact,
    show_phone,
    add_birthday,
    show_birthday,
    get_upcoming_birthdays,
    delete_contact
)
from Class import AddressBook, ConsoleView, Record
from parse import parse_input

def save_data(book, filename = 'address_book.pkl'):
    with open(filename, 'wb') as f:
        pickle.dump(book, f)

def load_data(filename = 'address_book.pkl'):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()

def main():
    view = ConsoleView()
    book = load_data()

    view.display_message("Welcome to the assistant bot!")
    
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            view.display_message("Good bye!")
            break

        elif command == "hello":
            view.display_message("How can I help you?")

        elif command == "add":
            view.display_message(add_contact(args, book))

        elif command == "change":
            view.display_message(change_contact(args, book))

        elif command == "phone":
            contact = show_phone(args, book)
            if contact:
                if isinstance(contact, Record):
                    view.display_contact(contact)
                else:
                    view.display_error("Unexpected error: Contact is not a valid Record object.")
            else:
                view.display_error('Contact not found.')

        elif command == "all":
            view.display_all_contacts(book.values())

        elif command == "add-birthday":
            view.display_message(add_birthday(args, book))

        elif command == "show-birthday":
            birthday_info = show_birthday(args, book)
            if birthday_info:
                view.display_message(birthday_info)
            else:
                view.display_error('birthday not found.')

        elif command == "birthdays":
            if len(args) != 1:
                view.display_message("Invalid arguments. Usage: birthdays [days]")
            else:
                try:
                    days = int(args[0])
                    view.display_message(get_upcoming_birthdays(book, days))
                except ValueError:
                    view.display_error("Invalid number of days.")

        elif command == "delete":
            view.display_message(delete_contact(args, book))

        else:
            view.display_error("Invalid command.")

    save_data(book)

if __name__ == "__main__":
    main()