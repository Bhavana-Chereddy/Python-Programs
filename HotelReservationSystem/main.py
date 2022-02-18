from HotelReservationSystem import HotelReservationSystem


def main():
    hotel_reservation_system = HotelReservationSystem()

    while True:
        print('\nSelect your menu: ')
        print('[1] Menu')
        print('[2] Exit')

        user_input = int(input('\n Please choose your option: '))

        if 2 < user_input < 1:
            print('\n Invalid input. Please try again.')
            continue

        match user_input:
            case 1:
                hotel_reservation_system.user_menu()
            case 2:
                print('\n Exiting program...')
                return


main()

# Thoughts =>

# Database
# hotels - id, # of rooms, location, star rating (3 hotels)
# rooms - id, type, price (10 rooms [different categories] per hotel), description
# bookings - id, hotel id, room id, from, to, total price, user name, type (regular/block)
# reviews - id, user, comment, rating

# Menu - Customer, Admin
# 1. Please select a hotel to book from
# 1.1 Please select a room to check availability:
# 1.1.1 Please enter from and to dates to check availability (cannot select dates before today)
# 1.1.2. The room xx is available. And the total cost would be xxx. Would you like to proceed with booking? [Y/N]

# 1.2. Provide Review for a hotel
# 1.2.1 Choose the hotel id that you would want to review
# 1.2.1.1 Provide your name
# 1.2.1.2 Input a number between 1 to 5
# 1.2.1.3 Write some details about the hotel
# 1.3. Check Reviews for a hotel
# 1.3.1 Choose the hotel id that you would like to check review for
# 2. exit

# Object Design
# - Hotel has rooms (Hotel Class, Room Class) - hotel can add rooms, remove rooms, block rooms for certain dates
# - Room can be of multiple types - Regular, Deluxe- Queen, Suite (Inheritance) - room can have amenities, description
# - Main - main menu, bookings etc.
