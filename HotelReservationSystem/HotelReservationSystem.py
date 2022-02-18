from db import DB
from copy import deepcopy
from tabulate import tabulate

from Hotel import Hotel


class HotelReservationSystem:
    def __init__(self):
        self.db = DB('hotel_reservation_system.sqlite')
        self.reset_database()
        self.db.execute('''SELECT * FROM hotels''')

        # get all hotels, for each hotel, get all rooms & initiate a hotel object
        self.hotels = []

        for hotel_row in self.db.get_cursor:
            hotel_details = {
                'id': hotel_row['id'],
                'name': hotel_row['name'],
                'location': hotel_row['location'],
                'star_rating': hotel_row['star_rating'],
                'rooms': [],
                'reviews': []
            }

            self.hotels.append(hotel_details)

        for hotel in self.hotels:
            rooms = []
            reviews = []

            self.db.execute('''SELECT * FROM rooms WHERE hotel_id =  ?''', [hotel['id']])

            for room_row in self.db.get_cursor:
                room_details = {
                    'id': room_row['id'],
                    'type': room_row['type'],
                    'price': room_row['price'],
                    'description': room_row['description'],
                    'hotel_id': room_row['hotel_id']
                }

                rooms.append(room_details)

            self.db.execute('''SELECT * FROM reviews WHERE hotel_id =  ?''', [hotel['id']])

            for review_row in self.db.get_cursor:
                review_details = {
                    'customer_name': review_row['customer_name'],
                    'comment': review_row['comment'],
                    'rating': review_row['rating']
                }

                reviews.append(review_details)

            hotel['rooms'] = rooms
            hotel['reviews'] = reviews
            hotel['obj'] = Hotel(hotel)

    def __del__(self):
        self.db.close_db()

    def reset_database(self):
        # create all necessary tables
        # insert hotel data
        # insert a few rooms for initial
        # commit transaction

        sql = """
                    DROP TABLE IF EXISTS hotels;
                    DROP TABLE IF EXISTS rooms;
                    DROP TABLE IF EXISTS reviews;
                    DROP TABLE IF EXISTS bookings;

                    CREATE TABLE hotels
                    (
                        id integer constraint hotels_pk primary key autoincrement unique,
                        name varchar(255),
                        location varchar(255),
                        star_rating varchar(255)
                    );

                    CREATE TABLE rooms
                    (
                        id integer constraint rooms_pk primary key autoincrement unique,
                        type varchar(255) default 'STANDARD',
                        price decimal,
                        hotel_id int constraint hotel_id references hotels,
                        description varchar(255)
                    );

                    CREATE TABLE reviews
                    (
                        id integer constraint reviews_pk primary key autoincrement unique,
                        customer_name varchar(255),
                        comment varchar,
                        rating int,
                        hotel_id int constraint hotel_id references hotels
                    );

                    CREATE TABLE bookings
                    (
                        id integer constraint bookings_pk primary key autoincrement unique,
                        hotel_id int constraint hotel_id references hotels,
                        room_id int references rooms,
                        booked_from date,
                        booked_until date,
                        total_price decimal,
                        customer_name varchar(255),
                        booking_type varchar(255) default 'NORMAL'
                    );

                    INSERT INTO hotels (name, location, star_rating)
                    VALUES ('Marriott', 'Salt Lake City', '3-star');
                    INSERT INTO hotels (name, location, star_rating)
                    VALUES ('Hampton Inn', 'Park City', '5-star');
                    INSERT INTO hotels (name, location, star_rating)
                    VALUES ('Grand America', 'Salt Lake City', '7-star');

                    INSERT INTO rooms (type, price, hotel_id, description)
                    VALUES ('STANDARD', 49.99, 1, 'Facing Street');
                    INSERT INTO rooms (type, price, hotel_id, description)
                    VALUES ('STANDARD', 49.99, 1, 'Facing Street');
                    INSERT INTO rooms (type, price, hotel_id, description)
                    VALUES ('DELUXE', 79.99, 1, 'Facing Mountains');

                    INSERT INTO rooms (type, price, hotel_id, description)
                    VALUES ('STANDARD', 79.99, 2, 'Near Jacuzzi');
                    INSERT INTO rooms (type, price, hotel_id, description)
                    VALUES ('DELUXE', 99.99, 2, 'Near Pool');
                    INSERT INTO rooms (type, price, hotel_id, description)
                    VALUES ('DELUXE', 109.99, 2, 'Facing Mountains, Near Pool');

                    INSERT INTO rooms (type, price, hotel_id, description)
                    VALUES ('DELUXE', 79.99, 3, 'Near Gym');
                    INSERT INTO rooms (type, price, hotel_id, description)
                    VALUES ('DELUXE', 99.99, 3, 'Near Gym');
                    INSERT INTO rooms (type, price, hotel_id, description)
                    VALUES ('SUITE', 509.99, 3, 'Top Floor, Facing Mountains, Near Pool');
                    
                    INSERT INTO bookings (hotel_id, room_id, booked_from, booked_until, total_price, 
                    customer_name, booking_type) VALUES (3, 9, '2021-11-21', '2021-11-24', 1530.00, 'John', 'NORMAL');
                    INSERT INTO bookings (hotel_id, room_id, booked_from, booked_until, total_price, 
                    customer_name, booking_type) VALUES (3, 9, '2021-11-26', '2021-11-28', 1530.00, 'Bhav', 'NORMAL');
                    INSERT INTO bookings (hotel_id, room_id, booked_from, booked_until, total_price, 
                    customer_name, booking_type) VALUES (3, 8, '2021-11-21', '2021-11-23', 200.00, 'Yash', 'NORMAL');
                    INSERT INTO bookings (hotel_id, room_id, booked_from, booked_until, total_price, 
                    customer_name, booking_type) VALUES (2, 6, '2021-11-21', '2021-11-23', 220.00, 'Hannah', 'NORMAL');
                    INSERT INTO bookings (hotel_id, room_id, booked_from, booked_until, total_price, 
                    customer_name, booking_type) VALUES (2, 5, '2021-11-21', '2021-11-23', 200.00, 'Kaleb', 'NORMAL');
                    INSERT INTO bookings (hotel_id, room_id, booked_from, booked_until, total_price, 
                    customer_name, booking_type) VALUES (2, 5, '2021-11-21', '2021-11-23', 200.00, 'George', 'NORMAL');
                    INSERT INTO bookings (hotel_id, room_id, booked_from, booked_until, total_price, 
                    customer_name, booking_type) VALUES (1, 3, '2021-11-17', '2021-11-24', 560.00, 'Ben', 'NORMAL');
                    INSERT INTO bookings (hotel_id, room_id, booked_from, booked_until, total_price, 
                    customer_name, booking_type) VALUES (1, 3, '2021-12-01', '2021-12-07', 0.00, 'Self', 'BLOCK');
                    INSERT INTO bookings (hotel_id, room_id, booked_from, booked_until, total_price, 
                    customer_name, booking_type) VALUES (1, 1, '2021-12-07', '2021-12-09', 100.00, 'Doug', 'NORMAL');
                    
                    
                    INSERT INTO reviews (customer_name, comment, rating, hotel_id) VALUES ('Ben', 'Great Place', 7, 3);
                    INSERT INTO reviews (customer_name, comment, rating, hotel_id) VALUES ('Den', 'Bad Place', 2, 3);
                    INSERT INTO reviews (customer_name, comment, rating, hotel_id) VALUES ('Don', 'Good Stay', 9, 2);
                    INSERT INTO reviews (customer_name, comment, rating, hotel_id) VALUES ('Harsh', 'Nice Place', 10, 1);
                    INSERT INTO reviews (customer_name, comment, rating, hotel_id) VALUES ('Bhavana', 'Great Place', 7, 1);
                    INSERT INTO reviews (customer_name, comment, rating, hotel_id) VALUES ('Sam', 'Average place to stay', 5, 2);
                """

        self.db.execute_script(sql)
        self.db.get_connection.commit()

    def print_all_hotels(self):
        hotels = deepcopy(self.hotels)

        for hotel in hotels:
            del hotel['rooms']
            del hotel['reviews']
            del hotel['obj']

        header = hotels[0].keys()
        rows = [hotel.values() for hotel in hotels]

        print('\n')
        print(tabulate(rows, header, tablefmt='grid'))
        print('\n')

    def user_menu(self):
        while True:
            print('\n[1] Select a hotel to book a room, leave a review or read reviews')
            print('[2] Exit')

            user_input = int(input('\n Please choose your option: '))

            if 2 < user_input < 1:
                print('\n Invalid input. Please try again.')
                continue

            match user_input:
                case 1:
                    self.print_all_hotels()

                    user_input = int(input('Select hotel. Enter hotel Id: '))

                    self.db.execute('''SELECT * FROM hotels WHERE id = ?''', [int(user_input)])
                    hotel_row = self.db.get_cursor.fetchone()

                    if hotel_row is None:
                        print('\n Invalid hotel id. Please try again.')
                        return

                    selected_hotel = None

                    for hotel in self.hotels:
                        if hotel['id'] == int(user_input):
                            selected_hotel = hotel['obj']

                    while True:
                        print('\n')
                        print('[a] Select a room to book')
                        print('[b] Read reviews about the hotel')
                        print('[c] Leave a review about the hotel')
                        print('[d] Go Back')

                        user_input = input('\nPlease choose your option: ')

                        if user_input not in ['a', 'b', 'c', 'd']:
                            print('\n Invalid input. Please try again.')
                            continue

                        match user_input:
                            case 'a':
                                selected_hotel.show_rooms()
                                selected_hotel.book_room(self.db)
                            case 'b':
                                selected_hotel.show_reviews()
                            case 'c':
                                selected_hotel.add_review(self.db)
                            case 'd':
                                break
                case 2:
                    print('\n Exiting user menu...')
                    return
