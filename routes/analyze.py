from flask import Blueprint, flash, redirect, render_template, session

analyze_bp = Blueprint("analyze", __name__)


@analyze_bp.route("/analyze", methods=["GET"])
def analyze():
    if "filename" not in session:
        flash("Please upload a dataset first", "warning")
        return redirect("/")

    return render_template(
        "analyze.html", filename=session["filename"], columns=session["columns"]
    )
