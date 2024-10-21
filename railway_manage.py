import pandas as pd
import os

class RailwayManagementSystem:
    def __init__(self):
        self.trains_file = 'trainbookings_info.csv'
        self.bookings_file = 'Customer_details.csv'
        self.load_data()

    def load_data(self):
        if os.path.exists(self.trains_file):
            self.trains = pd.read_csv(self.trains_file)
        else:
            self.trains = pd.DataFrame(columns=["Train Number", "Train Name", "Source", "Destination", "Departure Time", "Arrival Time", "Available Seats"])

        if os.path.exists(self.bookings_file):
            self.bookings = pd.read_csv(self.bookings_file)
        else:
            self.bookings = pd.DataFrame(columns=["Train Number", "Passenger Name"])

    def save_data(self):
        self.trains.to_csv(self.trains_file, index=False)
        self.bookings.to_csv(self.bookings_file, index=False)

    def add_train(self, train_number, train_name, source, destination, departure_time, arrival_time, available_seats):
        new_train = {
            "Train Number": train_number,
            "Train Name": train_name,
            "Source": source,
            "Destination": destination,
            "Departure Time": departure_time,
            "Arrival Time": arrival_time,
            "Available Seats": available_seats
        }
        self.trains = self.trains._append(new_train, ignore_index=True)
        self.save_data()

    def view_trains(self):
        return self.trains

    def book_ticket(self, train_number, passenger_name):
        train = self.trains[self.trains["Train Number"] == train_number]
        if train.empty:
            return "Train not found."
        elif train["Available Seats"].values[0] <= 0:
            return "No available seats."
        else:
            self.trains.loc[self.trains["Train Number"] == train_number, "Available Seats"] -= 1
            new_booking = {
                "Train Number": train_number,
                "Passenger Name": passenger_name
            }
            self.bookings = self.bookings._append(new_booking, ignore_index=True)
            self.save_data()
            return f"Ticket booked for {passenger_name} on train {train_number}."

    def view_bookings(self):
        return self.bookings

if __name__ == "__main__":
    rms = RailwayManagementSystem()


    rms.add_train("12345", "Express Train", "CityA", "CityB", "10:00 AM", "2:00 PM", 5)
    rms.add_train("67890", "Local Train", "CityC", "CityD", "3:00 PM", "5:00 PM", 3)

    # Viewing trains
    print("Available Trains:")
    print(rms.view_trains())

    # Booking a ticket
    print(rms.book_ticket("12345", "Alice Johnson"))
    print(rms.book_ticket("67890", "Bob Smith"))
    print(rms.book_ticket("67890", "Charlie Brown"))
    
    # View bookings
    print("Bookings:")
    print(rms.view_bookings())

    # Attempting to book a ticket on a fully booked train
    print(rms.book_ticket("67890", "David Lee"))
