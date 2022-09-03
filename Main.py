from Easings import*
from EasingUtil import* 
from TimingUtil import*
import re

class UtilCore:
    callCount = 0

    def Main():
        unknown = True
        if UtilCore.callCount == 0:
            print("使用 /help 展示帮助列表\n")
        s = input()
        if s == "/quit":
            return
        if s == "/help":
            print(UtilCore.Help())
            unknown = False
        if s == "/ease tips":
            print(EasingUtil.GetTips())
            unknown = False
        if re.match("/ease (calc|value) (\d+(\.?)(\d+)?) (\d+(\.?)(\d+)?) (\d+(\.?)(\d+)?) (\d+)", s):
            m0arr = s.replace("/ease", "").replace("calc ", "").replace("value ", "").split(" ")
            min = float(m0arr[1])
            max = float(m0arr[2])
            size = float(m0arr[3])
            ease = int(m0arr[4])
            result = EasingUtil.CalcValue(min, max, size, ease)
            print(result)
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
        if unknown == True:
            print("未知指令，使用 /help 展示帮助列表\n")
        UtilCore.callCount += 1
        UtilCore.Main()

    def Help():
        i = 0
        # Help list
        arr = [
            "",
            "基础指令:",
            "    /quit - 退出",
            "",
            "Ease 缓动帮助:",
            "    /ease tips - 展示缓动类型 ID",
            "    /ease <calc或value> <最小值:Float> <最大值:Float> <0-1:Float> <0-30:Int> - 计算对应点的值",
            "",
            "Aff 拓展指令:",
            "    /affutil easetiming - 获取缓动 Timing 列表",
            "    /affutil affanim - 获取帧动画 Aff 列表",
            "    /affutil cube - 获取立方体 Aff 列表",
            "    /affutil affanim2 - 获取 Cube 帧动画 Aff 列表",
            "    /affutil afftoshadow - 将 Aff 片段转换为由 Arc 事件构成的阴影谱面",
            "    /affutil affmirror - 镜像谱面",
            "",
        ]
        count = len(arr)
        while i < count:
            print(arr[i])
            i += 1
        return ""

UtilCore.Main()