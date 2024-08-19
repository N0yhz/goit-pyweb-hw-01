import re
from collections import UserDict
from datetime import datetime, timedelta
from abc import ABC, abstractmethod

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        self.validate(value)
        super().__init__(value)
    
    def validate(self, value):
        if not re.fullmatch(r'\d{10}', value):
            raise ValueError(f'Phone number {value} is invalid. It must contain exactly 10 digits.')

class Birthday(Field):
    def __init__(self, value):
        self.validate(value)
        super().__init__(value)

    def validate(self, value):
        try:
            self.date = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name, phones=None, birthday=None):
        self.name = Name(name)
        self.phones = [Phone(phone) for phone in phones] if phones else []
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        phone_to_remove = self.find_phone(phone)
        if phone_to_remove:
            self.phones.remove(phone_to_remove)
        else:
            raise ValueError(f'Phone number {phone} is not found.')

    def edit_phone(self, old_phone, new_phone):
        self.remove_phone(old_phone)
        self.add_phone(new_phone)

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.now().date()
            birthday_date = self.birthday.date.date()
            next_birthday = birthday_date.replace(year=today.year)
            if next_birthday < today:
                next_birthday = next_birthday.replace(year=today.year + 1)
            return (next_birthday - today).days
        return None

    def __str__(self):
        phones_str = ', '.join(str(phone) for phone in self.phones)
        birthday_str = f", Birthday: {self.birthday}" if self.birthday else ""
        return f"Name: {self.name}, Phones: [{phones_str}]{birthday_str}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise ValueError(f"Record with name {name} not found.")

    def get_upcoming_birthdays(self, days):
        upcoming_birthdays = []
        today = datetime.now().date()
        end_date = today + timedelta(days=days)
        for record in self.data.values():
            if record.birthday:
                birthday_date = record.birthday.date.date()
                next_birthday = birthday_date.replace(year=today.year)
                if today <= next_birthday <= end_date:
                    upcoming_birthdays.append(record)
        return upcoming_birthdays

    def __str__(self):
        records = [str(record) for record in self.data.values()]
        return '\n'.join(records)

class View(ABC):

    @abstractmethod
    def display_contact(self, record):
        pass

    @abstractmethod
    def display_all_contacts(self, record):
        pass

    @abstractmethod
    def display_commands(self):
        pass

    @abstractmethod
    def display_message(self, message):
        pass

    @abstractmethod
    def display_error(self, error_message):
        pass

class ConsoleView(View):
    def display_contact(self, record):
        print(f'Name: {record.name.value}')
        for phone in record.phones:
            print(f'Phones: {phone.value}')
        if record.birthday:
            print(f'Birthday: {record.birthday.value}')
    
    def display_all_contacts(self,contacts):
        for record in contacts:
            print(record)

    def display_commands(self):
        commands = [ 
            'add [name] [phone] - Add a new contact"',
            'change [name] [old_phone] [new_phone] - Change a contact phone',
            'phone [name] - Show the phone number of a contact',
            'all - Show all contacts',
            'add-birthday [name] [birthday] - Add a birthday to a contact',
            'show-birthday [name] - Show the birthday of a conctact',
            'birthdays [days] - Show the birthdays in the next N days',
            'exit - Exit the app'
        ]
        print('Available commands:')
        for command in commands:
            print(f'{command}')

    def display_message(self, message):
        print(message)
    
    def display_error(self, error_message):
        print(f'Error: {error_message}')