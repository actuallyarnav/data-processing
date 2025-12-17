from flask import Blueprint, request, redirect, flash, session, current_app, render_template
import os
import pandas as pd

generate_bp = Blueprint("generate", __name__)
@generate_bp.route("/generate", methods=["POST"])
def generate():
    if "filename" not in session:
        flash("Session expired. Please upload the dataset again.", "warning")
        return redirect("/")

    filename = session["filename"]
    file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)

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

    return render_template("generate.html", filename=filename, results=results)