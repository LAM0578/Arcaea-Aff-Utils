from Easing.Easings import*
from Easing.EasingUtil import* 
from Aff.TimingUtil import*
from Aff.AffCameraUtil import*
from Aff.VoidMaker import*
import os

class UtilCore:
    callCount = 0

    def Main():
        unknown = True
        if UtilCore.callCount == 0:
            print("使用 /help 展示帮助列表\n")
            print("编辑 AffOption.py 来修改选项\n")
        s = input()
        if s == "/quit":
            os._exit(0)
        if s == "/help":
            UtilCore.Help()
            unknown = False
        if s == "/ease tips":
            EasingUtil.GetTips()
            unknown = False
        if s == "/affutil easetiming":
            AffTimingUtil.Func_GetTimings()
            unknown = False
        if s == "/affutil affanim":
            AffTimingUtil.Func_OffsetAff()
            unknown = False
        if s == "/affutil cube":
            AffTimingUtil.Func_Cube()
            unknown = False
        if s == "/affutil affanim2":
            AffTimingUtil.Func_CubeAnim()
            unknown = False
        if s == "/affutil afftoshadow":
            AffUtil.Func_AffPathToShadow()
            unknown = False
        if s == "/affutil affmirror":
            AffUtil.Func_Mirror()
            unknown = False
        if s == "/affutil affreverse":
            AffUtil.Func_Reverse()
            unknown = False
        if s == "/affutil convert0":
            AffCameraUtil.Func_ConvertFlickToCameras()
            unknown = False
        if s == "/affutil convert1":
            AffUtil.Func_ToKey()
            unknown = False
        if s == "/affutil voidmaker":
            voidMaker.Func_ConvertToVoid()
            unknown = False
        if unknown == True:
            print(u"未知指令，使用 /help 展示帮助列表\n")
        UtilCore.callCount += 1
        UtilCore.Main()

    def Help():
        # Help list
        arr = [
            "",
            "基础指令:",
            "    /quit - 退出",
            "",
            "Ease 缓动帮助:",
            "    /ease tips - 展示缓动类型 ID",
            "",
            "Aff 拓展指令:",
            "    /affutil easetiming - 获取缓动 Timing 列表",
            "    /affutil affanim - 获取帧动画 Aff 列表",
            "    /affutil cube - 获取立方体 Aff 列表",
            "    /affutil affanim2 - 获取 Cube 帧动画 Aff 列表",
            "    /affutil afftoshadow - 将 Aff 片段转换为由 Arc 事件构成的阴影谱面",
            "    /affutil affmirror - 镜像谱面",
            "    /affutil affreverse - 颠倒谱面",
            "    /affutil convert0 - Flick 转换 Camera 移动事件",
            "    /affutil convert1 - 将谱面转换为键盘谱 注意: 比较试验性, 慎用!",
            "    /affutil voidmaker -  将谱面转换为由黑线构成的\"虚空\"谱面",
            "",
        ]
        for a in arr:
            print(a)

UtilCore.Main()