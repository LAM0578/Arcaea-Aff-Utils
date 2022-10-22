# Camera Origin Position: Vec3(0,990,0)
# Track to Camera x Offset: 425 : 1

from AffOption import FilePath
from Vector.Vec3 import *
from Vector.Vec2 import *
from ArcaeaFileFormat import *
import math

class AffCameraUtil:
    __OriginPos = Vec3(0, 990, 0)

    # Method

    def GetFlickOffsetMove(
        filepath: str,
        outpath: str,
        offset: float,
        easing: str,
        resetonend: bool = False,
        useresettype: bool = False,
        duration: float = 500
    ):
        easelist = ['qi', 'qo', 'l', 's', 'reset']
        if easing not in easelist or duration <= 0:
            return
        chart = Chart(filepath)
        flicks = []
        # We only use Flick notes here
        for group in chart.EventGroups:
            if type(group) is EventGroup:
                for f in group.Flicks:
                    flicks.append(f)
                # When in append to current Flick note list
                # reset group events and go to next
                group.ResetEvents()
        # After append over, clear all groups and append line
        chart.AppendLines.clear()
        chart.EventGroups.clear()
        cameras = []
        # Then we convert dgree to offset, but we need calc degree first
        for f in flicks:
            cam = CameraEvent()
            if type(f) is FlickNote:
                # Get degree first
                rad = math.atan2(f.VecX, f.VecY)
                # deg = math.degrees(rad)
                # If deg is zero, offset will always point to right
                # Convert to Vec2
                ovx = round(math.cos(rad), 5)
                ovy = round(math.sin(rad), 5)
                ovec = Vec2(ovx, ovy) * offset
                cam.Timing = f.Timing
                cam.PosX = ovec.y
                cam.PosY = ovec.x
                cam.CameraType = easing
                cam.Dutation = duration
                cameras.append(cam)
                if resetonend:
                    cam = CameraEvent()
                    cam.Timing = f.Timing + duration
                    if useresettype:
                        cam.CameraType = 'reset'
                    else:
                        cam.PosX = -ovec.y
                        cam.PosY = -ovec.x
                        cam.CameraType = 'l'
                        cam.Dutation = 10
                    cameras.append(cam)
        eventgroup = EventGroup(0)
        eventgroup.Cameras = cameras
        chart.EventGroups.append(eventgroup)
        AffWriter.WriteEvents(AffWriter,outpath,chart)
        print("\n文件已写入\n")

    # Function

    def Func_ConvertFlickToCameras():
        filepath = input('\n请输入文件路径:\n').replace("\\","/")
        outpath = input('\n请输入输出路径:\n').replace("\\","/")
        print('\n按格式输入:\n')
        arr = input('  偏移 缓动 在事件结束重置 使用 reset 类型 持续时长\n').split(' ')
        offset = float(arr[0])
        easing = arr[1]
        resetonend = arr[2].lower() == "true"
        useresettype = arr[3].lower() == "true"
        duration = int(arr[4])