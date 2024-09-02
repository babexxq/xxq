from wordcloud import WordCloud
import pandas as pd
from PIL import Image
import numpy
import jieba
import re # re用于正则表达式处理
from collections import Counter # Counter用于计数
import matplotlib.pyplot as plt

def get_wordcloud(data_path,save_path,is_send):
    # 读文件
    df = pd.read_excel(data_path)
    if is_send==2:
        texts = [str(text) for text in df['content_new'].to_list()]       
    else:
        texts = [str(text) for text in df[df['isSend'] == is_send]['content_new'].to_list()]

    with open("data/CNstopwords.txt",'r',encoding='utf-8') as f:
        lines = f.readlines()
        stopwords = [line.strip().replace("\ufeff","") for line in lines]
        stopwords.extend(["OKOK","xxxx"])

    # 使用jieba对消息内容进行分词，并根据定义的停用词表和正则表达式删除表情符号和特定字符（表情都是这样的格式：[xx]）
    norm_texts = []
    pattern_emoji = re.compile("(\[.+?\])")
    pattern_num = re.compile(r"\d+")
    '''
    - \[：这是一个转义字符，用于匹配左方括号 [。因为方括号在正则表达式中有特殊含义，所以需要用\进行转义，以匹配文字中的实际方括号字符。
    - .+?：.表示匹配除换行符外的任意字符，+表示匹配前面的模式一次或多次，?表示匹配模式0次或1次，尽可能少地匹配。
    - 这个组合.+?表示匹配任意字符，但尽可能少地匹配，直到下一个部分匹配。
    '''
    for text in texts:
        text = pattern_emoji.sub('', text).replace("\n","")
        '''
        使用pattern_emoji.sub('', text)将文本中匹配正则表达式pattern_emoji的部分替换为空字符串
        然后使用.replace("\n","")将剩余的文本中的换行符替换为空字符串。这样可以删除文本中的表情符号（如[笑脸]）和换行符。
        '''
        text = pattern_num.sub('', text).replace("\n","")
        words = jieba.lcut(text) # 使用jieba分词
        res = [word for word in words if word not in stopwords and word.replace(" ","")!="" and len(word)>1]
        if res!=[]:
            norm_texts.extend(res)

    count_dict = dict(Counter(norm_texts))
    mask_image = numpy.array(Image.open("data/wordcloud_mask.png"))
    wc = WordCloud(
                #    width=2560,
                #    height=1440, # 自定义mask后，图片尺寸取决于mask
                   font_path="data/汉仪雅酷黑55W.ttf", 
                   background_color='rgba(255, 255, 255, 0)', 
                   colormap='tab20b',
                   mask=mask_image,
                   scale=2, # 增大以提高分辨率，倍数增加
                   random_state=0
                   )
    wc = wc.fit_words(count_dict)
    plt.imshow(wc)
    plt.show()
    wc.to_file(save_path)

if __name__=='__main__':
    get_wordcloud("data/wordcloud.xlsx",save_path="result/词云-对方发送.png",is_send=0)
    get_wordcloud("data/wordcloud.xlsx",save_path="result/词云-自己发送.png",is_send=1)
    get_wordcloud("data/wordcloud.xlsx",save_path="result/词云-共同.png",is_send=2)
