import pandas as pd
import re
def preprocessor(data):
    pattern = '\d{1,2}/\d{1,2}/\d{1,2},\s\d{1,2}:\d{1,2}\s-\s'
    dates = re.findall(pattern, data)
    messages = re.split(pattern, data)[1:]
    df = pd.DataFrame({"user_message": messages, "message_date": dates})
    df['message_date'] = pd.to_datetime(df['message_date'], format="%d/%m/%y, %H:%M - ")
    df.rename(columns={"user_message": "message"}, inplace=True)
    user = []
    message = []
    for i in df['message']:

        mes = re.split("([\w,\s]+):\s", i)
        if mes[1:]:
            user.append(mes[1])
            message.append(mes[2])
        else:
            user.append("Group Notification")
            message.append(mes[0])
    df['user'] = user
    df['message_detail'] = message
    df['year'] = df["message_date"].dt.year
    df['month'] = df['message_date'].dt.month_name()
    df['day'] = df['message_date'].dt.day
    df['hour'] = df['message_date'].dt.hour
    df['minute'] = df['message_date'].dt.minute
    df['month_num'] = df['message_date'].dt.month
    df['date'] = df['message_date'].dt.date
    df['day_name'] = df["message_date"].dt.day_name()
    df.drop(columns=["message"], inplace=True)

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str("00"))
        elif hour == 0:
            period.append(str("00") + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))
    df['period'] = period
    return df