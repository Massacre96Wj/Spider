import stylecloud
from IPython.display import Image

with open("yy.txt", "r", encoding="utf-8") as f:
    content = f.read()
    stylecloud.gen_stylecloud(text=content, max_words=600,
                              collocations=False,
                              font_path="SIMLI.TTF",
                              icon_name="fas fa-heartbeat",
                              size=800,
                              output_name="yy.png")
    Image(filename="yy.png")