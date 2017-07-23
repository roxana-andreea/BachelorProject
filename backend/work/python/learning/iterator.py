#!/usr/local/bin/python3

class OddEven:
    def __init__(self, data):
        self._data = data
        self.indexes = (list(range(0,len(data), 2)) + list(range(1,len(data),2)))

    def __iter__(self):
        return self

    def __next__(self):
        if self.indexes:
            return self._data[self.indexes.pop(0)]
        raise StopIteration

oddeven = OddEven('ThisIsCool!')
print(''.join(c for c in oddeven))

oddeven = OddEven('HoLa')
it = iter(oddeven)
print(next(it))
print(next(it))
print(next(it))
print(next(it))

