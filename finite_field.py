class FieldElement(object):
    def __init__(self, num, prime):
        if num >= prime or num < 0:
            error_msg = f"Num {num} is not in field range 0 to {prime - 1}"
            raise ValueError(error_msg)
        self.num = num
        self.prime = prime

    def __repr__(self):
        return f'FieldElement_{self.prime}({self.num})'

    def __eq__(self, other):
        if other is None:
            return False
        return self.num == other.num and self.prime == other.prime

    def __ne__(self, other):
        return not self.__eq__(other)

    def __add__(self, other):
        if other is None:
            raise ValueError('Cannot add FieldElement and None')
        if other.prime != self.prime:
            raise ValueError('Cannot add field elements with different primes')
        return self.__class__((self.num + other.num) % self.prime, self.prime)

    def __sub__(self, other):
        if other is None:
            raise ValueError('Cannot subtract FieldElement and None')
        if other.prime != self.prime:
            raise ValueError('Cannot subtract field elements with different primes')
        return self.__class__((self.num - other.num) % self.prime, self.prime)

    def __mul__(self, other):
        if other is None:
            raise ValueError("Cannot multiply FieldElement and None")
        if other.prime != self.prime:
            raise ValueError('Cannot multiply field elements with different primes')
        return self.__class__((self.num * other.num) % self.prime, self.prime)

    def __pow__(self, power, modulo=None):
        if type(power) is not int and type(power) is not float:
            print(type(power))
            raise ValueError(f"power {power} must be a numerical value")
        if power < 0:
            power = power % (self.prime - 1)
        return self.__class__(pow(self.num, power, self.prime), self.prime)

    def __truediv__(self, other):
        if other is None:
            raise ValueError("Cannot divide by a None")
        if other.prime != self.prime:
            raise ValueError('Cannot divide field elements with different primes')
        other = other ** (other.prime - 2)
        return self * other

    def __lt__(self, other):
        if type(other) is float or type(other) is int:
            if other >= self.prime or other < 0:
                raise ValueError('other does not belong to the Field')
            return self.num < other
        elif type(other) is FieldElement:
            if self.prime != other.prime:
                raise ValueError("Cannot compare two elements of different finite field")
            return self.num < other.num
        else:
            raise TypeError("Cannot compare non numerical types")

    def __gt__(self, other):
        if type(other) is float or type(other) is int:
            if other >= self.prime or other < 0:
                raise ValueError('other does not belong to the Field')
            return self.num > other
        elif type(other) is FieldElement:
            if self.prime != other.prime:
                raise ValueError("Cannot compare two elements of different finite field")
            return self.num > other.num
        else:
            raise TypeError("Cannot compare non numerical types")

    def __ge__(self, other):
        if type(other) is float or type(other) is int:
            if other >= self.prime or other < 0:
                raise ValueError('other does not belong to the Field')
            return self.num >= other
        elif type(other) is FieldElement:
            if self.prime != other.prime:
                raise ValueError("Cannot compare two elements of different finite field")
            return self.num >= other.num
        else:
            raise TypeError("Cannot compare non numerical types")

    def __le__(self, other):
        if type(other) is float or type(other) is int:
            if other >= self.prime or other < 0:
                raise ValueError('other does not belong to the Field')
            return self.num <= other
        elif type(other) is FieldElement:
            if self.prime != other.prime:
                raise ValueError("Cannot compare two elements of different finite field")
            return self.num <= other.num
        else:
            raise TypeError("Cannot compare non numerical types")