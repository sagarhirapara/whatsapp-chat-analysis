from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import regex as re
def helper(user,df):
    if user == "Overall":
        return df.shape[0]
    else:
        return df[df['user'] == user].shape[0]
def get_words(user,df):
    if user == "Overall":
        words = []
        for i in df['message_detail']:
            words.extend(i.split(" "))
        return len(words)
    else:
        words = []
        detail = df[df['user'] == user]
        for i in detail["message_detail"]:
            words.extend(i.split(" "))
        return len(words)
def get_media(user,df):
    if user == "Overall":
        num_media = df[df['message_detail'] == '<Media omitted>\n'].shape[0]
        return num_media
    else:
        detail = df[df['user'] == user]
        num_media = detail[df['message_detail'] == '<Media omitted>\n'].shape[0]
        return num_media
def get_url(user,df):
    if user == "Overall":
        extractor = URLExtract()
        count = 0
        for i in df['message_detail']:
            count += len(extractor.find_urls(i))
        return count

    else:
        detail = df[df['user'] == user]
        count = 0
        extractor = URLExtract()
        for i in detail['message_detail']:
            count += len(extractor.find_urls(i))
        return count

def get_busy(df):
    df = df[df['user'] != "Group Notification"]
    detail = round((df['user'].value_counts()/df["user"].shape[0])*100,2).reset_index().rename(columns={"index":"users","user":"percentage(%)"})
    return df['user'].value_counts().head(), detail

def word_colud(user,df):
    if user != "Overall":
        df = df[df['user'] == user]
    wc = WordCloud(background_color="white",height=200,width=200,max_font_size=25,max_words=40)
    return wc.generate(df['message_detail'].str.cat(sep=" "))

def most_comman_word(user,df):
    if user != "Overall":
        df = df[df['user']==user]

    temp = df[df['user'] != "Group Notification"]
    temp = temp[temp['message_detail'] != "<Media omitted>\n"]

    f = open("stop_word.txt", 'r')
    x = f.read()

    words = []
    for i in temp['message_detail']:
        for j in i.lower().split():
            if j not in x:
                words.append(j)

    x = Counter(words)
    return pd.DataFrame(x.most_common(20)).rename(columns={0: "Word", 1: "Count"})

def get_emoji(user,df):
    if user != "Overall":
        df = df[df['user']==user]
    emo = []
    punc = r'''`~!@#$%*()“’₹🇳🇮⋅“ ’×।_^&–+={}>♀?"/'＼：／|\[]♂-:｜;”‘<,.'''
    for i in df["message_detail"]:
        t = ""
        for ele in i:
            if ele not in punc:
                t += ele.lower()
        x = re.findall(r'[^\w\s]',t)
        emo.extend(x)

    return pd.DataFrame(Counter(emo).most_common(len(Counter(emo))))
def get_timeline(user,df):
    if user != "Overall":
        df = df[df['user']==user]

    timeline = df.groupby(['year', "month_num", 'month']).count()['message_detail'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(str(timeline['month'][i]) + "-" + str(timeline['year'][i]))
    timeline['time'] = time

    return timeline

def get_daily_timeline(user,df):
    if user != "Overall":
        df = df[df['user'] == user]

    timeline = df.groupby(['date']).count()['message_detail'].reset_index()
    return timeline

def get_busy_day(user,df):
    if user != "Overall":
        df = df[df['user'] == user]

    return df['day_name'].value_counts().reset_index()

def get_busy_month(user,df):
    if user != "Overall":
        df = df[df['user'] == user]

    return df['month'].value_counts().reset_index()

def activity_heatmap(user,df):
    if user != "Overall":
        df = df[df['user'] == user]
    user_heatmap = df.pivot_table(index="day_name",columns='period',values="message_detail",aggfunc="count").fillna(0)
    return user_heatmap

