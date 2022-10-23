import math
from Utils.MathUtil import*
from Utils.StringParser import*
import ArcaeaFileFormat as Aff
import AffOption as option
import re

class ArcAlgorithm:
    # Easing Base

    def Straight(self, start: float, end: float, t: float):
        return (1 - t) * start + end * t

    def Out(self, start: float, end: float, t: float):
        return start + (end - start) * (1 - math.cos(1.5707963 * t))

    def In(self, start: float, end: float, t: float):
        return start + (end - start) * (math.sin(1.5707963 * t))

    def Both(self, start: float, end: float, t: float):
        o = float(1 - t)
        return math.pow(o, 3) * start + 3 * math.pow(o, 2) * t * start + 3 * o * math.pow(t, 2) * end + math.pow(t, 3) * end

    # Get value between two points by linetype

    def ArcX(self, start: float, end: float, t: float, linetype: str):
        linetype = linetype.strip().lower()
        if linetype == "s":
            return self.Straight(self, start, end, t)
        elif linetype == "b":
            return self.Both(self, start, end, t)
        elif linetype == "si" or linetype == "sisi" or linetype == "siso":
            return self.In(self, start, end, t)
        elif linetype == "so" or linetype == "sosi" or linetype == "soso":
            return self.Out(self, start, end, t)
        return self.Straight(self, start, end, t)

    def ArcY(self, start: float, end: float, t: float, linetype: str):
        linetype = linetype.strip().lower()
        if linetype == "s" or linetype == "si" or linetype == "so":
            return self.Straight(self, start, end, t)
        elif linetype == "b":
            return self.Both(self, start, end, t)
        elif linetype == "sisi" or linetype == "sosi":
            return self.In(self, start, end, t)
        elif linetype == "siso" or linetype == "soso":
            return self.Out(self, start, end, t)
        return self.Straight(self, start, end, t)

    # Get point between two points by linetype

    def GetArcPoint(self, start: list, end: list, t: float, linetype: str):
        x = self.ArcX(self, start[0], end[0], t, linetype)
        y = self.ArcY(self, start[1], end[1], t, linetype)
        return [x, y]

class FileUtil:
    def GetInputPath() -> list:
        if option.UseCustomForcePath == True:
            filePath = option.FilePath
            outPath = option.OutPath
        else:
            filePath = input("\n输入文件路径:\n").replace("\\","/")
            outPath = input("\n输入输出路径:\n").replace("\\","/")
        return [filePath,outPath]

class AffUtil:

    # There is utils of Arcaea chart file

    def GetEventStartTiming(context: str, eventhead: str):
        context = context.strip()
        s = StringParser(context)
        s.Skip(eventhead)
        value = s.ReadInt(",")
        return value

    def GetArcPosition(context: str):
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
        return "{0},{1},{2},{3}".format(startx, endx, starty, endy)

    def GetArcEventLine(self,
                        timing: int, endtiming: int,
                        startx: float, endx: float,
                        linetype: str, starty: float, endy: float,
                        color: int, fxname: str, istance: bool, arctaps=[]):
        # timing endtiming startx endx linetype starty endy color fxname istance
        result = "arc({0},{1},%0.2f,%0.2f,{2},%0.2f,%0.2f,{3},{4},{5})".format(
            timing, endtiming, linetype, color, fxname, "true" if istance == True else "false"
        ) % (
            startx, endx, starty, endy
        )
        if arctaps != []:
            result += "["
            i = 0
            length = len(arctaps)
            while i < length:
                result += "arctap({0})".format(arctaps[i])
                if i != length - 1:
                    result += ","
                i += 1
            result += "]"
        result += ";"
        return result

    def GetFittingEvent(self, obj):
        trackpos = [-0.75, -0.25, 0.25, 0.75, 1.25, 1.75]
        if type(obj) == Aff.TapNote:
            tap: Aff.TapNote = obj
            arc = Aff.ArcNote()
            arc.Timing = tap.Timing
            arc.EndTiming = tap.Timing + 1
            arc.StartX = -0.75 + 0.5 * tap.Track
            arc.EndX = arc.StartX
            arc.StartY = arc.EndY = 1
            arc.IsTrace = True
            arc.ArcTaps = [tap.Timing]
            return arc
        if type(obj) == Aff.HoldNote:
            hold: Aff.HoldNote = obj
            arc = Aff.ArcNote()
            arc.Timing = hold.Timing
            arc.EndTiming = hold.EndTiming
            arc.StartX = -0.75 + 0.5 * hold.Track
            arc.EndX = arc.StartX
            arc.StartY = arc.EndY = 1
            return arc
        if type(obj) == Aff.ArcNote:
            fitnum = option.FittingApproximately
            arc: Aff.ArcNote = obj
            notes = []
            addnewhold = False
            newtrack = 0
            if arc.StartX == arc.EndX and arc.StartY == arc.EndY == 1:
                j = 0
                while j < len(trackpos):
                    if MathUtil.Approximately(arc.StartX, trackpos[j], fitnum):
                        addnewhold = True
                        newtrack = j
                        break
                    j += 1
            if addnewhold == True:
                newhold = Aff.HoldNote()
                newhold.Timing = arc.Timing
                newhold.EndTiming = arc.EndTiming
                newhold.Track = newtrack
                arc.StartY = 1 - arc.StartY
                arc.EndY = 1 - arc.EndY
            else:
                arc.StartY = 1 - arc.StartY
                arc.EndY = 1 - arc.EndY
            # If arc.ArcTaps isn't empty, add each arctap pos to pos list
            if arc.ArcTaps != []:
                poslist = []
                i = 0
                while i < len(arc.ArcTaps):
                    duration = arc.EndTiming - arc.Timing
                    percent = (arc.ArcTaps[i] - arc.Timing) / duration
                    pos = ArcAlgorithm.GetArcPoint(
                        ArcAlgorithm,
                        [arc.StartX, arc.StartY],  # Start pos
                        [arc.EndX, arc.EndY],  # End pos
                        percent, arc.LineType)
                    poslist.append(pos)
                    i += 1
                # Loop in pos list, fit to track if x pos is approximately then track pos
                i = 0
                while i < len(poslist):
                    istapnote = False
                    x = poslist[i][0]
                    y = poslist[i][1]
                    # Fit to Tap Note
                    newtrack = 0
                    j = 0
                    while j < len(trackpos):
                        if MathUtil.Approximately(x, trackpos[j], fitnum):
                            istapnote = True
                            newtrack = j
                            break
                        j += 1
                    # If fit success, convert to tap note and add to note list
                    if istapnote == True:
                        newtap = Aff.TapNote()
                        newtap.Timing = arc.ArcTaps[i]
                        newtap.Track = newtrack
                        notes.append(newtap)
                    else:
                        newarc = Aff.ArcNote()
                        newarc.Timing = arc.ArcTaps[i]
                        newarc.EndTiming = arc.ArcTaps[i] + 1
                        newarc.StartX = newarc.EndX = x
                        newarc.StartY = newarc.EndY = y
                        newarc.FxName = arc.FxName
                        newarc.ArcTaps = [arc.ArcTaps[i]]
                        notes.append(newarc)
                    i += 1
            arc.ArcTaps = []   
            notes.append(arc)
            return notes

    # There is tools of Arcaea chart file

    def ConvertAffPathToShadow(self, filePath: str, outPath: str):
        lines = []
        # Load Chart first
        AffChart = Aff.Chart(filePath)
        # Loop in Chart event groups
        i = 0
        while i < len(AffChart.EventGroups):
            # Defined field "group" used for Convert
            group: Aff.EventGroup = AffChart.EventGroups[i]
            lines.append("timinggroup(noinput){")

            # Timing
            j = 0
            while j < len(group.Timings):
                timing: Aff.TimingEvent = group.Timings[j]
                lines.append("  timing({0},%0.2f,%0.2f);".format(
                    timing.Timing) % (timing.Bpm, timing.Beats))
                j += 1

            # Tap
            j = 0
            while j < len(group.Taps):
                tap: Aff.TapNote = group.Taps[j]
                posx = -0.75 + 0.5 * tap.Track
                line = self.GetArcEventLine(self,
                                            tap.Timing, tap.Timing + 1, posx, posx, "s", 10, 10, 0, "none", True, [tap.Timing])
                lines.append("  {0}".format(line))
                j += 1

            # Hold
            j = 0
            while j < len(group.Holds):
                hold: Aff.HoldNote = group.Holds[j]
                baseposx = -0.75 + 0.5 * hold.Track
                left = baseposx - 0.12
                right = baseposx + 0.12
                # Left
                # Head
                line = self.GetArcEventLine(
                    self,
                    hold.Timing, hold.Timing, -100, left, "s", 10, 10, 0, "none", False)
                lines.append("  {0}".format(line))
                # Body
                line = self.GetArcEventLine(
                    self,
                    hold.Timing, hold.EndTiming, left, left, "s", 10, 10, 0, "none", False)
                lines.append("  {0}".format(line))
                # Right
                # Head
                line = self.GetArcEventLine(
                    self,
                    hold.Timing, hold.Timing, 100, right, "s", 10, 10, 0, "none", False)
                lines.append("  {0}".format(line))
                # Body
                line = self.GetArcEventLine(
                    self,
                    hold.Timing, hold.EndTiming, right, right, "s", 10, 10, 0, "none", False)
                lines.append("  {0}".format(line))
                j += 1

            # Arc
            j = 0
            while j < len(group.Arcs):
                arc: Aff.ArcNote = group.Arcs[j]
                # Head
                if arc.IsTrace == False:
                    line = self.GetArcEventLine(
                        self,
                        arc.Timing, arc.Timing, -100, arc.StartX, "s", 10, 10, 0, "none", False)
                    lines.append("  {0}".format(line))
                # Body
                line = self.GetArcEventLine(
                    self,
                    arc.Timing, arc.EndTiming, arc.StartX, arc.EndX,
                    arc.LineType, 10, 10, 0, arc.FxName, arc.IsTrace, arc.ArcTaps)
                lines.append("  {0}".format(line))
                j += 1

            # Flick
            j = 0
            while j < len(group.Flicks):
                flick: Aff.FlickNote = group.Flicks[j]
                line = "  flick({0},%0.2f,%0.2f,%0.2f,%0.2f);".format(flick.Timing) % (
                    flick.PosX, flick.PosY, flick.VecX, flick.VecY)
                lines.append(line)
                j += 1

            # Camera
            j = 0
            while j < len(group.Cameras):
                camera: Aff.CameraEvent = group.Cameras[j]
                line = "  camera({0},%0.2f,%0.2f,%0.2f,%0.2f,%0.2f,%0.2f,{1},{2});".format(
                    camera.Timing, camera.CameraType, camera.Dutation) % (
                        camera.PosX, camera.PosY, camera.PosZ,
                        camera.RotX, camera.RotY, camera.RotZ)
                lines.append(line)
                j += 1

            # SceneControl
            j = 0
            while j < len(group.SceneControls):
                sc: Aff.SceneControl = group.SceneControls[j]
                line = "  scenecontrol({0},{1}".format(
                    sc.Timing, sc.SceneControlType)
                if sc.SceneControlType != "trackshow" or sc.SceneControlType != "trackhide":
                    line += ",{0},%0.2f".format(sc.ParamInt) % (sc.ParamFloat)
                line += ");"
                lines.append(line)
                j += 1

            lines.append("};")
            i += 1
        # Write lines to file
        with open(outPath, 'w') as file:
            i = 0
            while i < len(lines):
                file.writelines(lines[i])
                file.writelines("\n")
                i += 1
        print("\n文件已写入\n")

    def MirrorAllNotes(self, filePath: str, outPath: str):
        affChart: Aff.Chart = Aff.Chart(filePath)
        i = 0
        while i < len(affChart.EventGroups):
            group: Aff.EventGroup = affChart.EventGroups[i]

            if group.TimingGroupID != 0:
                j = 0
                while j < len(group.TimingGroupAttributes):
                    # Mirror angle dgree
                    if re.match("anglex(\d+)", group.TimingGroupAttributes[j]):
                        anglex = int(
                            group.TimingGroupAttributes[j].replace("anglex"))
                        anglex = 3600 - anglex
                        group.TimingGroupAttributes[j] = "anglex{0}".format(
                            anglex)
                    j += 1

            # Mirror Notes

            # Tap
            j = 0
            while j < len(group.Taps):
                tap: Aff.TapNote = group.Taps[j]
                tap.Track = -tap.Track + 5
                group.Taps[j] = tap
                j += 1

            # Hold
            j = 0
            while j < len(group.Holds):
                hold: Aff.HoldNote = group.Holds[j]
                hold.Track = 5 - hold.Track
                group.Holds[j] = hold
                j += 1

            # Arc

            # Get bigest color id used for mirror Arc color
            maxColorID = int(0)
            j = 0
            while j < len(group.Arcs):
                arc: Aff.ArcNote = group.Arcs[j]
                if maxColorID < arc.Color:
                    maxColorID = arc.Color
                j += 1
            if maxColorID < 1:
                maxColorID = 1

            # Mirror Arc
            j = 0
            while j < len(group.Arcs):
                arc: Aff.ArcNote = group.Arcs[j]
                arc.StartX = 1 - arc.StartX
                arc.EndX = 1 - arc.EndX
                arc.Color = maxColorID - arc.Color
                group.Arcs[j] = arc
                j += 1

            # Flick
            j = 0
            while j < len(group.Flicks):
                flick: Aff.FlickNote = group.Flicks[j]
                flick.PosX = 1 - flick.PosX
                flick.VecX = float(-flick.VecX)
                group.Flicks[j] = flick
                j += 1

            # Camera
            j = 0
            while j < len(group.Cameras):
                camera: Aff.CameraEvent = group.Cameras[j]
                if camera.PosX != 0:
                    camera.PosX = float(-camera.PosX)
                if camera.RotX != 0:
                    camera.RotX = float(-camera.RotX)
                if camera.RotZ != 0:
                    camera.RotZ = float(-camera.RotZ)
                group.Cameras[j] = camera
                j += 1

            i += 1
        Aff.AffWriter.WriteEvents(Aff.AffWriter, outPath, affChart)
        print("\n文件已写入\n")

    def ReverseAllNotes(self,filePath:str,outPath:str):
        chart = Aff.Chart(filePath)
        i = 0
        while i < len(chart.EventGroups):
            group:Aff.EventGroup = chart.EventGroups[i]

            Taps = []
            Holds = []
            Arcs = []
            Flicks = []
            Cameras = []
            SceneControls = []

            if option.ReverseAngle == True:
                j = 0
                while j < len(group.TimingGroupAttributes):
                    if re.Match("angley(\d+)",group.TimingGroupAttributes[j]):
                        angley = int(group.TimingGroupAttributes[j].replace("angley"))
                        angley = 3600 - angley
                        group.TimingGroupAttributes[j] = "angley{0}".format(angley)
                    j += 1

            if option.ReverseFitting == True:
                # Tap
                j = 0
                while j < len(group.Taps):
                    tap:Aff.TapNote = group.Taps[j]
                    Arcs.append(self.GetFittingEvent(self,tap))
                    j += 1
                # Hold
                j = 0
                while j < len(group.Holds):
                    hold:Aff.HoldNote = group.Holds[i]
                    Arcs.append(self.GetFittingEvent(self,hold))
                    j += 1
                # Arc
                j = 0
                while j < len(group.Arcs):
                    arc:Aff.ArcNote = group.Arcs[j]
                    notes:list = self.GetFittingEvent(self,arc)
                    if notes != None:
                        k = 0
                        while k < len(notes):
                            note = notes[k]
                            if type(note) == Aff.TapNote:
                                Taps.append(note)
                            if type(note) == Aff.HoldNote:
                                Holds.append(note)
                            if type(note) == Aff.ArcNote:
                                Arcs.append(note)
                            k += 1
                    j += 1
            else:
                # Tap
                Taps = group.Taps
                # Hold
                Holds = group.Holds
                # Arc
                j = 0
                while j < len(group.Arcs):
                    arc:Aff.ArcNote = group.Arcs[j]
                    arc.StartY = 1 - arc.StartY
                    arc.EndY = 1 - arc.EndY
                    Arcs.append(arc)
                    j += 1

            # Flick
            j = 0
            while j < len(group.Flicks):
                flick:Aff.FlickNote = group.Flicks[j]
                flick.PosY = 1 - flick.PosY
                flick.VecY = -flick.VecY
                Flicks.append(flick)
                j += 1

            # Camera
            if option.ReversePos == True or option.ReverseRot == True:
                j = 0
                while j < len(group.Cameras):
                    camera:Aff.CameraEvent = group.Cameras[j]
                    if option.ReversePos == True:
                        camera.PosY = -camera.PosY
                    if option.ReverseRot == True:
                        camera.RotY = -camera.RotY
                    Cameras.append(camera)
                    j += 1
            else:
                Cameras = group.Cameras

            # SceneControl
            SceneControls = group.SceneControls

            group.Taps = Taps
            group.Holds = Holds
            group.Arcs = Arcs
            group.Flicks = Flicks
            group.Cameras = Cameras
            group.SceneControls = SceneControls

            chart.EventGroups[i] = group
            i += 1
        Aff.AffWriter.WriteEvents(Aff.AffWriter,outPath,chart)
        print("\n文件已写入\n")

    def ConvertToKey(self,filePath:str,outPath:str):
        # Load chart.
        chart = Aff.Chart(filePath)

        # Note track in arc x pos.
        trackPos = [-0.75,-0.25,0.25,0.75,1.25,1.75]

        # For each group of all groups and for each note in group.
        AllTaps = []
        AllHolds = []

        # Local Methods.

        def checkEventOverlap(timing,track,endTiming=-1) -> bool:
            # Assign note.
            isHold = endTiming != -1
            note = Aff.TapNote()
            if isHold:
                note = Aff.HoldNote()
            note.Timing = timing
            note.Track = track
            if isHold:
                note.EndTiming = endTiming
            # Check note is overlap or to close.
            # If overlap or to close, return false.
            for n in AllTaps:
                if math.fabs(note.Timing - n.Timing) < 25:
                    return True
            for n in AllHolds:
                # If note timing in hold range, return false.
                if note.Timing > n.Timing and note.Timing < n.EndTiming:
                    return True
            return False

        def findNearAbleLane(timing, track): # -> int | bool
            notes = []
            # Find all nearest note.
            for n in AllTaps:
                if math.fabs(n.Timing - timing) < 25:
                    notes.append(n)
            for n in AllHolds:
                if math.fabs(n.Timing - timing) < 25 or math.fabs(n.EndTiming - timing) < 25:
                    notes.append(n)
            # Compare notes.
            result = track
            if result is None:
                return False
            tryResult = []
            # Loop 5 times in notes.
            for i in range(6):
                for n in notes:
                    if n.Track == result:
                        result += 1
                        result %= 5
                if result not in tryResult:
                    tryResult.append(result)
            # If sorted result is full, return false.
            if sorted(tryResult) == [0,1,2,3,4,5]:
                return False
            # Else, return result.
            return result

        # Return the nearest track by x pos.
        def getNearestTrack(x) -> int:
            for pos in trackPos:
                if abs(x - pos) <= 0.5:
                    result = trackPos.index(pos)
                    if x > 0.5 and result < 5:
                        return result + 1
                    return result

        # First foreach group is used to add note.
        for group in chart.EventGroups:
            # If group item type isnt Aff.EventGroup, we dont edit it.
            if type(group) is Aff.EventGroup:
                for n in group.Taps:
                    AllTaps.append(n)
                for n in group.Holds:
                    AllHolds.append(n)

        # Second foreach group is used to convert note.
        for group in chart.EventGroups:
            # Because Tap and Hold is in lane, so we dont edit them.
            # But we will add item to them.
            # If group item type isnt Aff.EventGroup, we dont edit it.
            if type(group) is Aff.EventGroup:
                Taps = group.Taps
                Holds = group.Holds
                # For each Arc in Arcs.
                for a in group.Arcs:
                    if type(a) is Aff.ArcNote:

                        # Return a value between arc startX and arc endX.
                        def getPosXAt(timing) -> float:
                            return ArcAlgorithm.ArcX(
                                ArcAlgorithm, a.StartX, a.EndX, timing, a.LineType)

                        # If arc is tance arc, we will convert arctaps to taps.
                        if a.IsTrace:
                            for at in a.ArcTaps:
                                # Get pos x.
                                posX = getPosXAt(at)
                                # Convert pos to note track.
                                track = getNearestTrack(posX)
                                # Check track is invalid.
                                # If track is uninvalid, continue.
                                if checkEventOverlap(at,track):
                                    track = findNearAbleLane(at,track)
                                    if track == False:
                                        continue
                                # If track is invalid, convert it to tap note and add to list.
                                n = Aff.TapNote()
                                n.Timing = at
                                n.Track = track
                                AllTaps.append(n)
                                Taps.append(n)
                        else:
                            # Convert pos to note track.
                            track = getNearestTrack(a.StartX)
                            # Check track is invalid.
                            # If track is uninvalid, continue.
                            if checkEventOverlap(a.Timing,track,a.EndTiming):
                                track = findNearAbleLane(a.Timing,track)
                                if track == False:
                                    continue
                            # If track is invalid, convert it to hold note and add to list.
                            n = Aff.HoldNote()
                            n.Timing = a.Timing
                            n.Track = track
                            n.EndTiming = a.EndTiming
                            AllHolds.append(n)
                            Holds.append(n)

                    for f in group.Flicks:
                        if type(f) is Aff.FlickNote:
                            # Convert pos to note track.
                            track = getNearestTrack(f.PosX)
                            # Check track is invalid.
                            # If track is uninvalid, continue.
                            if checkEventOverlap(f.Timing,track):
                                track = findNearAbleLane(f.Timing,track)
                                if track == False:
                                    continue
                            # If track is invalid, convert it to tap note and add to list.
                            n = Aff.TapNote()
                            n.Timing = f.Timing
                            n.Track = track
                            AllTaps.append(n)
                            Taps.append(n)

                # Final, we need set note value to group.
                group.Arcs.clear()
                group.Flicks.clear()
                group.Taps = Taps
                group.Holds = Holds
        # Write chart to file.
        Aff.AffWriter.WriteEvents(Aff.AffWriter,outPath,chart)
        print("\n文件已写入\n")

    # There is Functions for edit Aff chart

    def Func_AffPathToShadow():
        paths = FileUtil.GetInputPath()
        filePath = paths[0]
        outPath = paths[1]
        AffUtil.ConvertAffPathToShadow(AffUtil, filePath, outPath)

    def Func_Mirror():
        paths = FileUtil.GetInputPath()
        filePath = paths[0]
        outPath = paths[1]
        AffUtil.MirrorAllNotes(AffUtil, filePath, outPath)

    def Func_Reverse():
        paths = FileUtil.GetInputPath()
        filePath = paths[0]
        outPath = paths[1]
        AffUtil.ReverseAllNotes(AffUtil, filePath, outPath)

    def Func_ToKey():
        paths = FileUtil.GetInputPath()
        filePath = paths[0]
        outPath = paths[1]
        AffUtil.ConvertToKey(AffUtil, filePath, outPath)
