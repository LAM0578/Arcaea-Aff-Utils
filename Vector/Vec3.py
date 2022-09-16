class Vec3:
    def __init__(self,x:float=None,y:float=None,z:float=None):
        if (x != None and y != None and z != None) or \
           (x == None and y == None and z == None):
            self.x = x if x != None else 0
            self.y = y if y != None else 0
            self.z = z if z != None else 0
        else:
            exmsg = 'Field'
            if x == None:
                exmsg += ' x,'
            if y == None:
                exmsg += ' y,'
            if z == None:
                exmsg += ' z,'
            exmsg = exmsg.rstrip(',')
            exmsg += ' is Empty'
            raise Exception(exmsg)

    x = 0
    y = 0
    z = 0

    def __add__(self,value):
        x = self.x + value.x
        y = self.y + value.y
        z = self.z + value.z
        return Vec3(x,y,z)
    
    def __sub__(self,value):
        x = self.x - value.x
        y = self.y - value.y
        z = self.z - value.z
        return Vec3(x,y,z)

    def __mul__(self,value):
        vx = value
        if type(value) == Vec3:
            vx = value.x
        vy = value
        if type(value) == Vec3:
            vy = value.y
        vz = value
        if type(value) == Vec3:
            vz = value.z
        x = self.x * vx
        y = self.y * vy
        z = self.z * vz
        return Vec3(x,y,z)

    def __truediv__(self,value):
        vx = value
        if type(value) == Vec3:
            vx = value.x
        vy = value
        if type(value) == Vec3:
            vy = value.y
        vz = value
        if type(value) == Vec3:
            vz = value.z
        x = self.x / vx if vx != 0 else 0
        y = self.y / vy if vy != 0 else 0
        z = self.z / vz if vz != 0 else 0
        return Vec3(x,y,z)

    def __str__(self) -> str:
        return f'({self.x}, {self.y}, {self.z})'
