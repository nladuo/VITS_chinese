import json
import os.path

import requests
from bs4 import BeautifulSoup
from urllib.parse import quote


# tag = "胡桃"
tag = "可莉"

resp = requests.get(f"https://wiki.biligame.com/ys/{quote(tag+'语音')}")
# print(resp.content.decode("utf8"))

soup = BeautifulSoup(resp.content.decode("utf-8"))

out_div = soup.find("div", {"class": "resp-tabs-container"})
block_divs = soup.find_all("div", {"class": "resp-tab-content"})

audios = []
index = 0
for block_div in block_divs:
    audio_tables = block_div.find_all("table", {"class": "wikitable"})
    for audio_div in audio_tables:
        # print(audio_div)
        # continue
        audio_addr = audio_div.tbody.find_all("tr")[2].find_all("td")[0].div.attrs["data-src"]
        audio_text = audio_div.tbody.find_all("tr")[3].td.find_all("div")[0].get_text().strip()
        print(audio_text, audio_addr.split(".")[-1])
        if audio_addr.endswith("mp3") or audio_addr.endswith("ogg"):
            print(index, audio_text, audio_addr)
            audios.append({
                "index": index,
                "audio_text": audio_text,
                "audio_addr": audio_addr,
                "audio_suffix": audio_addr.split(".")[-1]
            })
            index += 1


if not os.path.exists(tag):
    os.mkdir(tag)

if not os.path.exists(f"{tag}/audios"):
    os.mkdir(f"{tag}/audios")

for au in audios:   # 下载音频
    rsp = requests.get(au["audio_addr"])
    suffix = au["audio_suffix"]
    with open(f"{tag}/audios/{au['index']}.{suffix}", "wb") as f:
        f.write(rsp.content)

with open(f"{tag}/info.json", "w", encoding="utf8") as f:
    json.dump(audios, f, ensure_ascii=False)



# resp = requests.get("https://patchwiki.biligame.com/images/ys/3/3f/73ne3fbhw4emno2z3ss6wf7zjdmpph9.mp3")
# with open("1.mp3", "wb") as f:
#     f.write(resp.content)
