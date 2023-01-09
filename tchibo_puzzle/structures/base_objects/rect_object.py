class RectObject:
    def __init__(self, pos, size):
        self.__pos = pos
        self.__size = size

    @property
    def pos(self):
        return self.__pos

    @pos.setter
    def pos(self, value):
        self.__pos = value

    @property
    def x(self):
        return self.__pos[0]

    @x.setter
    def x(self, value):
        self.__pos = (value, self.y)

    @property
    def y(self):
        return self.__pos[1]

    @y.setter
    def y(self, value):
        self.__pos = (self.x, value)

    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self, value):
        self.__size = value

    @property
    def width(self):
        return self.__size[0]

    @width.setter
    def width(self, value):
        self.__size = (value, self.height)

    @property
    def height(self):
        return self.__size[1]

    @height.setter
    def height(self, value):
        self.__size = (self.width, value)

    def check_collision(self, pos) -> bool:
        x, y = pos
        return (
                self.x <= x <= self.x + self.width
                and self.y <= y <= self.y + self.height
        )
