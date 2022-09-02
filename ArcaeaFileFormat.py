# This file is used for parse Arcaea chart file
from StringParser import StringParser

# Base

class TimingEvent:
    Timing = int(0)
    Bpm = float(0)
    Beats = float(0)

# Notes

class TapNote:
    Timing = int(0)
    Track = int(0)

class HoldNote:
    Timing = int(0)
    EndTiming = int(0)
    Track = int(0)

class ArcNote:
    Timing = int(0)
    EndTiming = int(0)
    StartX = float(0)
    EndX = float(0)
    LineType = ""
    StartY = float(0)
    EndY = float(0)
    Color = int(0)
    FxName = ""
    IsTrace = False
    ArcTaps = []

class FlickNote:
    Timing = int(0)
    # The pos of this flick
    PosX = float(0)
    PosY = float(0)
    # The final pos of this flick, used for calc dgree
    VecX = float(0)
    VecY = float(0)

# Effects

class CameraEvent:
    Timing = int(0)
    # The moved pos of this camera
    PosX = float(0)
    PosY = float(0)
    PosZ = float(0)
    # The rotated dgrees of this camera
    RotX = float(0)
    RotY = float(0)
    RotZ = float(0)
    # Other
    CameraType = ""
    Dutation = int(0)

# Not support Arcade-Zero / Arcade-One custom scenecontrol
class SceneControl:
    Timing = int(0)
    SceneControlType = ""
    ParamFloat = float(0)
    ParamInt = int(0)

# Chart

class EventGroup:
    def __init__(self,id:int):
        self.TimingGroupID = id
    TimingGroupID = 0
    TimingGroupAttributes = []

    # Events
    Timings = []
    Taps = []
    Holds = []
    Arcs = []
    Flicks = []
    Cameras = []
    SceneControls = []

    def ParseAttributes(self,str:str):
        str = str.strip()
        attributes = str.replace("timinggroup(","").replace("){","").split("_")
        self.TimingGroupAttributes = attributes

class Chart:
    def __init__(self,filePath:str):
        self.Parse(filePath)

    # Every events group will append to here
    EventGroups = []

    # Parse chart from file
    def Parse(self,filePath:str):
        eventGroups = []
        totalID = 0
        currID = 0 # Current Timing Group ID
        with open(filePath, 'r') as file:
            lines = file.readlines()
            i = 0
            currGroup = EventGroup(0)
            eventGroups.append(currGroup)
            while i < len(lines):
                line = lines[i].strip()
                # Case types and parse
                if line.startswith("timinggroup("):
                    totalID += 1
                    currID = totalID
                    currGroup = EventGroup(totalID)
                    currGroup.ParseAttributes(line)
                    eventGroups.append(currGroup)
                if line.startswith("};"):
                    currID = 0
                group:EventGroup = eventGroups[currID]
                if line.startswith("timing("):
                    group.Timings.append(self.ParseTiming(line))
                elif line.startswith("("):
                    group.Taps.append(self.ParseTap(line))
                elif line.startswith("hold("):
                    group.Holds.append(self.ParseHold(line))
                elif line.startswith("arc("):
                    group.Arcs.append(self.ParseArc(line))
                elif line.startswith("flick("):
                    group.Flicks.append(self.ParseFlick(line))
                elif line.startswith("camera("):
                    group.Cameras.append(self.ParseCamera(line))
                elif line.startswith("scenecontrol("):
                    group.SceneControls.append(self.ParseSceneControl(line))
                i += 1
            self.EventGroups = eventGroups

    def ParseTiming(self,line:str):
        line = line.strip()
        n = TimingEvent()
        s = StringParser(line)
        s.Skip(7) # The skip value is event start symbol (eg: "<timing(>100,1000.00,4.00);")
        n.Timing = s.ReadInt(",")
        n.Bpm = s.ReadFloat(",")
        n.Beats = s.ReadFloat(")")
        return n

    def ParseTap(self,line:str):
        line = line.strip()
        n = TapNote()
        s = StringParser(line)
        s.Skip(1)
        n.Timing = s.ReadInt(",")
        n.Track = s.ReadInt(")")
        return n

    def ParseHold(self,line:str):
        line = line.strip()
        n = HoldNote()
        s = StringParser(line)
        s.Skip(5)
        n.Timing = s.ReadInt(",")
        n.EndTiming = s.ReadInt(",")
        n.Track = s.ReadInt(")")
        return n

    def ParseArc(self,line:str):
        line = line.strip()
        n = ArcNote()
        s = StringParser(line)
        s.Skip(4)
        n.Timing = s.ReadInt(",")
        n.EndTiming = s.ReadInt(",")
        n.StartX = s.ReadFloat(",")
        n.EndX = s.ReadFloat(",")
        n.LineType = s.ReadString(",")
        n.StartY = s.ReadFloat(",")
        n.EndY = s.ReadFloat(",")
        n.Color = s.ReadInt(",")
        n.FxName = s.ReadString(",")
        n.IsTrace = s.ReadBool(")")
        arctaps = []
        if s.Current() != ";":
            n.IsTrace = True
            while True:
                s.Skip(8)
                arctaps.append(s.ReadInt(")"))
                if s.Current() != ",":
                    break
        n.ArcTaps = arctaps
        return n

    def ParseFlick(self,line:str):
        line = line.strip()
        n = FlickNote()
        s = StringParser(line)
        s.Skip(6)
        n.Timing = s.ReadInt(",")
        n.PosX = s.ReadFloat(",")
        n.PosY = s.ReadFloat(",")
        n.VecX = s.ReadFloat(",")
        n.VecY = s.ReadFloat(")")
        return n

    def ParseCamera(self,line:str):
        line = line.strip()
        n = CameraEvent()
        s = StringParser(line)
        s.Skip(7)
        n.Timing = s.ReadInt(",")
        # Position
        n.PosX = s.ReadFloat(",")
        n.PosY = s.ReadFloat(",")
        n.PosZ = s.ReadFloat(",")
        # Rotation
        n.RotX = s.ReadFloat(",")
        n.RotY = s.ReadFloat(",")
        n.RotZ = s.ReadFloat(",")
        # Other
        n.CameraType = s.ReadString(",")
        n.Dutation = s.ReadInt(")")
        return n

    def ParseSceneControl(self,line:str):
        line = line.strip()
        n = SceneControl()
        s = StringParser(line)
        s.Skip(13)
        n.Timing = s.ReadInt(",")
        n.SceneControlType = s.ReadString(",")
        if n.SceneControlType != "trackhide" or n.SceneControlType != "trackshow":
            n.ParamFloat = s.ReadFloat(",")
            n.ParamInt = s.ReadInt(")")
        return n


