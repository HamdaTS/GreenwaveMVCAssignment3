# controller/controller.py
from model.models import *
import pickle

class GreenWaveController:
    def __init__(self):
        self.attendees = self.load_data("attendees.pkl")
        self.ticket_types = [
            TicketType("Single", 100, ["A"]),
            TicketType("Double", 150, ["A", "B"]),
            TicketType("Full", 200, ["A", "B", "C"])
        ]
        self.logged_in = None

    def save_data(self, filename, data):
        # Save objects to a binary file
        with open(filename, 'wb') as f:
            pickle.dump(data, f)

    def load_data(self, filename):
        # Load objects from a binary file
        try:
            with open(filename, 'rb') as f:
                return pickle.load(f)
        except (FileNotFoundError, EOFError):
            return []

    def create_account(self, username, password, email):
        # Ensure username is unique
        for att in self.attendees:
            if att.account.username == username:
                raise ValueError("Username already exists")
        new_account = Account(username, password, email)
        new_attendee = Attendee(new_account)
        self.attendees.append(new_attendee)
        self.save_data("attendees.pkl", self.attendees)

    def login(self, username, password):
        for att in self.attendees:
            if att.account.username == username and att.account.password == password:
                self.logged_in = att
                return
        raise ValueError("Invalid username or password")

    def delete_account(self, username, password):
        for att in self.attendees:
            if att.account.username == username and att.account.password == password:
                self.attendees.remove(att)
                self.save_data("attendees.pkl", self.attendees)
                return
        raise ValueError("Account not found or password mismatch")

    def get_logged_in_attendee(self):
        return self.logged_in

    def logout(self):
        self.logged_in = None

    def get_ticket_types(self):
        return self.ticket_types
