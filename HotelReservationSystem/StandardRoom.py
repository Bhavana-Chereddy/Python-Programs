from Room import Room


class StandardRoom(Room):
    def __init__(self, room_details):
        super().__init__(room_details)

        self.type = 'STANDARD'
        self.amenities = ['Air Conditioning', 'Twin Bed']
