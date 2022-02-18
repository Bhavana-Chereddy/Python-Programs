class Room:
    """Room class to describe a Room & its functionalities"""

    def __init__(self, room_details):
        self.id = room_details['id']
        self.price = room_details['price']
        self.description = room_details['description']
        self.hotel_id = room_details['hotel_id']


