from Room import Room


class SuiteRoom(Room):
    def __init__(self, room_details):
        super().__init__(room_details)

        self.type = 'SUITE'
        self.amenities = ['Air Conditioning', 'King Bed', 'Tv', 'Refrigerator', 'Drawing Room']