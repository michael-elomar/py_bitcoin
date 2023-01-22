class Point:
    def __init__(self, x, y, a, b, _tol=1e-12):
        self.x = x
        self.y = y
        self.a = a
        self.b = b
        if self.x is None and self.y is None:
            return
        if self.y**2 - (self.x**3 + self.a*self.x + self.b) > _tol:
            error_msg = f'Point ({self.x},{self.y}) is not on the elliptic curve'
            error_msg = f'{error_msg} defined by y^2 = x^3 + a*x + b'
            raise ValueError(error_msg)

    def _is_on_curve(self, a, b, _tol=1e-12):
        return self.y**2 - (self.x**3 + a*self.x + b) <= _tol

    def __repr__(self):
        return f"Point_[{self.a.num},{self.b.num}]({self.x}, {self.y})"

    def _same_curve(self, other):
        return self.a == other.a and self.b == other.b

    def __eq__(self, other):
        assert type(other) == Point
        return self.a == other.a and self.b == other.b \
            and self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self.__eq__(other)

    def __add__(self, other):
        if type(other) is not self.__class__:
            raise TypeError(f"{other} is of type : {type(other)} and  not {self.__class__}")
        if not self._same_curve(other):
            raise TypeError(f"Points {self}, {other} are not on the same curve")
        if self.x is None:
            return other
        if other.x is None:
            return self

        if self.x == other.x and self.y != other.y:
            return self.__class__(None, None, self.a, self.b)
        if self.x != other.x:
            s = (other.y - self.y) / (other.x - self.x)
            x3 = s**2 - self.x - other.x
            y3 = s*(self.x - x3) - self.y
            return self.__class__(x3, y3, self.a, self.b)
        if self.x == other.x and self.y == other.y:
            s = (3*self.x**2 + self.a) / (2*self.y)
            x3 = s**2 - 2*self.x
            y3 = s*(self.x - x3) - self.y
            return self.__class__(x3, y3, self.a, self.b)
        if self == other and self.y == 0:
            return self.__class__(None, None, self.a, self.b)
