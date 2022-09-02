from StringParser import *
import ArcaeaFileFormat as Aff


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
                line = self.GetArcEventLine(self,
                    hold.Timing, hold.Timing, -100, left, "s", 10, 10, 0, "none", False)
                lines.append("  {0}".format(line))
                # Body
                line = self.GetArcEventLine(self,
                    hold.Timing, hold.EndTiming, left, left, "s", 10, 10, 0, "none", False)
                lines.append("  {0}".format(line))
                # Right
                # Head
                line = self.GetArcEventLine(self,
                    hold.Timing, hold.Timing, 100, right, "s", 10, 10, 0, "none", False)
                lines.append("  {0}".format(line))
                # Body
                line = self.GetArcEventLine(self,
                    hold.Timing, hold.EndTiming, right, right, "s", 10, 10, 0, "none", False)
                lines.append("  {0}".format(line))
                j += 1

            # Arc
            j = 0
            while j < len(group.Arcs):
                arc: Aff.ArcNote = group.Arcs[j]
                # Head
                if arc.IsTrace == False:
                    line = self.GetArcEventLine(self,
                        arc.Timing, arc.Timing, -100, arc.StartX, "s", 10, 10, 0, "none", False)
                    lines.append("  {0}".format(line))
                # Body
                line = self.GetArcEventLine(self,
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
        print("文件已写入\n")

    # There is Functions for edit Aff chart

    def Func_AffPathToShadow():
        filePath = input("\n输入文件路径:\n")
        outPath = input("\n输入输出路径:\n")
        AffUtil.ConvertAffPathToShadow(AffUtil,filePath,outPath)

# AffUtil.ConvertAffPathToShadow(
#     AffUtil, "F:/dl/grievouslady/2.aff", "F:/dl/grievouslady/outputshadow.aff")
