#imports
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash, session
from dotenv import load_dotenv
import os
from werkzeug.utils import secure_filename
from processing import *

#initial checks
load_dotenv()
UPLOAD_FOLDER='./static/uploads/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'csv'}

#flask setup
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
    flash("CSV uploaded!")
    column_info = analyze_columns(path)

    # store in session
    session["filename"] = filename
    session["columns"] = column_info

    return redirect(url_for("analyze"))


@app.route('/analyze', methods=['GET'])
def analyze():
    if "filename" not in session:
        flash("Please upload a dataset first", "warning")
        return redirect("/")

    return render_template("analyze.html",filename=session["filename"],columns=session["columns"])


@app.route("/generate", methods=["POST"])
def generate():
    if "filename" not in session:
        flash("Session expired. Please upload the dataset again.", "warning")
        return redirect("/")

    filename = session["filename"]
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    # user selections
    numeric_cols = request.form.getlist("numeric_cols")
    categorical_cols = request.form.getlist("categorical_cols")
    options = request.form.getlist("options")

    df = pd.read_csv(file_path)

    results = {}

    # Summary statistics
    if "summary" in options and numeric_cols:
        results["summary"] = (
            df[numeric_cols]
            .describe()
            .round(2)
            .to_html(classes="table table-striped table-bordered", border=0)
        )
    else:
        results["summary"] = "ERROR: no values selected."

    # Missing value analysis
    if "missing" in options and (numeric_cols or categorical_cols):
        missing = df[numeric_cols + categorical_cols].isna().sum()
        results["missing"] = (
            missing
            .rename("Missing Values")
            .to_frame()
            .to_html(classes="table table-striped table-bordered", border=0)
        )
    else:
        results["missing"] = "ERROR: no values selected."

    # Categorical value counts
    categorical_results = {}
    for col in categorical_cols:
        categorical_results[col] = (
            df[col]
            .value_counts()
            .to_frame("Count")
            .to_html(classes="table table-striped table-bordered", border=0)
        )

    results["categorical"] = categorical_results

    return render_template(
        "generate.html",
        filename=filename,
        results=results
    )


@app.route("/health")
def health():
    return "OK", 200

@app.route('/about', methods=['POST', 'GET'])
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)