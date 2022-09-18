import AffOption as option
from Easing.Easings import *
from Easing.EasingUtil import *
from Utils.MathUtil import *
from Utils.StringParser import *
from Utils.ParserUtil import*
from Aff.AffUtil import *

class AffTimingUtil:
    # start timing, end timing, start bpm, end bpm, step, ease type
    def CalcEasingTimings(self, tstart: int, tend: int, bstart: float, bend: float, step: int, easing: str):
        result = []
        tseg0 = int((tend - tstart) / step)
        i = 0
        print("\n输出:")
        while i <= step:
            p = i / step
            num = EasingUtil.CalcValue(bstart, bend, p, easing)
            r = "timing({0},%0.2f,4.00);".format(int(tstart + i * tseg0)) % num
            print("    {0}".format(r))
            result.append(r)
            i += 1
        return result

    def CalcOffsetedArc(line: str, offsettiming: int, offsetx: float, offsety: float):
        # Read context
        s = StringParser(line)
        s.Skip("arc(")
        timing = s.ReadInt(",")
        endtiming = s.ReadInt(",")
        startx = s.ReadFloat(",")
        endx = s.ReadFloat(",")
        linetype = s.ReadString(",")
        starty = s.ReadFloat(",")
        endy = s.ReadFloat(",")
        color = s.ReadInt(",")
        fx = s.ReadString(",")
        isvoid = s.ReadBool(")")
        arctaps = []
        if s.Current() != ";":
            while s.Current() != ",":
                s.Skip(8)
                arctaps.append(s.ReadInt(")"))
        # Calc offset
        timing += offsettiming
        endtiming += offsettiming
        startx += offsetx
        endx += offsetx
        starty += offsety
        endy += offsety
        if arctaps != []:
            i = 0
            while i < len(arctaps):
                arctaps[i] += offsettiming
                i += 1
        # Return context
        arctapsstr = ""
        if arctaps != []:
            arctapsstr += "["
            i = 0
            while i < len(arctaps):
                arctapsstr += "arctap({0}),".format(arctaps[i])
                i += 1
            arctapsstr += "]"
        arctapsstr += ";"
        result = "arc({0},{1},%0.2f,%0.2f,{2},%0.2f,%0.2f,{3},{4},{5}){6}".format(
            timing, endtiming, linetype, color, fx, "true" if isvoid else "false", arctapsstr
        ) % (startx, endx, starty, endy)
        return result

    def BuildCube(pos: list, size: list, length: int, timing: int, worldpos: bool, stroke: bool):
        arcarr = []
        startx = float(pos[0]) - float(size[0]) / 2
        endx = float(pos[0]) + float(size[0]) / 2
        starty = float(pos[1]) - float(size[1]) / 2
        endy = float(pos[1]) + float(size[1]) / 2
        if worldpos == False:
            startx = startx * 0.5
            endx = endx * 0.5
        # Build front
        arcarr.append("arc({0},{1},%0.2f,%0.2f,s,%0.2f,%0.2f,0,none,true);".format(
            timing, timing) % (startx, endx, starty, starty))
        arcarr.append("arc({0},{1},%0.2f,%0.2f,s,%0.2f,%0.2f,0,none,true);".format(
            timing, timing) % (startx, endx, endy, endy))
        arcarr.append("arc({0},{1},%0.2f,%0.2f,s,%0.2f,%0.2f,0,none,true);".format(
            timing, timing) % (startx, startx, starty, endy))
        arcarr.append("arc({0},{1},%0.2f,%0.2f,s,%0.2f,%0.2f,0,none,true);".format(
            timing, timing) % (endx, endx, starty, endy))
        if stroke == True:
            arcarr.append("arc({0},{1},%0.2f,%0.2f,s,%0.2f,%0.2f,0,none,true);".format(
                timing, timing) % (startx, endx, starty, endy))
        # Build Cube if length != 0
        if length != 0:
            # Copy front with offset
            i = 0
            while i < 4:
                arcarr.append(AffTimingUtil.CalcOffsetedArc(
                    arcarr[i], length, 0, 0))
                i += 1
            # Build z-axis
            arcarr.append("arc({0},{1},%0.2f,%0.2f,s,%0.2f,%0.2f,0,none,true);".format(
                timing, timing + length) % (startx, startx, starty, starty))
            arcarr.append("arc({0},{1},%0.2f,%0.2f,s,%0.2f,%0.2f,0,none,true);".format(
                timing, timing + length) % (endx, endx, starty, starty))
            arcarr.append("arc({0},{1},%0.2f,%0.2f,s,%0.2f,%0.2f,0,none,true);".format(
                timing, timing + length) % (startx, startx, endy, endy))
            arcarr.append("arc({0},{1},%0.2f,%0.2f,s,%0.2f,%0.2f,0,none,true);".format(
                timing, timing + length) % (endx, endx, endy, endy))
            if stroke == True:
                arcarr.append("arc({0},{1},%0.2f,%0.2f,s,%0.2f,%0.2f,0,none,true);".format(
                    timing + length, timing + length) % (startx, endx, endy, starty))
                arcarr.append("arc({0},{1},%0.2f,%0.2f,s,%0.2f,%0.2f,0,none,true);".format(
                    timing, timing + length) % (startx, startx, endy, starty))
                arcarr.append("arc({0},{1},%0.2f,%0.2f,s,%0.2f,%0.2f,0,none,true);".format(
                    timing, timing + length) % (endx, endx, starty, endy))
                arcarr.append("arc({0},{1},%0.2f,%0.2f,s,%0.2f,%0.2f,0,none,true);".format(
                    timing, timing + length) % (startx, endx, endy, endy))
                arcarr.append("arc({0},{1},%0.2f,%0.2f,s,%0.2f,%0.2f,0,none,true);".format(
                    timing, timing + length) % (endx, startx, starty, starty))
        return arcarr

    def Func_GetTimings():
        arr0 = input(
            "\n按格式输入:\n    开始时间 结束时间 开始Bpm 结束Bpm 拟合精度 缓动类型\n").split(" ")
        timingarr = AffTimingUtil.CalcEasingTimings(
            int(arr0[0]), int(arr0[1]), float(arr0[2]), float(
                arr0[3]), int(arr0[4]), arr0[5],
        )
        if option.UseCustomForcePath == True:
            outpath = option.OutPath
        else:
            outpath = input("\n输入输出文件路径:\n").replace("\\","/")
        with open(outpath, 'w') as f:
            i = 0
            size = len(timingarr)
            while i < size:
                f.writelines("{0}\n".format(timingarr[i]))
                i += 1
        print("文件已写入\n")

    def Func_OffsetAff():
        # Based settings
        if option.UseCustomForcePath == True:
            inpath = option.FilePath
            outpath = option.OutPath
        else:
            inpath = input("\n输入原始Arc片段文件路径:\n").replace("\\","/")
            outpath = input("\n输入输出Arc片段文件路径:\n").replace("\\","/")
        # Animation settings
        arr = input(
            "\n按格式输入:\n    偏移x 偏移y 动画时长 拟合精度 缓动类型 在每个循环添加开始组\n"
        ).split(" ")
        offsetx = float(arr[0])
        offsety = float(arr[1])
        duration = int(arr[2])
        step = int(arr[3])
        loop = int(arr[4])
        easing = arr[5]
        addgroup = ParseUtil.ParseBool(arr[6])
        # Generate animation
        arcarr = []
        exarcarr = []
        timingarr = []
        with open(inpath, 'r') as f:
            lines = f.readlines()
            i = 0
            linesize = int(len(lines))
            duration *= loop
            while i < linesize:
                line = lines[i].strip().replace("\n", "")
                if line.startswith("arc(") == True:
                    l = 0
                    while l < loop:
                        if addgroup == True:
                            lp = l
                            if l == 0:
                                lp = loop
                            r = lp % 2
                            arcstr = AffTimingUtil.CalcOffsetedArc(
                                line, int(duration / loop * lp), offsetx * r, offsety * r)
                            exarcarr.append(arcstr)
                        currpos = ""
                        s = 0
                        while s < step:
                            p = EasingUtil.GetValue(
                                float(1 / step * s), easing)
                            if l % 2 != 0:
                                p = 1 - p
                            offsett = duration / loop / step * s + duration / loop * l
                            arcstr = AffTimingUtil.CalcOffsetedArc(
                                line, int(offsett), offsetx * p, offsety * p)
                            if arcstr in arcarr == False and AffUtil.GetArcPosition(arcstr) != currpos:
                                arcarr.append(arcstr)
                                currpos = AffUtil.GetArcPosition(arcstr)
                            s += 1
                        l += 1
                elif line.startswith("timing(") == True:
                    timingarr.append(line)
                i += 1
        with open(outpath, 'w') as w:
            size = 0
            if addgroup == True:
                size = int(len(exarcarr))
                i = 0
                while i < size:
                    w.writelines("{0}\n".format(exarcarr[i]))
                    i += 1
            size = int(len(arcarr))
            i = 0
            while i < size:
                line = arcarr[i]
                w.writelines("timinggroup({0}){{\n".format(
                    "noinput" if i != size - 1 else ""))
                if i <= 0:
                    j = 0
                    while j < int(len(timingarr)):
                        w.writelines("  {0}\n".format(timingarr[j]))
                        w.writelines("  scenecontrol({0},hidegroup,0.00,1);\n".format(
                            AffUtil.GetEventStartTiming(arcarr[i], "arc(")))
                        j += 1
                else:
                    showtiming = AffUtil.GetEventStartTiming(
                        arcarr[i - 1], "arc(")
                    hidetiming = AffUtil.GetEventStartTiming(arcarr[i], "arc(")
                    if i < size - 1:
                        w.writelines("  timing(0,100.00,4.00);\n")
                        w.writelines(
                            "  timing({0},999999.00,4.00);\n".format(showtiming - 1))
                        w.writelines(
                            "  timing({0},0.00,4.00);\n".format(showtiming))
                        w.writelines(
                            "  timing({0},100.00,4.00);\n".format(hidetiming))
                        w.writelines(
                            "  scenecontrol({0},hidegroup,0.00,1);\n".format(hidetiming))
                    else:
                        j = 0
                        while j < int(len(timingarr)):
                            w.writelines("  {0}\n".format(timingarr[j]))
                            j += 1
                        w.writelines("  scenecontrol(0,hidegroup,0.00,1);\n")
                        w.writelines(
                            "  scenecontrol({0},hidegroup,0.00,0);\n".format(showtiming))
                w.writelines("  {0}\n".format(line))
                w.writelines("};\n")
                i += 1
        print("文件已写入\n")

    def Func_Cube():
        # Based settings
        if option.UseCustomForcePath == True:
            outpath = option.OutPath
        else:
            outpath = input("\n输入输出Arc片段文件路径:\n").replace("\\","/")
        # Create Cube
        arr = input(
            "\n按格式输入:\n    位置 大小 长度 使用世界坐标 三角描边\n" +
            "    例: 0.5,0.5 1,1 300 false true\n"
        ).split(" ")
        pos = arr[0].split(",")
        pos[0] = "{0}".format(float(pos[0]) * 2)
        size = arr[1].split(",")
        length = int(arr[2])
        worldpos = ParseUtil.ParseBool(arr[3])
        stroke = ParseUtil.ParseBool(arr[4])
        timing = int(input("输入开始时间:\n"))
        # Build Cube
        arcarr = AffTimingUtil.BuildCube(
            pos, size, length, timing, worldpos, stroke)
        with open(outpath, 'w') as w:
            i = 0
            while i < int(len(arcarr)):
                w.writelines("{0}\n".format(arcarr[i]))
                i += 1
        print("\n文件已写入\n")

    def Func_CubeAnim():
        # Based settings
        if option.UseCustomForcePath == True:
            outpath = option.OutPath
        else:
            outpath = input("\n输入输出Arc片段文件路径:\n").replace("\\","/")
        # Animation settings
        # startpos endpos startsize endsize stroke
        arr = input(
            "\n按格式输入:\n    开始位置 结束位置 开始大小 结束大小 三角描边\n" +
            "    例: 0,0.5 1,1 1,1,200 0.5,0.5,100 true\n"
        ).split(" ")
        startpos = arr[0].split(",")
        endpos = arr[1].split(",")
        startsize = arr[2].split(",")
        endsize = arr[3].split(",")
        stroke = ParseUtil.ParseBool(arr[4])
        # starttiming duration step loop easing addgroup
        arr = input(
            "\n按格式输入:\n    开始时间 持续时间 拟合精度 循环次数 缓动类型 在每个循环添加开始组\n" +
            "    例: 1000 2000 120 1 outquad true\n"
        ).split(" ")
        starttiming = int(arr[0])
        duration = int(arr[1])
        step = int(arr[2])
        loop = int(arr[3])
        easing = arr[4]
        addgroup = ParseUtil.ParseBool(arr[5])
        # Build Animation
        arcgroups = []
        timings = []
        exgroups = []
        # Get each Cube frame
        startposx = float(startpos[0])
        startposy = float(startpos[1])
        endposx = float(endpos[0])
        endposy = float(endpos[1])
        startsizex = float(startsize[0])
        startsizey = float(startsize[1])
        startlength = int(startsize[2])
        endsizex = float(endsize[0])
        endsizey = float(endsize[1])
        endlength = int(endsize[2])
        bpm = 100
        offsetlength = 100000
        duration *= loop
        loopcount = 0
        while loopcount < loop:
            if addgroup == True and step % 2 != 0:
                lp = loopcount
                if loopcount == 0:
                    lp = loop
                r = lp % 2
                x = startposx if r != 0 else endposx
                y = startposy if r != 0 else endposy
                sx = startsizex if r != 0 else endsizex
                sy = startsizey if r != 0 else endsizey
                l = startlength if r != 0 else endlength
                t = starttiming + duration / loop * loopcount + offsetlength
                pos = "{0},{1}".format(x, y).split(",")
                size = "{0},{1}".format(sx, sy).split(",")
                exgroups.append(AffTimingUtil.BuildCube(
                    pos, size, int(l), int(t), False, stroke))
            stepcount = 0
            currtimings = []
            fix = 0
            while stepcount < step:
                p = EasingUtil.GetValue(float(1 / step * stepcount), easing)
                if loopcount % 2 != 0:
                    p = 1 - p
                p = math.fabs(p)
                x = startposx + (endposx - startposx) * p
                y = startposy + (endposy - startposy) * p
                pos = "{0},{1}".format(x * 2, y).split(",")
                x = startsizex + (endsizex - startsizex) * p
                y = startsizey + (endsizey - startsizey) * p
                length = startlength + (endlength - startlength) * p
                size = "{0},{1}".format(x, y).split(",")
                offset = duration / loop / step * stepcount + duration / loop * loopcount
                timing = int(starttiming + offset + offsetlength)
                if stepcount > 0:
                    fix = (timing - offsetlength) - currtimings[stepcount - 1]
                timing -= fix
                currtimings.append(int(timing - offsetlength + fix))
                arcgroups.append(AffTimingUtil.BuildCube(
                    pos, size, int(length), int(timing), False, stroke))
                stepcount += 1
            timingcount = 0
            # Fix timings
            while timingcount < int(len(currtimings)):
                if timingcount == int(len(currtimings) - 1):
                    currtimings[int(len(currtimings) - 1)] += fix
                timings.append(currtimings[timingcount])
                timingcount += 1
            loopcount += 1
        # Build timing groups
        timinggroups = []
        i = 0
        while i < int(len(timings)):
            lines = []
            lines.append("timinggroup(noinput){")
            if i > 0:
                showtiming = timings[i - 1]
                hidetiming = timings[i]
                showduration = int(hidetiming - showtiming)
                lines.append("  timing(0,%0.2f,4.00);" % (bpm))
                lines.append("  timing({0},%0.2f,4.00);".format(
                    int(showtiming)) % (-bpm * offsetlength))
                lines.append("  timing({0},%0.2f,4.00);".format(
                    int(showtiming + 1)) % (0))
                lines.append("  timing({0},%0.2f,4.00);".format(
                    int(hidetiming)) % (-bpm * offsetlength))
                lines.append("  timing({0},%0.2f,4.00);".format(
                    int(hidetiming + 1)) % (bpm))
                lines.append("  timing({0},%0.2f,4.00);".format(
                    int(showtiming + offsetlength - 1)) % (bpm * showduration))
                lines.append("  timing({0},%0.2f,4.00);".format(
                    int(showtiming + offsetlength)) % (bpm))
            else:
                t = timings[0]
                lines.append("  timing(0,%0.2f,4.00);" % (bpm))
                lines.append("  timing({0},%0.2f,4.00);".format(
                    int(t)) % (-bpm * offsetlength))
                lines.append("  timing({0},%0.2f,4.00);".format(
                    int(t + 1)) % (bpm))
            j = 0
            while j < int(len(arcgroups[i])):
                line = arcgroups[i][j]
                lines.append("  {0}".format(line))
                j += 1
            lines.append("};")
            timinggroups.append(lines)
            i += 1
        # Write to file
        with open(outpath, 'w') as w:
            i = 0
            while i < int(len(timinggroups)):
                tg = timinggroups[i]
                if addgroup == False and step % 2 == 0 and i % step == 0 and i > 0:
                    i += 1
                    continue
                j = 0
                while j < int(len(tg)):
                    if j > 0 and tg[j] == tg[j - 1]:
                        continue
                    w.write(tg[j])
                    w.write("\n")
                    j += 1
                i += 1
            if addgroup == True and exgroups != []:
                lines = []
                i = 0
                while i < int(len(exgroups)):
                    j = 0
                    while j < int(len(exgroups[i])):
                        group = exgroups[i]
                        arcstr = group[j]
                        timing = AffUtil.GetEventStartTiming(
                            arcstr.strip(), "arc(") - offsetlength
                        lines.append("  timing(0,%0.2f,4.00);" % (bpm))
                        lines.append("  timing({0},%0.2f,4.00);".format(
                            int(timing)) % (-bpm * offsetlength))
                        lines.append("  timing({0},%0.2f,4.00);".format(
                            int(timing + 1)) % (bpm))
                        lines.append("  {0}".format(arcstr))
                        j += 1
                    i += 1

        print("\n文件已写入\n")

