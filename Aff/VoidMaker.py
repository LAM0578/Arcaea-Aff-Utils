# Notes:
# 'x => x.value' in python is 'lambda x: x.value'
from copy import copy, deepcopy
from Aff.AffUtil import*
import ArcaeaFileFormat as Aff
from Vector.Vec2 import *
import math


class voidModels:
    def __init__(self, tapNotes: list) -> None:
        tapNotes = sorted(tapNotes,key = lambda n: n.Timing)
        self.tapNotes = tapNotes

    tapNoteLength = 25
    arcHeadLength = 5

    def tapModel(self, n: Aff.TapNote) -> list:
        length = self.tapNoteLength
        result = []
        # Get pos
        basePosX = -0.75 + n.Track * 0.5
        left = basePosX - 0.25 + 0.03
        right = basePosX + 0.25 - 0.03
        # Assign arc
        arc = Aff.ArcNote()
        arc.IsTrace = True
        arc.StartY = arc.EndY = -0.2
        # Left
        arc.Timing = n.Timing
        arc.EndTiming = n.Timing + length
        arc.StartX = arc.EndX = left
        result.append(copy(arc))
        # Right
        arc.Timing = n.Timing
        arc.EndTiming = n.Timing + length
        arc.StartX = arc.EndX = right
        result.append(copy(arc))
        # Back
        arc.Timing = n.Timing + length
        arc.EndTiming = n.Timing + length
        arc.StartX = left
        arc.EndX = right
        result.append(copy(arc))
        # Front
        arc.Timing = n.Timing
        arc.EndTiming = n.Timing
        arc.StartX = left
        arc.EndX = right
        result.append(copy(arc))
        return result

    def holdModel(self, n: Aff.HoldNote) -> list:
        result = []
        # Get pos
        basePosX = -0.75 + n.Track * 0.5
        left = basePosX - 0.25 + 0.03
        right = basePosX + 0.25 - 0.03
        # Assign arc
        arc = Aff.ArcNote()
        arc.IsTrace = True
        arc.StartY = arc.EndY = -0.2
        # Left
        arc.Timing = n.Timing
        arc.EndTiming = n.EndTiming
        arc.StartX = arc.EndX = left
        result.append(copy(arc))
        # Right
        arc.Timing = n.Timing
        arc.EndTiming = n.EndTiming
        arc.StartX = arc.EndX = right
        result.append(copy(arc))
        # Back
        arc.Timing = n.EndTiming
        arc.EndTiming = n.EndTiming
        arc.StartX = left
        arc.EndX = right
        result.append(copy(arc))
        # Front
        arc.Timing = n.Timing
        arc.EndTiming = n.Timing
        arc.StartX = left
        arc.EndX = right
        result.append(copy(arc))
        return result

    def arcModel(self, n: Aff.ArcNote, isHead: bool, isHeight: bool, noInput: bool) -> list:
        result = []
        startX = n.StartX
        endX = n.EndX
        startY = n.StartY
        endY = n.EndY
        isFx = n.FxName != 'none'
        # If arc note is trace, add it to result list.
        # region: Create void arc model.
        # print('in model target void: ' + n.IsTrace.__str__())
        
        def assignArcPoints(note:Aff.ArcNote,point_start:Vec2, point_End:Vec2) -> Aff.ArcNote:
            note.StartX = point_start.x
            note.EndX = point_End.x
            note.StartY = point_start.y
            note.EndY = point_End.y
            return note

        if n.IsTrace:
            a = deepcopy(n)
            a.ArcTaps.clear()
            result.append(a)
        else:
            # Build void
            # Point start
            # region PointValues
            point_start_left = Vec2(startX - 0.09, startY - 0.08)
            point_start_mid = Vec2(startX, startY + 0.09)
            point_start_right = Vec2(startX + 0.09, startY - 0.08)
            # Point end
            point_end_left = Vec2(endX - 0.09, endY - 0.08)
            point_end_mid = Vec2(endX, endY + 0.09)
            point_end_right = Vec2(endX + 0.09, endY - 0.08)
            # endregion
            # region BodyPoints
            # Body Point X
            bodyPoint_left_x = Vec2(point_start_left.x, point_end_left.x)
            bodyPoint_mid_x = Vec2(point_start_mid.x, point_end_mid.x)
            bodyPoint_right_x = Vec2(point_start_right.x, point_end_right.x)
            # Body Point Y
            bodyPoint_left_y = Vec2(point_start_left.y, point_end_left.y)
            bodyPoint_mid_y = Vec2(point_start_mid.y, point_end_mid.y)
            bodyPoint_right_y = Vec2(point_start_right.y, point_end_right.y)
            # endregion
            # Body
            # If duration != 0, build body.
            if abs(n.EndTiming - n.Timing) > 0:
                timing = n.Timing
                endTiming = n.EndTiming
                # If duration < 0, reverse timing.
                if n.EndTiming - n.Timing < 0:
                    timing = n.EndTiming
                    endTiming = n.Timing
                # Assign arc
                arc = Aff.ArcNote()
                arc.Timing = timing
                arc.EndTiming = endTiming
                arc.LineType = n.LineType
                arc.IsTrace = True
                # Body left
                result.append(assignArcPoints(arc,\
                    Vec2(bodyPoint_left_x.x,bodyPoint_left_y.x),Vec2(bodyPoint_left_x.y,bodyPoint_left_y.y)))
                # Body Mid
                result.append(assignArcPoints(arc,\
                    Vec2(bodyPoint_mid_x.x,bodyPoint_mid_x.y),Vec2(bodyPoint_mid_y.x,bodyPoint_mid_y.y)))
                # Body Right
                result.append(assignArcPoints(arc,\
                    Vec2(bodyPoint_right_x.x,bodyPoint_right_y.x),Vec2(bodyPoint_right_x.y,bodyPoint_right_y.y)))
            # End
            # Assign arc
            arc = Aff.ArcNote()
            arc.Timing = n.EndTiming
            arc.EndTiming = n.EndTiming
            arc.IsTrace = True
            # End Segment Left
            result.append(assignArcPoints(arc,\
                    Vec2(point_end_mid.x,point_end_left.x),Vec2(point_end_mid.y,point_end_left.y)))
            # End Segment Right
            result.append(assignArcPoints(arc,\
                    Vec2(point_end_mid.x,point_end_right.x),Vec2(point_end_mid.y,point_end_right.y)))
            # End Segment Right
            # Height
            # If start y = end y = 0.2, builded void height is point.
            if isHeight and not (startY == endY == -0.2):
                # Assign arc
                arc = Aff.ArcNote()
                arc.IsTrace = True
                arc.Timing = n.Timing
                arc.EndTiming = n.Timing
                arc.StartY = -0.2
                arc.EndY = startY - 0.08
                # Left
                arc.StartX = arc.EndX = startX - 0.01
                result.append(copy(arc))
                # Right
                arc.StartX = arc.EndX = startX + 0.01
                result.append(copy(arc))
            # Head
            if isHead:
                # Assign arc
                arc = Aff.ArcNote()
                arc.IsTrace = True
                arc.Timing = n.Timing - voidModels.arcHeadLength
                arc.EndTiming = n.Timing
                # Left
                result.append(assignArcPoints(arc,\
                        Vec2(point_start_mid.x,point_start_left.y),Vec2(point_start_left.x,point_start_left.y)))
                # Mid
                result.append(assignArcPoints(arc,\
                        Vec2(point_start_mid.x,startY - 0.08),Vec2(point_start_mid.x,point_start_mid.y)))
                # Right
                result.append(assignArcPoints(arc,\
                        Vec2(point_start_mid.x,point_start_right.y),Vec2(point_start_right.x,point_start_right.y)))
                # BodyPath
                arc.Timing = n.Timing
                arc.EndTiming = n.Timing
                # Left
                result.append(assignArcPoints(arc,\
                        Vec2(point_start_mid.x,point_start_mid.y),Vec2(point_start_left.x,point_start_left.y)))
                # Right
                result.append(assignArcPoints(arc,\
                        Vec2(point_start_mid.x,point_start_mid.y),Vec2(point_start_right.x,point_start_right.y)))
        # endregion
        # region: Create void arcTaps model.

        def arcTapModel(timing: int) -> list:
            result = []
            # Get percent first.
            t = (timing - n.Timing) / float(n.EndTiming - n.Timing)
            # Then get arc tap pos.
            pos = ArcAlgorithm.GetArcPoint(
                ArcAlgorithm, [n.StartX, n.StartY], [n.EndX, n.EndY], t, n.LineType)
            # Define float values
            x = pos[0]
            y = pos[1]
            endTiming = timing + int(voidModels.tapNoteLength / 2)

            # Get points.
            point_0 = Vec2(x,y) + Vec2(-0.25+0.02,-0.01)
            point_1 = Vec2(x,point_0.y) + Vec2(0.25-0.02,-0.15)
            # region: Create arc tap void cube.
            # Assign arc
            arc = Aff.ArcNote()
            arc.IsTrace = True

            # Point Top Start
            arc.Timing = timing
            arc.EndTiming = timing
            result.append(assignArcPoints(arc,\
                    point_0,Vec2(point_1.x,point_0.y)))
            # Point Top End
            arc.Timing = endTiming
            arc.EndTiming = endTiming
            arc.StartX = point_0.x
            arc.EndX = point_1.x
            arc.StartY = point_0.y
            arc.EndY = point_0.y
            result.append(assignArcPoints(arc,\
                    point_0,Vec2(point_1.x,point_0.y)))
            # Point Bottom Start
            arc.Timing = timing
            arc.EndTiming = timing
            result.append(assignArcPoints(arc,\
                    Vec2(point_0.x,point_1.y),point_1))
            # Point Bottom End
            arc.Timing = endTiming
            arc.EndTiming = endTiming
            result.append(assignArcPoints(arc,\
                    Vec2(point_0.x,point_1.y),point_1))
            
            # Point Left Start
            arc.Timing = timing
            arc.EndTiming = timing
            result.append(assignArcPoints(arc,\
                    point_0,Vec2(point_0.x,point_1.y)))
            # Point Left End
            arc.Timing = endTiming
            arc.EndTiming = endTiming
            result.append(assignArcPoints(arc,\
                    point_0,Vec2(point_0.x,point_1.y)))
            # Point Right Start
            arc.Timing = timing
            arc.EndTiming = timing
            result.append(assignArcPoints(arc,\
                    Vec2(point_1.x,point_0.y),point_1))
            # Point Right End
            arc.Timing = endTiming
            arc.EndTiming = endTiming
            result.append(assignArcPoints(arc,\
                    Vec2(point_1.x,point_0.y),point_1))
            
            # Point Left Top
            arc.Timing = timing
            arc.EndTiming = endTiming
            result.append(assignArcPoints(arc,\
                    point_0,point_0))
            # Point Left Bottom
            arc.Timing = timing
            arc.EndTiming = endTiming
            result.append(assignArcPoints(arc,\
                    Vec2(point_0.x,point_1.y),Vec2(point_0.x,point_1.y)))
            # Point Right Top
            arc.Timing = timing
            arc.EndTiming = endTiming
            result.append(assignArcPoints(arc,\
                    Vec2(point_1.x,point_0.y),Vec2(point_1.x,point_0.y)))
            # Point Right Bottom
            arc.Timing = timing
            arc.EndTiming = endTiming
            result.append(assignArcPoints(arc,\
                    point_1,point_1))
            # endregion
            return result

        def glassArcTapModel(timing:int) -> list:
            result = []
            # Get percent first.
            t = (timing - n.Timing) / float(n.EndTiming - n.Timing)
            # Then get arc tap pos.
            pos = ArcAlgorithm.GetArcPoint(
                ArcAlgorithm, [n.StartX, n.StartY], [n.EndX, n.EndY], t, n.LineType)
            # Define float values.
            x = pos[0]
            y = pos[1]
            halfEndTiming = timing + int(voidModels.tapNoteLength / 2 / 2)
            endTiming = timing + int(voidModels.tapNoteLength / 2)
            def offsetArcs(lst:list,offsetTiming:int) -> list:
                result = []
                for a in lst:
                    a = copy(a)
                    a.Timing += offsetTiming
                    a.EndTiming += offsetTiming
                    result.append(copy(a))
                return result
            def mirrorArcs(lst:list,mx:float) -> list:
                result = []
                for a in lst:
                    a = copy(a)
                    s = a.StartX + (mx - a.StartX) * 2
                    e = a.EndX + (mx - a.EndX) * 2
                    a.StartX = s
                    a.EndX = e
                    result.append(copy(a))
                return result
            # region: Get Points
            # Center point of model.
            model_basepos = Vec2(x, y - 0.08)
            # region: Cube points.
            cube_center = model_basepos
            cube_left = cube_center + Vec2(-0.04,0)
            cube_right = cube_center + Vec2(0.04,0)
            cube_top = cube_center + Vec2(0,0.08)
            cube_bottom = cube_center + Vec2(0,-0.08)
            # endregion
            # region: Append points.
            append_top_start = model_basepos + Vec2(0,0.1)
            append_top_end = append_top_start + Vec2(0,0.04)
            append_bottom_start = model_basepos + Vec2(0,-0.14)
            append_bottom_end = append_bottom_start + Vec2(0,0.04)
            # endregion
            # region: Main part left.
            main_left_top_left = model_basepos + Vec2(-0.25+0.02,0.08)
            main_left_top_right = model_basepos + Vec2(-0.07,0.08)
            main_left_bottom_left = model_basepos + Vec2(-0.25+0.02,-0.08)
            main_left_bottom_right = model_basepos + Vec2(-0.07,-0.08)
            main_left_center = model_basepos + Vec2(-0.09,0)
            # endregion
            # Main right path used mirror.
            # endregion
            # region: Build void glass arc tap model.
            # Assign arc
            arc = Aff.ArcNote()
            arc.IsTrace = True
            # region: Build cube
            # Left top
            arc.Timing = halfEndTiming
            arc.EndTiming = halfEndTiming
            arc = assignArcPoints(arc,cube_left,cube_top)
            result.append(copy(arc))
            # Left bottom
            arc.Timing = halfEndTiming
            arc.EndTiming = halfEndTiming
            arc = assignArcPoints(arc,cube_left,cube_bottom)
            result.append(copy(arc))
            # Right top
            arc.Timing = halfEndTiming
            arc.EndTiming = halfEndTiming
            arc = assignArcPoints(arc,cube_right,cube_top)
            result.append(copy(arc))
            # Right bottom
            arc.Timing = halfEndTiming
            arc.EndTiming = halfEndTiming
            arc = assignArcPoints(arc,cube_right,cube_bottom)
            result.append(copy(arc))

            # Top left top
            arc.Timing = halfEndTiming
            arc.EndTiming = endTiming
            arc = assignArcPoints(arc,cube_left,cube_center)
            result.append(copy(arc))
            # Top left bottom
            arc.Timing = timing
            arc.EndTiming = halfEndTiming
            arc = assignArcPoints(arc,cube_center,cube_left)
            result.append(copy(arc))
            # Top right top
            arc.Timing = halfEndTiming
            arc.EndTiming = endTiming
            arc = assignArcPoints(arc,cube_right,cube_center)
            result.append(copy(arc))
            # Top right bottom
            arc.Timing = timing
            arc.EndTiming = halfEndTiming
            arc = assignArcPoints(arc,cube_center,cube_right)
            result.append(copy(arc))

            # Right side left top
            arc.Timing = timing
            arc.EndTiming = halfEndTiming
            arc = assignArcPoints(arc,cube_center,cube_top)
            result.append(copy(arc))
            # Right side left bottom
            arc.Timing = timing
            arc.EndTiming = halfEndTiming
            arc = assignArcPoints(arc,cube_center,cube_bottom)
            result.append(copy(arc))
            # Right side right top
            arc.Timing = halfEndTiming
            arc.EndTiming = endTiming
            arc = assignArcPoints(arc,cube_top,cube_center)
            result.append(copy(arc))
            # Right side right bottom
            arc.Timing = halfEndTiming
            arc.EndTiming = endTiming
            arc = assignArcPoints(arc,cube_bottom,cube_center)
            result.append(copy(arc))
            
            # endregion
            # region: Build append
            # Top
            arc.Timing = halfEndTiming
            arc.EndTiming = halfEndTiming
            arc = assignArcPoints(arc,append_top_start,append_top_end)
            result.append(copy(arc))
            # Bottom
            arc.Timing = halfEndTiming
            arc.EndTiming = halfEndTiming
            arc = assignArcPoints(arc,append_bottom_start,append_bottom_end)
            result.append(copy(arc))
            # endregion
            # region: Build main left
            arcs = []
            mirArcs = []
            # Left
            arc.Timing = timing
            arc.EndTiming = timing
            arc = assignArcPoints(arc,main_left_top_left,main_left_bottom_left)
            arcs.append(copy(arc))
            mirArcs.append(copy(arc))
            result.append(copy(arc))
            # Top
            arc.Timing = timing
            arc.EndTiming = timing
            arc = assignArcPoints(arc,main_left_top_left,main_left_top_right)
            arcs.append(copy(arc))
            mirArcs.append(copy(arc))
            result.append(copy(arc))
            # Bottom
            arc.Timing = timing
            arc.EndTiming = timing
            arc = assignArcPoints(arc,main_left_bottom_left,main_left_bottom_right)
            arcs.append(copy(arc))
            mirArcs.append(copy(arc))
            result.append(copy(arc))
            # Right top
            arc.Timing = timing
            arc.EndTiming = timing
            arc = assignArcPoints(arc,main_left_top_right,main_left_center)
            arcs.append(copy(arc))
            mirArcs.append(copy(arc))
            result.append(copy(arc))
            # Right bottom
            arc.Timing = timing
            arc.EndTiming = timing
            arc = assignArcPoints(arc,main_left_bottom_right,main_left_center)
            arcs.append(copy(arc))
            mirArcs.append(copy(arc))
            result.append(copy(arc))
            
            # Append lines
            mirAppend = []
            # Left top
            arc.Timing = timing
            arc.EndTiming = endTiming
            arc = assignArcPoints(arc,main_left_top_left,main_left_top_left)
            mirAppend.append(copy(arc))
            result.append(copy(arc))
            # Left bottom
            arc.Timing = timing
            arc.EndTiming = endTiming
            arc = assignArcPoints(arc,main_left_bottom_left,main_left_bottom_left)
            mirAppend.append(copy(arc))
            result.append(copy(arc))
            # Right top
            arc.Timing = timing
            arc.EndTiming = endTiming
            arc = assignArcPoints(arc,main_left_top_right,main_left_top_right)
            mirAppend.append(copy(arc))
            result.append(copy(arc))
            # Right bottom
            arc.Timing = timing
            arc.EndTiming = endTiming
            arc = assignArcPoints(arc,main_left_bottom_right,main_left_bottom_right)
            mirAppend.append(copy(arc))
            result.append(copy(arc))

            arcs = offsetArcs(arcs,int(self.tapNoteLength / 2))
            result.extend(arcs)
            mirAppend.extend(arcs)
            # endregion
            # region: Main right path used mirror.
            result.extend(mirrorArcs(mirArcs,x))
            result.extend(mirrorArcs(mirAppend,x))
            # endregion
            # endregion
            return result

        def connetionLineModel(timing:int) -> list:
            result = []
            if noInput:
                return result
            # Get percent first.
            t = (timing - n.Timing) / float(n.EndTiming - n.Timing)
            # Then get arc tap pos.
            pos = ArcAlgorithm.GetArcPoint(
                ArcAlgorithm, [n.StartX, n.StartY], [n.EndX, n.EndY], t, n.LineType)
            # Get all tap note if abs(tap.Timing - timing) <= 1.
            taps = filter(lambda n: abs(n.Timing - timing) <= 1, self.tapNotes)
            # Create void connetion line for each tap note.
            for t in taps:
                arc = Aff.ArcNote()
                arc.Timing = arc.EndTiming = t.Timing
                arc.StartX = pos[0]
                arc.EndX = -0.75 + t.Track * 0.5
                arc.StartY = pos[1] - 0.15
                arc.EndY = -0.2
                arc.IsTrace = True
                result.append(copy(arc))
            return result
        
        for at in n.ArcTaps:
            # Get arcTap void model and append to result.
            append_arcs = arcTapModel(at)
            if isFx:
                append_arcs = glassArcTapModel(at)
            result.extend(append_arcs)
            # Get connetionLine void model and append to result.
            result.extend(connetionLineModel(at))
        # endregion
        return result

    def flickModel(self, n: Aff.FlickNote) -> list:
        print('This module is abandoned.')
        return []
        result = []
        # Vector to deg.
        rad = math.atan2(n.VecX, n.VecY)
        deg = math.degrees(rad)
        # Local methods.
        def flickPosToArc(pos:Vec2) -> Vec2:
            # To world pos.
            y = pos.y * 5.5
            # To arc pos.
            pos.y = (y - 1) / 4.5
            return pos
        def assignArcPos(arc:Aff.ArcNote,start:Vec2,end:Vec2) -> Aff.ArcNote:
            note = copy(arc)
            note.StartX = start.x
            note.EndX = end.x
            note.StartY = start.y
            note.EndY = end.y
            return note
        def rotatePoint(start:Vec2,end:Vec2,deg:float) -> Vec2:
            result = Vec2()
            rad = math.radians(-deg)
            p = abs(deg % 90) / 90
            result.x = (end.x - start.x) * (2 - p) * math.cos(rad) - (end.y - start.y) * (1 - p / 2) * math.sin(rad) + start.x
            result.y = (end.x - start.x) * (2 - p) * math.sin(rad) + (end.y - start.y) * (1 - p / 2) * math.cos(rad) + start.y
            result.x /= 1.5
            result.y *= 1.25
            result.y -= (start.y * 0.35)
            return result

        # Build base model
        pos = flickPosToArc(Vec2(n.PosX,n.PosY))
        point_left = rotatePoint(pos, pos + Vec2(-0.13,0), deg)
        point_right = rotatePoint(pos, pos + Vec2(0.13,0), deg)
        point_top = rotatePoint(pos, pos + Vec2(0,0.8), deg)
        point_bottom = rotatePoint(pos, pos + Vec2(0,0.15), deg)
        side_left = 0
        side_right = 0
        # Assign arc
        arc = Aff.ArcNote()
        arc.Timing = arc.EndTiming = n.Timing
        arc.IsTrace = True
        # Left
        line = [point_left,point_top]
        result.append(assignArcPos(arc,line[0],line[1]))
        line = [point_left,point_bottom]
        result.append(assignArcPos(arc,line[0],line[1]))
        # Right
        line = [point_right,point_top]
        result.append(assignArcPos(arc,line[0],line[1]))
        line = [point_right,point_bottom]
        result.append(assignArcPos(arc,line[0],line[1]))
        # Rotate model and return.
        # return rotateArcGroup(result,pos,deg)
        return result

class voidMaker:
    
    def __convertToVoid(filePath:str,outpath:str) -> None:
        # We load chart at first.
        chart = Aff.Chart(filePath)
        # Add all target notes to list.
        allTaps = []
        allArcs = []
        for group in chart.EventGroups:
            allTaps.extend(group.Taps)
            for a in group.Arcs:
                # [timingGroupID,arc]
                allArcs.append([group.TimingGroupID,a])
        # Sort all arcs by arc.timing.
        sorted(allArcs,key=lambda a: a[1].Timing)
        model = voidModels(allTaps)
        # Relationship arc item will add to here.
        # [arc,isHead,isHeight,groupID]
        rArcs = [[a[1],True,True,a[0]] for a in allArcs]
        # region: Get arc relationship.
        # Convert and add all arc item to rArcs.
        for a in rArcs:
            for b in rArcs:
                # If a is equals to b, continue.
                if a == b:
                    continue
                # If x difference <= 0.1 and timing difference < 10 and a.EndY == b.StartY,
                # check a.IsTrace is equals to b.IsTrace.
                if abs(a[0].EndX - b[0].StartX) <= 0.1 and\
                   abs(a[0].EndTiming - b[0].Timing) < 10 and\
                   a[0].EndY == b[0].StartY:
                    # If a.IsTrace is equals to b.IsTrace, b.IsHead set to false.
                    if a[0].IsTrace == b[0].IsTrace:
                        b[1] = False
                # Set IsHeight
                # If IsHeight, will build void height model when build void arc model.
                a[2] = not(\
                    (a[0].IsTrace) or\
                    (a[0].StartY == a[0].EndY and not(a[1])))
                b[2] = not(\
                    (b[0].IsTrace) or\
                    (b[0].StartY == b[0].EndY and not(b[1])))
        # endregion     
        # Then convert for each group events to void model.
        for group in chart.EventGroups:
            if type(group) is Aff.EventGroup:
                noinput = 'noinput' in group.TimingGroupAttributes
                # Find all current group arcs.
                groupArcs = filter(lambda n: n[3] == group.TimingGroupID ,rArcs)
                # Converted notes void model will add to here.
                arcs = []
                for t in group.Taps:
                    arcs.extend(model.tapModel(t))
                for t in group.Holds:
                    arcs.extend(model.holdModel(t))
                for t in groupArcs:
                    # [arc,isHead,isHeight,groupID]
                    arcs.extend(model.arcModel(t[0],t[1],t[2],noinput))
                # for t in group.Flicks:
                #     arcs.extend(model.flickModel(t))
                # Clear all unusing notes and set group's Arcs this arcs.
                group.ClearAllNotes()
                group.Arcs = arcs
        # Write chart to output path.
        Aff.AffWriter.WriteEvents(Aff.AffWriter,outpath,chart)

    def Func_ConvertToVoid():
        path = FileUtil.GetInputPath()
        voidMaker.__convertToVoid(path[0],path[1])
        print("\n文件已写入\n")

