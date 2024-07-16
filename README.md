# Telegram Dashboard

This Streamlit application provides an interactive dashboard to analyze Telegram and Twitter data. It allows users to upload data files, perform text analysis, and visualize the results.

## Features

- Sidebar navigation with options for Home, Data Analysis, Twitter Analysis, Contact Us, and Sentiment Analysis.
- Upload and analyze Telegram data files (CSV and Excel formats).
- Display data from uploaded files and perform basic text analysis.
- Visualize message statistics and lengths with interactive charts.
- Analyze and display Twitter data from a CSV file.
- Contact page for user support and feedback.
- accepts file size upto 500 MB

## Requirements

- Python 3.7+
- Streamlit
- Pandas
- Plotly
- DuckDB
- Streamlit Option Menu

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/telegram-dashboard.git
    cd telegram-dashboard
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the Streamlit app:
    ```bash
    streamlit run app.py
    ```

2. Use the sidebar to navigate between different sections of the dashboard:
    - **Home**: Overview of the dashboard.
    - **Data Analysis**: Upload Telegram data files for analysis and visualization.
    - **Twitter Analysis**: Display and analyze Twitter data from a CSV file.
    - **Contact Us**: Contact information and support.

## Data Analysis

- **Upload Files**: Upload multiple CSV or Excel files for analysis.
- **Data Preview**: View the first 100 rows of the uploaded data.
- **Message Statistics**: Bar charts for total messages and average message length.
- **Message Lengths**: Histograms of message lengths.
- **Word Count**: Total words in messages.
- **Top Messages by Length**: Visualize top messages by length using pie charts, line graphs, and scatter plots.
- **Top Senders by Message Length**: Visualize top senders by message length using pie charts, line graphs, and scatter plots.

## Contact Us

For any queries or feedback, please contact us at: [support@telegramtrends.xyz](mailto:support@telegramtrends.xyz)

Follow us on our social media channels for the latest updates.

## License

This project is licensed under the MIT License.

## Acknowledgements

- [Streamlit](https://www.streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [Plotly](https://plotly.com/)
- [DuckDB](https://duckdb.org/)
- [Streamlit Option Menu](https://github.com/victoryhb/streamlit-option-menu)
