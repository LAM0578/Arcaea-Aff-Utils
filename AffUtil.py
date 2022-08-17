from StringParser import*

class AffUtil:
    def GetEventStartTiming(context:str,eventhead:str):
        context = context.strip()
        s = StringParser(context)
        s.Skip(eventhead)
        value = s.ReadInt(",")
        return value

    def GetArcPosition(context:str):
        context = context.strip()
        s = StringParser(context)
        s.Skip(4)
        s.ReadInt(",")
        s.ReadInt(",")
        startx = s.ReadFloat(",")
        endx = s.ReadFloat(",")
        s.ReadString(",")
        starty = s.ReadFloat(",")
        endy = s.ReadFloat(",")
        return "{0},{1},{2},{3}".format(startx,endx,starty,endy)