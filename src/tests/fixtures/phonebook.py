from faker import Faker


class PhonebookFixture:
    fake: Faker

    def create_phonebook_entry(self): ...
