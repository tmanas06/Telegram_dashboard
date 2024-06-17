from flask import Flask, render_template, request, redirect, url_for
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start-streamlit')
def start_streamlit():
    subprocess.Popen(['streamlit', 'run', 'streamlit_app.py'])
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)
