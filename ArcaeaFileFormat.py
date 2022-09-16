# This file is used for parse Arcaea chart file
from Utils.StringParser import StringParser


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
    LineType = "s"
    StartY = float(0)
    EndY = float(0)
    Color = int(0)
    FxName = "none"
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
    def __init__(self, id: int):
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

    def ParseAttributes(self, str: str):
        str = str.strip()
        attributes = str.replace(
            "timinggroup(", "").replace("){", "").split("_")
        self.TimingGroupAttributes = attributes

    def ResetEvents(self):
        self.Timings = []
        self.Taps = []
        self.Holds = []
        self.Arcs = []
        self.Flicks = []
        self.Cameras = []
        self.SceneControls = []


class Chart:
    def __init__(self, filePath: str = None):
        if filePath != None:
            self.AppendLines.clear()
            self.EventGroups.clear()
            self.Parse(filePath)

    AppendLines = []  # Before "-"
    EventGroups = []  # Every events group will append to here

    # Parse chart from file
    def Parse(self, filePath: str):
        eventGroups = []
        totalID = 0
        currID = 0  # Current Timing Group ID
        with open(filePath, 'r') as file:
            lines = file.readlines()
            appendLines = []
            splitLine = 0
            try:
                splitLine = lines.index("-\n")
            except:
                try:
                    splitLine = lines.index("-")
                except:
                    pass
            if splitLine > 0:
                i = 0
                while i <= splitLine:
                    appendLines.append(lines[i])
                    i += 1
            i = splitLine + 1
            currGroup = EventGroup(0)
            # Must clear current notes here
            currGroup.ResetEvents()
            totalID += 1
            eventGroups.append(currGroup)
            Timings = []
            Taps = []
            Holds = []
            Arcs = []
            Flicks = []
            Cameras = []
            SceneControls = []
            while i < len(lines):
                line = lines[i].strip()
                # Case types and parse
                if line.startswith("timinggroup("):
                    # Must clear current notes here
                    Timings = []
                    Taps = []
                    Holds = []
                    Arcs = []
                    Flicks = []
                    Cameras = []
                    SceneControls = []
                    totalID += 1
                    currID = totalID - 1
                    currGroup = EventGroup(totalID)
                    # Must clear current notes here
                    currGroup.ResetEvents()
                    currGroup.ParseAttributes(line)
                    eventGroups.append(currGroup)
                if line.startswith("};"):
                    currID = 0
                group: EventGroup = eventGroups[currID]
                if currID == 0:
                    Timings = group.Timings
                    Taps = group.Taps
                    Holds = group.Holds
                    Arcs = group.Arcs
                    Flicks = group.Flicks
                    Cameras = group.Cameras
                    SceneControls = group.SceneControls

                if line.startswith("timing("):
                    Timings.append(self.ParseTiming(line))
                elif line.startswith("("):
                    Taps.append(self.ParseTap(line))
                elif line.startswith("hold("):
                    Holds.append(self.ParseHold(line))
                elif line.startswith("arc("):
                    Arcs.append(self.ParseArc(line))
                elif line.startswith("flick("):
                    Flicks.append(self.ParseFlick(line))
                elif line.startswith("camera("):
                    Cameras.append(self.ParseCamera(line))
                elif line.startswith("scenecontrol("):
                    SceneControls.append(self.ParseSceneControl(line))

                group.Timings = Timings
                group.Taps = Taps
                group.Holds = Holds
                group.Arcs = Arcs
                group.Flicks = Flicks
                group.Cameras = Cameras
                group.SceneControls = SceneControls

                eventGroups[currID] = group
                i += 1
            self.EventGroups = eventGroups
            self.AppendLines = appendLines

    def ParseTiming(self, line: str):
        line = line.strip()
        n = TimingEvent()
        s = StringParser(line)
        # The skip value is event start symbol (eg: "<timing(>100,1000.00,4.00);")
        s.Skip(7)
        n.Timing = s.ReadInt(",")
        n.Bpm = s.ReadFloat(",")
        n.Beats = s.ReadFloat(")")
        return n

    def ParseTap(self, line: str):
        line = line.strip()
        n = TapNote()
        s = StringParser(line)
        s.Skip(1)
        n.Timing = s.ReadInt(",")
        n.Track = s.ReadInt(")")
        return n

    def ParseHold(self, line: str):
        line = line.strip()
        n = HoldNote()
        s = StringParser(line)
        s.Skip(5)
        n.Timing = s.ReadInt(",")
        n.EndTiming = s.ReadInt(",")
        n.Track = s.ReadInt(")")
        return n

    def ParseArc(self, line: str):
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

    def ParseFlick(self, line: str):
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

    def ParseCamera(self, line: str):
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

    def ParseSceneControl(self, line: str):
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


class AffWriter:

    # Write Events to File
    def WriteEvents(self, writePath: str, chart: Chart):
        with open(writePath, 'w') as file:
            # Write Append lines first
            i = 0
            while i < len(chart.AppendLines):
                file.writelines(chart.AppendLines[i])
                if "\n" not in str(chart.AppendLines[i]):
                    file.writelines("\n")
                i += 1
            # Then wirte events
            i = 0
            while i < len(chart.EventGroups):
                # Loop in event groups
                # Get current group in groups
                group: EventGroup = chart.EventGroups[i]

                # Write Timing Group Attributes
                timingGroupHead = ""
                if group.TimingGroupID != 0:
                    timingGroupHead = "  "
                    attributes = ""
                    j = 0
                    while j < len(group.TimingGroupAttributes):
                        attributes += group.TimingGroupAttributes[j]
                        if j != len(group.TimingGroupAttributes) - 1:
                            attributes += "_"
                        j += 1
                    file.writelines("timinggroup({0}){{".format(attributes))

                # Write event to file

                # Timing
                j = 0
                while j < len(group.Timings):
                    timing: TimingEvent = group.Timings[j]
                    line = "timing({0},%0.2f,%0.2f);".format(
                        timing.Timing) % (timing.Bpm, timing.Beats)
                    file.writelines("{0}{1}".format(timingGroupHead, line))
                    file.writelines("\n")
                    j += 1

                # Tap
                j = 0
                while j < len(group.Taps):
                    tap: TapNote = group.Taps[j]
                    line = "({0},{1});".format(tap.Timing, tap.Track)
                    file.writelines("{0}{1}".format(timingGroupHead, line))
                    file.writelines("\n")
                    j += 1

                # Hold
                j = 0
                while j < len(group.Holds):
                    hold: HoldNote = group.Holds[j]
                    line = "hold({0},{1},{2});".format(
                        hold.Timing, hold.EndTiming, hold.Track)
                    file.writelines("{0}{1}".format(timingGroupHead, line))
                    file.writelines("\n")
                    j += 1

                # Arc
                j = 0
                while j < len(group.Arcs):
                    arc: ArcNote = group.Arcs[j]
                    line = "arc({0},{1},%0.2f,%0.2f,{2},%0.2f,%0.2f,{3},{4},{5})".format(
                        arc.Timing, arc.EndTiming, arc.LineType,
                        arc.Color, arc.FxName, str(arc.IsTrace).lower()
                    ) % (
                        arc.StartX, arc.EndX, arc.StartY, arc.EndY
                    )
                    if arc.ArcTaps != []:
                        line += "["
                        k = 0
                        while k < len(arc.ArcTaps):
                            line += "arctap({0})".format(arc.ArcTaps[k])
                            if k != len(arc.ArcTaps) - 1:
                                line += ","
                            k += 1
                        line += "]"
                    line += ";"
                    file.writelines("{0}{1}".format(timingGroupHead, line))
                    file.writelines("\n")
                    j += 1

                # Flick
                j = 0
                while j < len(group.Flicks):
                    flick: FlickNote = group.Flicks[j]
                    line = "flick({0},%0.2f,%0.2f,%0.2f,%0.2f);".format(flick.Timing) % (
                        flick.PosX, flick.PosY, flick.VecX, flick.VecY
                    )
                    file.writelines("{0}{1}".format(timingGroupHead, line))
                    file.writelines("\n")
                    j += 1

                # Camera
                j = 0
                while j < len(group.Cameras):
                    camera: CameraEvent = group.Cameras[j]
                    line = "camera({0},%0.2f,%0.2f,%0.2f,%0.2f,%0.2f,%0.2f,{1},{2});".format(
                        camera.Timing, camera.CameraType, camera.Dutation
                    ) % (
                        camera.PosX, camera.PosY, camera.PosZ,
                        camera.RotX, camera.RotY, camera.RotZ
                    )
                    file.writelines("{0}{1}".format(timingGroupHead, line))
                    file.writelines("\n")
                    j += 1

                # SceneControl
                j = 0
                while j < len(group.SceneControls):
                    sc: SceneControl = group.SceneControls[j]
                    lineend = ""
                    if sc.SceneControlType != "trackhide" or sc.SceneControlType != "trackshow":
                        lineend = ",%0.2f,{0}".format(
                            sc.ParamInt) % (sc.ParamFloat)
                    line = "scenecontrol({0},{1}{2});".format(
                        sc.Timing, sc.SceneControlType, lineend)
                    file.writelines("{0}{1}".format(timingGroupHead, line))
                    file.writelines("\n")
                    j += 1

                if group.TimingGroupID != 0:
                    file.writelines("};")
                    file.writelines("\n")

                i += 1
