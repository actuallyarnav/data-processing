# imports
from flask import Flask, render_template

from config import UPLOAD_FOLDER
from routes.analyze import analyze_bp
from routes.generate import generate_bp

# blueprint imports
from routes.upload import upload_bp
from services.db_utils import create_db, init_fill_table

# flask setup
app = Flask(__name__)
app.config.from_object("config")

# register blueprintss
app.register_blueprint(upload_bp)
app.register_blueprint(analyze_bp)
app.register_blueprint(generate_bp)

# database init
create_db()
init_fill_table(UPLOAD_FOLDER)


# misc routes that dont need their own blueprint
@app.route("/health")
def health():
    return {"status": "OK"}, 200


@app.route("/about", methods=["POST", "GET"])
def about():
    return render_template("about.html")


# main
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
