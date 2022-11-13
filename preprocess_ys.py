import argparse
import text
from utils import load_filepaths_and_text
import os
import json



tag = "胡桃"

if not os.path.exists(f"test/{tag}"):
    os.mkdir(f"test/{tag}")

out = ''

with open(f"YSAudio/{tag}/info.json", "r", encoding="utf-8") as f:
    audios = json.load(f)
    for audio in audios:
        print(audio)
        cleaned_text = text._clean_text(audio["audio_text"], ["chinese_cleaners1"])
        print(cleaned_text)
        if not os.path.exists(f"test/{tag}/{audio['index']}.wav"):
            cmd = f"ffmpeg -i YSAudio/{tag}/audios/{audio['index']}.{audio['audio_suffix']} -ac 1 -ar 16000 test/{tag}/{audio['index']}.wav"
            os.system(cmd)
            print(cmd)
        # if (len(cleaned_text.split(" ")) > 5) and (len(cleaned_text.split(" ")) < 20):
        out += f"./test/{tag}/{audio['index']}.wav|{cleaned_text}\n"


with open(f"test/{tag}.txt.2.cleaned", "w", encoding="utf-8") as f:
    f.write(out)





exit()
if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("--out_extension", default="cleaned")
  parser.add_argument("--text_index", default=1, type=int)
  parser.add_argument("--filelists", nargs="+", default=["filelists/ljs_audio_text_val_filelist.txt", "filelists/ljs_audio_text_test_filelist.txt"])
  parser.add_argument("--text_cleaners", nargs="+", default=["chinese_cleaners1"])   # english_cleaners2

  args = parser.parse_args()
    

  for filelist in args.filelists:
    print("START:", filelist)
    filepaths_and_text = load_filepaths_and_text(filelist)
    for i in range(len(filepaths_and_text)):
      original_text = filepaths_and_text[i][args.text_index]
      cleaned_text = text._clean_text(original_text, args.text_cleaners)
      filepaths_and_text[i][args.text_index] = cleaned_text

    new_filelist = filelist + "." + args.out_extension
    with open(new_filelist, "w", encoding="utf-8") as f:
      f.writelines(["|".join(x) + "\n" for x in filepaths_and_text])
