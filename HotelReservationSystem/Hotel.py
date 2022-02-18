from tabulate import tabulate
from datetime import date

from DeluxeRoom import DeluxeRoom
from StandardRoom import StandardRoom
from SuiteRoom import SuiteRoom


class Hotel:
    """Hotel class to describe a Hotel & its functionalities"""

    def __init__(self, hotel_details):
        self.id = hotel_details['id']
        self.name = hotel_details['name']
        self.location = hotel_details['location']
        self.star_rating = hotel_details['star_rating']
        self.reviews = hotel_details['reviews']
        self.rooms = []

        for room in hotel_details['rooms']:
            new_room = None

            if room['type'] == 'STANDARD':
                new_room = StandardRoom(room)
            elif room['type'] == 'DELUXE':
                new_room = DeluxeRoom(room)
            elif room['type'] == 'SUITE':
                new_room = SuiteRoom(room)

            if new_room is not None:
                self.rooms.append(new_room)

    def show_unavailability_for_selected_room(self, room_id, db):
        today = date.today()

        db.execute('''SELECT * FROM bookings WHERE room_id = ? and booked_from >= ?''',
                   [int(room_id), today])

        print('Unavailable dates for this room: ')

        header = ['BOOKED_FROM', 'BOOKED_UNTIL']
        rows = []

        for booking_row in db.get_cursor:
            booked_from = booking_row['booked_from']
            booked_until = booking_row['booked_until']

            rows.append([booked_from, booked_until])

        if len(rows):
            print(tabulate(rows, header, tablefmt='grid'))
        else:
            print('  There are no bookings for this room.')

    def book_room(self, db):
        rooms = []
        room_ids = []

        for room in self.rooms:
            room_dict = vars(room)
            rooms.append(room_dict)
            room_ids.append(room_dict['id'])

        while True:
            room_price = 0
            customer_name = input('\nEnter the name of the guest: ')
            room_id = int(input('Select the preferred room id: '))

            if room_id not in room_ids:
                print('\n Invalid room id. Please check and try again.')
                continue

            self.show_unavailability_for_selected_room(room_id, db)

            try:
                check_in_date = date.fromisoformat(input('Enter a check-in date in YYYY-MM-DD format: '))
                check_out_date = date.fromisoformat(input('Enter a check-out date in YYYY-MM-DD format: '))
                today = date.today()
            except ValueError:
                print('\n Invalid check-in/check-out date. Please check and try again.')
                continue

            if check_in_date < today:
                print('\n Check-in date cannot be before today\'s date. Please check and try again.')
                continue

            if check_out_date < check_in_date:
                print('\n Check-out date cannot be before check-in date. Please check and try again.')
                continue

            # check if the room is available for the given dates
            db.execute('''SELECT * FROM bookings WHERE room_id = ? and booked_from >= ?''',
                            [int(room_id), today])

            try_new_dates = False

            for booking_row in db.get_cursor:
                booked_from = date.fromisoformat(booking_row['booked_from'])
                booked_until = date.fromisoformat(booking_row['booked_until'])

                if booked_from <= check_in_date < booked_until or booked_from < check_out_date <= booked_until:
                    try_new_dates = True
                    print('\n Sorry, this room is not available during the requested days. Please try other dates.')

            if try_new_dates:
                continue

            number_of_days = (check_out_date - check_in_date).days

            for room in rooms:
                if room['id'] == room_id:
                    room_price = room['price']

            total_price = round(number_of_days * room_price, 2)

            print('\n Your estimated total price for your stay is: $' + str(total_price))
            user_input = input(' Do you wish to proceed with this booking[Y/N]: ')

            if user_input != 'Y':
                continue

            db.execute('''INSERT INTO bookings (hotel_id, room_id, booked_from, booked_until, total_price, 
            customer_name, booking_type) VALUES (?, ?, ?, ?, ?, ?, 'NORMAL'); ''', [self.id, room_id, check_in_date,
                                                                                    check_out_date, float(total_price),
                                                                                    customer_name])
            db.get_connection.commit()

            booking_confirmation_number = db.get_cursor.lastrowid

            print('\n Hurray! Your room is booked !!!')
            print(' Below are the details of your booking: ')
            print(' ====================================== ')
            print(' BOOKING CONFIRMATION NUMBER: ' + str(booking_confirmation_number))
            print(' GUEST_NAME: ' + customer_name)
            print(' HOTEL NAME: ' + self.name)
            print(' HOTEL LOCATION: ' + self.location)
            print(' ROOM ID: ' + str(room_id))
            print(' CHECK-IN DATE: ' + str(check_in_date))
            print(' CHECK-OUT DATE: ' + str(check_out_date))
            print(' TOTAL_PRICE: $' + str(total_price))
            print(' ====================================== ')

            return

    def show_rooms(self):
        header = vars(self.rooms[0]).keys()
        rows = [vars(room).values() for room in self.rooms]
        print(tabulate(rows, header, tablefmt='grid'))

    def add_review(self, db):
        customer_name = input('Please enter your name: ')
        rating = input('Please enter your rating (1-10): ')
        comment = input('Please write a brief review about this hotel: ')

        db.execute('''INSERT INTO reviews (customer_name, comment, rating, hotel_id) VALUES (?, ?, ?, ?); ''',
                   [customer_name, comment, rating, self.id])
        db.get_connection.commit()

        self.reviews.append({
            'customer_name': customer_name,
            'comment': comment,
            'rating': rating
        })

        print('Thank you for submitting your review!')

    def show_reviews(self):
        if len(self.reviews) == 0:
            print('\n No Reviews yet for this hotel. Please submit yours.')
            return

        header = self.reviews[0].keys()
        rows = [review.values() for review in self.reviews]
        print(tabulate(rows, header, tablefmt='grid'))
        return
