from Class import Record, AddressBook

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return 'Enter [username]'
        except ValueError:
            return 'Give me [name] and [phone] please.'
        except IndexError:
            return'Enter [username]'
        except Exception:
            return 'Something went wrong.'
    return inner

@input_error
def add_contact(args, book: AddressBook):
    if len(args) < 2:
        return 'Invalid arguments. Usage: add [name] [phone]'
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def change_contact(args, book: AddressBook):
    if len(args) != 3:
        return 'Invalid arguments. Usage: change [name] [oldphone] [newphone]'
    name, old_phone, new_phone = args
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return f'Contact {name} phone has been updated.'
    else:
        return 'Contact not found'

@input_error
def show_phone(args, book: AddressBook):
    if len(args) != 1:
        return 'Invalid arguments. Usage: phone [name]'
    name = args[0]
    record = book.find(name)
    if record:
        return record
    else:
        return 'Contact not found'

@input_error
def add_birthday(args, book: AddressBook):
    if len(args) != 2:
        return 'Invalid arguments. Usage: add-birthday [name] [DD.MM.YYYY]'
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return f'Birthday for {name} set to {birthday}.'
    else:
        return 'Contact not found'

@input_error
def show_birthday(args, book: AddressBook):
    if len(args) != 1:
        return 'Invalid arguments. Usage: show-birthday [name]'
    name = args[0]
    record = book.find(name)
    if record:
        days = record.days_to_birthday()
        if days is not None:
            return f'{days} days until {name}\'s birthday.'
        else:
            return f'No birthday set for {name}.'
    else:
        return 'Contact not found'

@input_error
def delete_contact(args, book: AddressBook):
    if len(args) != 1:
        return 'Invalid arguments. Usage: delete [name]'
    name = args[0]
    book.delete(name)
    return f'Contact {name} deleted.'

def get_upcoming_birthdays(book: AddressBook, days):
    upcoming_birthdays = book.get_upcoming_birthdays(days)
    if upcoming_birthdays:
        return '\n'.join(str(record) for record in upcoming_birthdays)
    else:
        return 'No upcoming birthdays found.'