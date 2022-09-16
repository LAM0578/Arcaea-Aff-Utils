from Utils.MathUtil import MathUtil
from Easing.Easings import*

class EasingUtil:
    
    def __GetEaseName(id):
        if id == 0:
            return Easings.easeLinear.__name__.replace("ease","")
        elif id == 1:
            return Easings.easeInSine.__name__.replace("ease","")
        elif id == 2:
            return Easings.easeOutSine.__name__.replace("ease","")
        elif id == 3:
            return Easings.easeInOutSine.__name__.replace("ease","")
        elif id == 4:
            return Easings.easeInQuad.__name__.replace("ease","")
        elif id == 5:
            return Easings.easeOutQuad.__name__.replace("ease","")
        elif id == 6:
            return Easings.easeInOutQuad.__name__.replace("ease","")
        elif id == 7:
            return Easings.easeInCubic.__name__.replace("ease","")
        elif id == 8:
            return Easings.easeOutCubic.__name__.replace("ease","")
        elif id == 9:
            return Easings.easeInOutCubic.__name__.replace("ease","")
        elif id == 10:
            return Easings.easeInQuart.__name__.replace("ease","")
        elif id == 11:
            return Easings.easeOutQuart.__name__.replace("ease","")
        elif id == 12:
            return Easings.easeInOutQuart.__name__.replace("ease","")
        elif id == 13:
            return Easings.easeInQuint.__name__.replace("ease","")
        elif id == 14:
            return Easings.easeOutQuint.__name__.replace("ease","")
        elif id == 15:
            return Easings.easeInOutQuint.__name__.replace("ease","")
        elif id == 16:
            return Easings.easeInExpo.__name__.replace("ease","")
        elif id == 17:
            return Easings.easeOutExpo.__name__.replace("ease","")
        elif id == 18:
            return Easings.easeInOutExpo.__name__.replace("ease","")
        elif id == 19:
            return Easings.easeInCirc.__name__.replace("ease","")
        elif id == 20:
            return Easings.easeOutCirc.__name__.replace("ease","")
        elif id == 21:
            return Easings.easeInOutCirc.__name__.replace("ease","")
        elif id == 22:
            return Easings.easeInBack.__name__.replace("ease","")
        elif id == 23:
            return Easings.easeOutBack.__name__.replace("ease","")
        elif id == 24:
            return Easings.easeInOutBack.__name__.replace("ease","")
        elif id == 25:
            return Easings.easeInElastic.__name__.replace("ease","")
        elif id == 26:
            return Easings.easeOutElastic.__name__.replace("ease","")
        elif id == 27:
            return Easings.easeInOutElastic.__name__.replace("ease","")
        elif id == 28:
            return Easings.easeInBounce.__name__.replace("ease","")
        elif id == 29:
            return Easings.easeOutBounce.__name__.replace("ease","")
        elif id == 30:
            return Easings.easeInOutBounce.__name__.replace("ease","")

    def GetTips():
        i = 0
        print("缓动 ID 表:")
        while i < 31:
            print("    {0} - {1}".format(i, EasingUtil.__GetEaseName(i)))
            i += 1
        print("")

    def CalcValue(min, max, x, id):
        p = EasingUtil.GetValue(x, id)
        return min + (max - min) * p

    def GetValue(x, id):
        id = MathUtil.TryParseInt(id)
        if type(id) == int:
            return Easings.Ease(x, id)
        elif type(id) == str:
            return Easings.EaseS(x, id)
