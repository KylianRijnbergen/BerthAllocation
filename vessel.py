class Vessel:
    """
    A class that stores information on the vessels.
    
    All information must be static.
    """
    
    __new_id = 0
    
    def __init__(self, arrival_time: int, handling_time: list, closing_time: int, cost_unit_time: float):
        self.arrival_time = arrival_time
        self.handling_time = handling_time
        self.closing_time = closing_time
        self.cost_unit_time = cost_unit_time
        self.id = Vessel.__new_id % 60
        Vessel.__new_id += 1
        self.time_window = self.closing_time - self.arrival_time
        
    def get_time_window(self):
        return self.closing_time - self.arrival_time

    def __str__(self):
        return f"Vessel: id: {self.id}, arrival: {self.arrival_time}, closing: {self.closing_time}. Handling: {self.handling_time}"
    
    def __repr__(self):
        return f"Vessel({self.arrival_time}, {self.handling_time}, {self.closing_time}, {self.cost_unit_time})"
    
    def __hash__(self):
        return 31 * hash(self.arrival_time) + 31 * hash(str(self.handling_time)) + 31 * hash(self.closing_time) + 31 * hash(self.cost_unit_time) + 31 * hash(self.time_window)    
    
if __name__ == "__main__":
    inst1 = Vessel(8, [10, 13], 15, 20.5)
    print(repr(inst1))
    inst2 = eval(repr(inst1))
    
    print(inst2)
    
    print(inst1 == inst2)
    print(hash(inst1) == hash(inst2))
    print(hash(inst1))
