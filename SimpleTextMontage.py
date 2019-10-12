import os
from PIL import Image, ImageFont, ImageDraw

# Simple Text Montage by @FanKetchup. You can adjust the result by modifying the following values.

text = u"测试文字"
textSize = 10  # Size of the text (px).
textHSp = 2  # Text horizontal space.
textVSp = 2  # Text vertical space.
textColor = ""  # If you set this value, text color will not change automatically. (format: #F00AFF)
ims = Image.open("pic.jpg")  # Image source.
savename = "result.png"  # Name of the output (target) image.
keyColor = "#FFFFFF"  # Keying background color for the input image.
keyThres = 10  # Threshold for keying.
thresRatio = 0.5  # Ratio of effective pixels in a subimage to "activate".
scale = 1.0  # Change this value if you want to resize the image (Do NOT set it too large!).

font = ImageFont.truetype(os.path.join("fonts", "msyh.ttc"), int(textSize*scale))
# Open your device's font directory and check the font's name that you want to use.
# Font e.g.1: os.path.join("fonts", "simsun.ttc")  # 宋体
# Font e.g.2: os.path.join("fonts", "msyh.ttc")  # 微软雅黑
# Font e.g.3: os.path.join("fonts", "SourceHanSansSC-Light.otf")  # 思源黑体


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
