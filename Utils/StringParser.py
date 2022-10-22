
class StringParser:
    def __init__(self, str:str):
        self.base = str
        self.pos = 0
    base = ""
    pos = 0

    # bool ? x : y convert to python:
    # x if bool else y

    # str.substring(start, length) convert to python:
    # str[start:start+length]

    def Skip(self, length):
        if type(length) == int:
            self.pos += length
        elif type(length) == str:
            self.pos += len(length)

    def ReadFloat(self, ternimator = None):
        end = self.base.find(ternimator, self.pos) if ternimator != None else (int(len(self.base)) - 1)
        value = float(self.base[self.pos:end])
        self.pos += (end - self.pos + 1)
        return value
        
    def ReadInt(self, ternimator = None):
        end = self.base.find(ternimator, self.pos) if ternimator != None else (int(len(self.base)) - 1)
        value = int(self.base[self.pos:end])
        self.pos += (end - self.pos + 1)
        return value

    def ReadBool(self, ternimator = None):
        end = self.base.find(ternimator, self.pos) if ternimator != None else (int(len(self.base)) - 1)
        value = self.base[self.pos:end].lower() == "true"
        self.pos += (end - self.pos + 1)
        return value

    def ReadString(self, ternimator = None):
        end = self.base.find(ternimator, self.pos) if ternimator != None else (int(len(self.base)) - 1)
        value = self.base[self.pos:end]
        self.pos += (end - self.pos + 1)
        return value

    def Current(self):
        return self.base[self.pos]

    def Peek(self, length = 1):
        return self.base[self.pos:self.pos + length]

    def TryReadFloat(self, ternimator = None):
        try:
            return self.ReadFloat(ternimator)
        except:
            return 0

    def TryReadInt(self, ternimator = None):
        try:
            return self.ReadInt(ternimator)
        except:
            return 0

    def CanReadFloat(self, ternimator = None):
        originPos = pos
        try:
            self.ReadFloat(ternimator)
            pos = originPos
            return True
        except:
            pos = originPos
            return False

    def CanReadInt(self, ternimator = None):
        originPos = pos
        try:
            self.ReadInt(ternimator)
            pos = originPos
            return True
        except:
            pos = originPos
            return False
