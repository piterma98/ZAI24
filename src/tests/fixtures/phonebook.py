import random

from faker import Faker

from phonebook.models import PhonebookEntry, PhonebookGroup, PhonebookNumber


class PhonebookFixture:
    fake: Faker

    def create_phonebook_entry(
        self, create_numbers: bool = True, create_groups: bool = True, **kwargs
    ) -> PhonebookEntry:
        if "name" not in kwargs:
            kwargs["name"] = "Test entry"
        if "city" not in kwargs:
            kwargs["city"] = self.fake.city()
        if "street" not in kwargs:
            kwargs["street"] = self.fake.street_address()
        if "postal_code" not in kwargs:
            kwargs["postal_code"] = self.fake.postcode()
        if "country" not in kwargs:
            kwargs["country"] = self.fake.country()
        if "type" not in kwargs:
            kwargs["type"] = random.choice(["enterprise", "personal"])
        entry = PhonebookEntry(**kwargs)
        entry.save()
        if create_numbers:
            for _ in range(2):
                PhonebookNumber.objects.create(
                    phonebook_entry=entry,
                    number=self.fake.phone_number(),
                    type=random.choice(["enterprise", "personal"]),
                )
        if create_groups:
            for _ in range(2):
                group = PhonebookGroup.objects.create(name=self.fake.word())
                entry.groups.add(group)
        return entry

    def add_phonebook_entry_number(self, entry: PhonebookEntry, number: str, number_type: str) -> PhonebookNumber:
        return PhonebookNumber.objects.create(
            phonebook_entry=entry,
            number=number,
            type=number_type,
        )

    def add_phonebook_group(self, entry: PhonebookEntry, name: str) -> PhonebookGroup:
        group = PhonebookGroup.objects.create(name=name)
        entry.groups.add(group)
        return group
