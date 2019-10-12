import os
from PIL import Image, ImageFont, ImageDraw

# 简易文字蒙太奇 @FanKetchup。 你可以修改以下值来调整产生的结果。

text = u"测试文字"
textSize = 10  # 文字的大小 (px)。
textHSp = 2  # 文字水平间距。
textVSp = 2  # 文字垂直间距。
textColor = ""  # 留空文字根据图像变色，否则是单色文字。 (格式: #F00AFF)
ims = Image.open("pic.jpg")  # 输入图像。
savename = "result.png"  # 输出图像的名字。
keyColor = "#FFFFFF"  # 抠像扣去的背景颜色，同时也将作为生成图像的背景色。
keyThres = 10  # 抠像色差范围。
thresRatio = 0.5  # 当图像区块有效像素比例超过该比例时，该区块会生成文字。
scale = 1.0  # 生成图像的尺寸比例（别设太大）。

font = ImageFont.truetype(os.path.join("fonts", "msyh.ttc"), int(textSize*scale))
# 更改字体前请翻看电脑的fonts文件夹看看字体文件的实际名称
# 例1: os.path.join("fonts", "simsun.ttc")  # 宋体
# 例2: os.path.join("fonts", "msyh.ttc")  # 微软雅黑
# 例3: os.path.join("fonts", "SourceHanSansSC-Light.otf")  # 思源黑体


def hex2RGBColor(hexcolor):
    return tuple(int((hexcolor.lstrip('#'))[k:k + 2], 16) for k in (0, 2, 4))


def RGB2hexColor(r, g, b):
    return "#{:02x}{:02x}{:02x}".format(r, g, b)


def getAvgColor(section):
    pcounts = 0
    tr = 0
    tg = 0
    tb = 0
    for si in range(0, section.width):
        for sj in range(0, section.height):
            (r, g, b) = section.getpixel((si, sj))
            diff = abs(r - RGBkeyColor[0]) + abs(g - RGBkeyColor[1]) + abs(b - RGBkeyColor[2])
            if diff > keyThres:
                pcounts = pcounts + 1
                tr = tr + r
                tg = tg + g
                tb = tb + b
    if pcounts > 0:
        avgr = int(tr / pcounts)
        avgg = int(tg / pcounts)
        avgb = int(tb / pcounts)
        avgc = (avgr, avgg, avgb)
    else:
        avgc = (0, 0, 0)
    if pcounts > section.height * section.width * thresRatio:
        flag = True
    else:
        flag = False
    return avgc, flag


neww = int(ims.width * scale)
newh = int(ims.height * scale)
ims = ims.resize((neww, newh), Image.ANTIALIAS)
ims = ims.convert("RGB")
RGBkeyColor = hex2RGBColor(keyColor)
secWidth = int((textHSp + textSize)*scale)
secHeight = int((textVSp + textSize)*scale)
secCols = int(ims.width / secWidth)
secRows = int(ims.height / secHeight)
leftPadding = int((ims.width - secCols * secWidth) / 2) + int(textHSp / 2)
upPadding = int((ims.height - secRows * secHeight) / 2) + int(textVSp / 2)
im = Image.new("RGB", (ims.width, ims.height), RGBkeyColor)
dr = ImageDraw.Draw(im)

textp = 0
texty = upPadding
print("Generating... \nTarget image size: ", ims.width, "x", ims.height)
for i in range(0, secRows):
    textx = leftPadding
    for j in range(0, secCols):
        tempsec = ims.crop((textx, texty, textx + secWidth, texty + secHeight))
        textx = textx + secWidth
        (ac, flg) = getAvgColor(tempsec)
        if flg is True and textp < len(text):
            if len(textColor) > 0:
                dr.text((textx, texty), text[textp], font=font, fill=textColor)
            else:
                dr.text((textx, texty), text[textp], font=font, fill=RGB2hexColor(ac[0], ac[1], ac[2]))
            textp = textp + 1
            if textp >= len(text):
                textp = 0
    texty = texty + secHeight

print("Finished!")
im.show()
im.save(savename)
