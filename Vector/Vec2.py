
class Vec2:
    def __init__(self,x:float=None,y:float=None):
        if (x != None and y != None) or \
           (x == None and y == None):
            self.x = x if x != None else 0
            self.y = y if y != None else 0
        else:
            exmsg = 'Field'
            if x == None:
                exmsg += ' x,'
            if y == None:
                exmsg += ' y,'
            exmsg = exmsg.rstrip(',')
            exmsg += ' is Empty'
            raise Exception(exmsg)

    x = 0
    y = 0

    def __add__(self,value):
        x = self.x + value.x
        y = self.y + value.y
        return Vec2(x,y)
    
    def __sub__(self,value):
        x = self.x - value.x
        y = self.y - value.y
        return Vec2(x,y)

    def __mul__(self,value):
        vx = value
        if type(value) == Vec2:
            vx = value.x
        vy = value
        if type(value) == Vec2:
            vy = value.y
        x = self.x * vx
        y = self.y * vy
        return Vec2(x,y)

    def __truediv__(self,value):
        vx = value
        if type(value) == Vec2:
            vx = value.x
        vy = value
        if type(value) == Vec2:
            vy = value.y
        x = self.x / vx
        y = self.y / vy
        return Vec2(x,y)

    def __str__(self) -> str:
        return f'({self.x}, {self.y})'

    def ToVec3(self):
        import Vector.Vec3 as Vector
        return Vector.Vec3(self.x,self.y,0)
