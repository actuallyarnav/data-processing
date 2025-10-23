from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
from dotenv import load_dotenv
import os

from werkzeug.utils import secure_filename
from processing import process_csv 
load_dotenv()
UPLOAD_FOLDER='./static/uploads/'
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1000 * 1000
app.secret_key =  os.getenv("SECRET_KEY")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('home.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    if not file or file.filename == '':
        flash("Please upload a valid CSV file", "warning")
        return redirect('/')

    if not allowed_file(file.filename):
        flash("Allowed file type: CSV only", "warning")
        return redirect('/')

    filename = secure_filename(file.filename)
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(path)
    summary_html = process_csv(path)

    return render_template('summary.html', summary=summary_html, filename=filename)


@app.route('/about', methods=['POST', 'GET'])
def about():
    return render_template('about.html')
if __name__ == "__main__":
    app.run(port=8080, debug=True)