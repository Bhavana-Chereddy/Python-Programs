from Room import Room


class DeluxeRoom(Room):
    def __init__(self, room_details):
        super().__init__(room_details)

        self.type = 'DELUXE'
        self.amenities = ['Air Conditioning', 'Queen Bed', 'Tv']
        