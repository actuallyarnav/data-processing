import os

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    session,
)

from config import UPLOAD_FOLDER
from services.db_utils import update_db
from services.file_utils import save_file
from services.processing import analyze_columns

upload_bp = Blueprint("upload", __name__)


@upload_bp.route("/", methods=["GET"])
def home():
    return render_template("home.html")


@upload_bp.route("/upload", methods=["POST"])
def upload():
    filename = save_file(request.files.get("file"), current_app.config["UPLOAD_FOLDER"])

    if not filename:
        flash("Invalid CSV file", "warning")
        return redirect("/")

    path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)

    # store in session
    session["filename"] = filename
    session["columns"] = analyze_columns(path)
    update_db(filename)

    flash("CSV uploaded!", "success")
    return redirect("/analyze")
