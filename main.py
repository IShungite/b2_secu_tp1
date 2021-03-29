from flask import Flask, render_template, request, redirect

app = Flask(__name__)
app.secret_key = "oizeffazFEZIHfezz"
app.debug = True

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "py"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    try:
        file = request.files["inputFile"]
        if file.filename == "":
            return "No input"
        if file and not allowed_file(file.filename):
            return "Bad format"
        file.save(f"static/images/{file.filename}")
        return f"Image sended static/images/{file.filename}"
    except Exception as e:
        return f"Error while sending file: {e}"
