import streamlit as st
import pandas as pd
import plotly.express as px
import duckdb
from streamlit_option_menu import option_menu

# Load custom CSS for futuristic styling
def load_css():
    st.markdown("""
    <style>
    body {
        background-color: #0e0e0e;
        color: #fff;
        font-family: 'Roboto', sans-serif;
    }
    .sidebar .sidebar-content {
        background-color: #1a1a1a;
    }
    .stButton>button {
        background-color: #1f77b4;
        color: white;
        border-radius: 8px;
        font-size: 16px;
        padding: 8px 20px;
    }
    .stButton>button:hover {
        background-color: #ff6600;
        color: white;
    }
    .stTextInput>div>div>input {
        background-color: #2b2b2b;
        color: white;
    }
    .stMarkdown {
        color: #8ab4f8;
    }
    .stDataFrame {
        background-color: #1e1e1e;
        color: white;
    }
    .st-expander>div>div>div {
        background-color: #1e1e1e;
    }
    .stMetric {
        background-color: #1e1e1e;
        border-radius: 10px;
        padding: 10px;
    }
    .plotly-chart {
        background-color: #0e0e0e;
    }
    .css-1r6slb0 {
        background-color: #1a1a1a;
    }
    .css-1adrfps {
        background-color: #1a1a1a;
    }
    .css-v7itv9 {
        background-color: #1a1a1a;
    }
    </style>
    """, unsafe_allow_html=True)

load_css()

# Sidebar menu
with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["Home", "Data Analysis", "Review", "Contact Us"],
        icons=["house", "bar-chart", "star", "envelope"],
        menu_icon="cast",
        default_index=0,
    )

if selected == "Home":
    st.title("Telegram Dashboard")
    st.markdown("TelegramTrends v1")
    t1, t2 = st.columns((0.09, 0.75))

    t1.image('logo.png', width=160)
    t2.title("Dashboard Data - Telegram Report")
    t2.markdown("Website: **https://telegramtrends.xyz/**")

    st.header("Welcome to the Telegram Dashboard")
    st.write("Use the sidebar to navigate to different sections of the dashboard.")

if selected == "Data Analysis":
    st.title("Data Analysis")
    st.markdown("### Upload your Telegram data files for analysis")

    @st.cache_data
    def load_data(files):
        data_list = []
        for file in files:
            if file.name.endswith('.csv'):
                data = pd.read_csv(file)
            elif file.name.endswith('.xlsx'):
                data = pd.read_excel(file)
            else:
                st.error('Unsupported file type: ' + file.name)
                return None
            data_list.append(data)
        combined_data = pd.concat(data_list, ignore_index=True)
        return combined_data

    uploaded_files = st.sidebar.file_uploader("Choose files", accept_multiple_files=True)

    if uploaded_files:
        st.info("Uploaded files through config")
        df = load_data(uploaded_files)
        if df is not None:
            st.dataframe(df.head())  # Display the first few rows of the dataframe

            with st.expander("Data Preview"):
                st.write("Data preview is shown here")
                st.dataframe(df.head(100))  # Display only the first 100 rows

            # Display column names for debugging
            st.markdown("""
                <div style="padding: 10px; border: 1px solid #2d9cdb; border-radius: 5px;">
                    <span style="color: #2d9cdb;">Columns in the dataset: {}</span>
                </div>
            """.format(', '.join(df.columns.tolist())), unsafe_allow_html=True)

            # Simple text analysis on the Message column
            def plot_text_analysis():
                query = """
                SELECT
                    COUNT(*) as Total_Messages,
                    AVG(LENGTH(Message)) as Avg_Message_Length
                FROM df
                """
                message_data = duckdb.query(query).df()
                st.dataframe(message_data)

            plot_text_analysis()

            def plot_message_lengths():
                query = """
                SELECT
                    LENGTH(Message) as Message_Length
                FROM df
                """
                message_lengths = duckdb.query(query).df()

                fig1 = px.histogram(message_lengths, x="Message_Length", color_discrete_sequence=['#2d9cdb'])
                fig1.update_layout(margin=dict(l=0, r=0, t=30, b=0), title='Histogram of Message Lengths')
                fig1.update_xaxes(range=[0, 500])

                fig2 = px.histogram(message_lengths, x="Message_Length", nbins=50, color_discrete_sequence=['#00b3ff'])
                fig2.update_layout(margin=dict(l=0, r=0, t=30, b=0), title='Histogram of Message Lengths with More Bins')
                fig2.update_xaxes(range=[0, 600])

                with st.container():
                    st.plotly_chart(fig1)
                    st.plotly_chart(fig2)

            plot_message_lengths()

            def plot_word_count():
                query = """
                SELECT
                    SUM(LENGTH(Message) - LENGTH(REPLACE(Message, ' ', '')) + 1) as Total_Words
                FROM df
                """
                word_count_data = duckdb.query(query).df()
                st.dataframe(word_count_data)

            plot_word_count()

            # Example Metrics and Charts
            st.subheader("Metrics")
            m1, m2, m3 = st.columns(3)

            total_messages = len(df)
            avg_message_length = df['Message'].dropna().apply(lambda x: len(str(x))).mean()

            m1.metric(label='Total Messages', value=total_messages)
            m2.metric(label='Avg Message Length', value=f"{avg_message_length:.2f} characters")

            # Example bar chart for message counts by hour (if timestamp is available)
            if 'Timestamp' in df.columns:
                df['Timestamp'] = pd.to_datetime(df['Timestamp'])
                df['Hour'] = df['Timestamp'].dt.hour
                hourly_counts = df.groupby('Hour').size().reset_index(name='Counts')

                fig = px.bar(hourly_counts, x='Hour', y='Counts', title='Messages by Hour')
                fig.update_layout(margin=dict(l=0, r=0, t=30, b=0))
                st.plotly_chart(fig)

            # Charts for Top Messages by Length
            st.subheader("Top Messages by Length")
            filtered_df = df[df['Sender Name'] != 'Unknown']
            top_messages = filtered_df.assign(Message_Length=filtered_df['Message'].apply(lambda x: len(str(x)))).nlargest(5, 'Message_Length')[['Dialog ID', 'Dialog Name', 'Sender Name', 'Message', 'Message_Length']]

            with st.container():
                fig_pie = px.pie(top_messages, names='Sender Name', values='Message_Length', title='Top 5 Messages by Length - Pie Chart', color_discrete_sequence=px.colors.cyclical.HSV)
                st.plotly_chart(fig_pie)

                fig_line = px.line(top_messages, x='Sender Name', y='Message_Length', markers=True, title='Top 5 Messages by Length - Line Graph')
                st.plotly_chart(fig_line)

                fig_scatter = px.scatter(top_messages, x='Sender Name', y='Message_Length', size='Message_Length', color='Sender Name', title='Top 5 Messages by Length - Scatter Plot')
                st.plotly_chart(fig_scatter)

            # Convert 'Message' to string and calculate 'Message_Length'
            df['Message_Length'] = df['Message'].astype(str).apply(len)

            # Group by 'Sender Name' and calculate total message length
            grouped_messages = df.groupby('Sender Name')['Message_Length'].sum().reset_index()

            # Sort by 'Message_Length' in descending order and take the top 5
            top_senders = grouped_messages.sort_values('Message_Length', ascending=False).head(5)

            color_palette = ['#2d9cdb', '#00ffff', '#ffd500']

            with st.container():
                fig_pie = px.pie(top_senders, names='Sender Name', values='Message_Length', title='Top 5 Senders by Message Length - Pie Chart', color_discrete_sequence=color_palette)
                st.plotly_chart(fig_pie)

                fig_line = px.line(top_senders, x='Sender Name', y='Message_Length', markers=True, title='Top 5 Senders by Message Length - Line Graph', color_discrete_sequence=color_palette)
                st.plotly_chart(fig_line)

                color_scale = [[0, '#2d9cdb'], [0.5, '#00b3ff'], [1, '#ffd500']]

                fig_scatter = px.scatter(top_senders, x='Sender Name', y='Message_Length', size='Message_Length', color='Sender Name', title='Top 5 Senders by Message Length - Scatter Plot', color_continuous_scale=color_scale)
                st.plotly_chart(fig_scatter)

if selected == "Contact Us":
    st.title("Contact Us")
    st.subheader("We'd love to hear from you!")
    st.markdown("For any queries or feedback, please contact us at: support@telegramtrends.xyz")
    st.markdown("You can also follow us on our social media channels for the latest updates.")

