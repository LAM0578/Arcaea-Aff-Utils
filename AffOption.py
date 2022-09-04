# 路径选项
# 注意: 需要将路径中的 "\" 替换成 "/" 来避免部分字符被转义产生的报错
# 举例: "F:\Folder\File.txt" => "F:/Folder/File.txt"
UseCustomForcePath:bool = False # 使用固定路径
FilePath:str = "" # 输入文件路径
OutPath:str = "" # 输出文件路径 

# 颠倒选项
ReverseAngle:bool = False # 颠倒 Angle
ReverseFitting:bool = True # 使用物件拟合
FittingApproximately:float = 0.05 # 拟合精度 (越小越精确)

# 颠倒 Camera 选项
ReversePos:bool = True # 颠倒 Move Y
ReverseRot:bool = True # 颠倒 Rotate Y
