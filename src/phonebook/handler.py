from django.db import transaction


class PhonebookHandler:
    @transaction.atomic
    def create(self): ...

    @transaction.atomic
    def update(self): ...

    @transaction.atomic
    def delete(self): ...

    @transaction.atomic
    def add_to_group(self): ...

    @transaction.atomic
    def remove_from_group(self): ...

    @transaction.atomic
    def add_number(self): ...

    @transaction.atomic
    def remove_number(self): ...
