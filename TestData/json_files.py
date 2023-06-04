import pytest

from Utilities.readexcel import read_data_by_value as read


def register_payload():
    return {
        "name": read("Data_Sheet", "name"),
        "email": read("Data_Sheet", "email"),
        "password": read("Data_Sheet", "password")
    }


def register_payload_with_registered_email():
    return {
        "name": read("Data_Sheet", "name"),
        "email": read("Data_Sheet", "email"),
        "password": read("Data_Sheet", "password")
    }


def login_payload():
    return {
        "email": read("Data_Sheet", "email"),
        "password": read("Data_Sheet", "password")
    }


def login_payload_with_wrong_email_password():
    return {
        "email": "mnops@gmail.com",
        "password": "qwerty"
    }


def profile_payload():
    return {
        "name": read("Data_Sheet", "name"),
        "phone": read("Data_Sheet", "phone"),
        "company": read("Data_Sheet", "company")
    }


def forgot_password_payload():
    return {
        "email": read("Data_Sheet", "email")
    }


def change_password_payload():
    return {
        "currentPassword": read("Data_Sheet", "password"),
        "newPassword": read("Data_Sheet", "new_pass")
    }


def create_notes_payload(category):
    return {
        "title": read("Data_Sheet", "title"),
        "description": read("Data_Sheet", "description"),
        "category": category
    }


def get_note_by_id_payload(note_id):
    return {
        "id": note_id
    }


def edit_note_payload(note_id):
    return {
        "id": note_id,
        "title": read("Data_Sheet", "title"),
        "description": read("Data_Sheet", "description"),
        "completed": "false",
        "category": read("Data_Sheet", "category")
    }


def update_note_as_completed_payload(note_id):
    return {
        "id": note_id,
        "completed": "true"
    }


def new_login_payload():
    return {
        "email": read("Data_Sheet", "email"),
        "password": read("Data_Sheet", "new_pass")
    }
