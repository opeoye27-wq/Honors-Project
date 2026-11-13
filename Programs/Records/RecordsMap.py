# See assignment for class attributes.
# Remember to include docstrings.
# Start with unittests

class LocalRecord:
    def __init__(self, pos, max=None, min=None, precision = 0): 
        """initialize the position and temps"""
        self.precision = precision
        self.pos = (round(pos[0], self.precision), round(pos[1], self.precision)) #tuple representing location --> key
        self.max = max #value that key maps to
        self.min = min #value that key maps to

    def add_report(self, temp):
        """adding a report/ updating min or max if necessary"""
        if self.max is None or temp > self.max:
            self.max = temp
        if self.min is None or temp < self.min:
            self.min = temp

    def __eq__(self, other): 
        """checks if other is equal to self"""
        return isinstance(other, LocalRecord) and self.pos == other.pos

    def __hash__(self): 
        """returns the hash of the position"""
        return hash(self.pos)
        

    def __repr__(self):
        """return information about the record"""
        return f"Record(pos={self.pos}, max={self.max}, min={self.min})"

class RecordsMap:
    """stores all of the local record info"""
    def __init__(self, capacity = 8): 
        """initialize the table"""
        self.capacity = capacity
        self.table = [[] for _ in range(capacity)]
        self.size = 0 #number of items in table
        self.cap = 0.7

    def _hash(self, pos):
        """return a hash for the rounded position"""
        rounded_pos = (round(pos[0]), round(pos[1]))
        return hash(rounded_pos) % self.capacity

    def __len__(self): 
        """returns the number of elements in the hash table"""
        return self.size

    def add_report(self, pos, temp): 
        """adding a report/ updating the report if the position is already there"""
        index = self._hash(pos)
        rounded_pos = (round(pos[0]), round(pos[1]))

        for record in self.table[index]:
            if record.pos == rounded_pos:
                #overwriting
                record.add_report(temp)
                return
        self.table[index].append(LocalRecord(pos, temp, temp))
        self.size += 1

        if self.size / self.capacity > 0.7:
            self._rehash(self.capacity * 2)

    def __getitem__(self, pos): 
        """returning the temperature at position pos"""
        index = self._hash(pos)
        rounded_pos = (round(pos[0]), round(pos[1]))
        for i, record in enumerate(self.table[index]):
            if record.pos == rounded_pos:
                return record.min, record.max
        raise KeyError("This position does not exist")

  
    def __contains__(self, pos):
        """checking if the table contains given pos""" 
        index = self._hash(pos)
        rounded_pos = (round(pos[0]), round(pos[1]))
        for record in self.table[index]:
            if record.pos == rounded_pos:
                return True
        return False

    def _rehash(self, m_new): 
        """rehashing the table"""
        self.capacity = m_new
        old_table = self.table
        self.table = [[] for _ in range(self.capacity)]
        self.size = 0

        for bucket in old_table:
            for record in bucket:
                self.add_report(record.pos, record.min)
                if record.max != record.min:
                    self.add_report(record.pos, record.max)
        