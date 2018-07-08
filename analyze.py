from PIL import Image
import glob
import cv2
import os.path

import pyocr
import pyocr.builders

# Trimming all images
files = glob.glob("./image/*")

for file in files:
    out_name, ext = os.path.splitext(file)
    out_name += '_cut.jpg'
    im = cv2.imread(file, 0)
    dst = im[650:750,0:577]
    cv2.imwrite(out_name, dst)


# OCR
tools = pyocr.get_available_tools()
if len(tools) == 0:
    print("No OCR tool found")
    sys.exit(1)
tool = tools[0]
print("Will use tool '%s'" % (tool.get_name()))

langs = tool.get_available_languages()
print("Available languages: %s" % ", ".join(langs))

files = glob.glob("./image/*_cut.jpg")

title_list = []
for file in files:
    txt = tool.image_to_string(
        Image.open(file),
        lang='eng',
        builder=pyocr.builders.TextBuilder()
        )

    title_list.append(txt)

    print(txt)
    os.remove(file)
    print("----------")

print(txt)

# Google search
