from PIL import Image
import glob
import cv2
import os.path

import pyocr
import pyocr.builders

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

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
cnt = 1
for file in files:
    print(str(cnt) + ":")
    txt = tool.image_to_string(
        Image.open(file),
        lang='eng',
        builder=pyocr.builders.TextBuilder()
        )

    title_list.append(txt)

    print(txt)
    os.remove(file)
    cnt += 1
    print("----------")

# Google search
# Obtain API KEY from local file "API_KEY"
print("=====Search analyzed titles with Youtube Data API v3=====")
api_key = open("API_KEY", "r").read()

DEVELOPER_KEY = api_key.strip()
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def youtube_search(search_word):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

    search_response = youtube.search().list(
        q = search_word,
        part = "id,snippet",
        maxResults = 5
        ).execute()

    videos = []

    # Add each result to the appropriate list, and then display the lists of videos
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos.append("%s (%s)" % (search_result["snippet"]["title"], search_result["id"]["videoId"]))

    print "Videos:\n", "\n".join(videos), "\n"

for title in title_list:
    print("Searching..." + title)

    try:
        youtube_search(title)
    except HttpError, e:
        print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
