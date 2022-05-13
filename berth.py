class Berth:
    """
    A class that stores information on the berths.
    
    All information must be static.
    """
    
    __new_id = 0
    
    def __init__(self, opening_time: int, closing_time: int):
        self.opening_time = opening_time
        self.closing_time = closing_time
        self.id = Berth.__new_id
        Berth.__new_id += 1

    def __str__(self):
        return f"Berth. id: {self.id}, open: {self.opening_time}, close: {self.closing_time}"