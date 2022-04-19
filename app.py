import streamlit as st
import helper
import preprocessor
import matplotlib.pyplot as plt
import seaborn as sns
st.sidebar.title("Whatsapp chat analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a whatsapp chat file")
if uploaded_file is not None:
    byte_data = uploaded_file.getvalue()
    data = byte_data.decode("utf-8")
    df = preprocessor.preprocessor(data)
    # st.dataframe(df[df['message_detail'] == "<Media omitted>\n"])
    # fetch unique users

    user = df['user'].unique().tolist()
    user.sort(reverse=True)
    user.insert(0,"Overall")
    selected_user = st.sidebar.selectbox(
     'select user',
     (user))
    total_message = helper.helper(selected_user,df)
    total_words = helper.get_words(selected_user,df)
    total_media = helper.get_media(selected_user, df)
    total_url = helper.get_url(selected_user,df)

    if st.sidebar.button("show analysis"):
        st.title("Top statistic")
        col1,col2,col3,col4 = st.columns(4)
        with col1:
            col1.header("Total messages")
            col1.title(total_message)
        with col2:
            col2.header("Total words")
            col2.title(total_words)
        with col3:
            col3.header("Media shared")
            col3.title(total_media)
        with col4:
            col4.header("Shared Link")
            col4.title(total_url)

    time_df = helper.get_timeline(selected_user, df)
    st.title("Monthly Timeline")

    fig, ax = plt.subplots()
    ax.plot(time_df['time'], time_df['message_detail'],color="green")
    plt.xticks(rotation="vertical")
    plt.ylabel("Count of messages")
    st.pyplot(fig)

    st.title("Daily timeline")
    daily_df = helper.get_daily_timeline(selected_user,df)
    fig,ax = plt.subplots()
    ax.plot(daily_df['date'],daily_df['message_detail'],color="blue")
    plt.xticks(rotation="vertical")
    plt.ylabel("Count of messages")
    st.pyplot(fig)

    st.title("Activity Map")

    col1,col2 = st.columns(2)
    with col1:
        st.title("Most busy day")
        busy_day = helper.get_busy_day(selected_user,df)
        fig, ax = plt.subplots()
        ax.bar(busy_day["index"], busy_day["day_name"], color="blue")
        plt.xticks(rotation="vertical")
        plt.ylabel("Count of messages")
        st.pyplot(fig)
    # st.dataframe(busy_day)
    with col2:
        st.title("Most busy Month")
        busy_month = helper.get_busy_month(selected_user,df)
        fig, ax = plt.subplots()
        ax.bar(busy_month["index"], busy_month["month"], color="orange")
        plt.xticks(rotation="vertical")
        plt.ylabel("Count of messages")
        st.pyplot(fig)
    st.title("Weekly activity map")
    user_heatmap = helper.activity_heatmap(selected_user,df)
    fig,ax = plt.subplots()
    ax = sns.heatmap(user_heatmap)
    st.pyplot(fig)


    if selected_user == "Overall":
        st.title("Most busy user")
        x,new_df = helper.get_busy(df)
        y_axis = x.index[::-1]
        x_axis = x.values[::-1]

        fig , ax = plt.subplots()
        col1 , col2 = st.columns(2)
        with col1:
            ax.barh(y_axis,x_axis,color="red")
            st.pyplot(fig)
        with col2:
            st.dataframe(new_df)

    st.title("Wordcloud of Chat")
    wc = helper.word_colud(selected_user,df)
    fig, ax = plt.subplots()
    ax.imshow(wc)
    st.pyplot(fig)
    st.title("Most common word")
    most_comman_word = helper.most_comman_word(selected_user,df)
    # st.dataframe(most_comman_word)

    fig , ax = plt.subplots()
    ax.barh(most_comman_word['Word'],most_comman_word['Count'])
    ax.set_xlabel("frequency")
    st.pyplot(fig)

    #  get the emoji

    get_emoji = helper.get_emoji(selected_user,df)
    if get_emoji.shape[0] > 0:
        st.title("Most common emojis")
        st.table(get_emoji[:20].rename(columns={0:"Emoji",1:"Count"}))






