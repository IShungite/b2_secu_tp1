from flask import Flask, render_template, request
import io
import zipfile
import os
import config.config


app = Flask(__name__)
app.secret_key = "oizeffazFEZIHfezz"
app.debug = True


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in config.config.ALLOWED_EXTENSIONS


def unzip(zip_file, extraction_path):
    """
    code to unzip files
    """
    print("[INFO] Unzipping")
    try:
        files = []
        with zipfile.ZipFile(zip_file, "r") as z:
            for fileinfo in z.infolist():
                filename = fileinfo.filename
                dat = z.open(filename, "r")
                files.append(filename)
                outfile = os.path.join(extraction_path, filename)
                if not os.path.exists(os.path.dirname(outfile)):
                    try:
                        os.makedirs(os.path.dirname(outfile))
                    except OSError as exc:  # Guard against race condition
                        print(f"\n[WARN] OS Error: Race Condition: {exc}")
                if not outfile.endswith("/"):
                    with io.open(outfile, mode="wb") as f:
                        f.write(dat.read())
                dat.close()
        return files
    except Exception as e:
        print(f"[ERROR] Unzipping Error: {e}")


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
        file.save(f"static/{file.filename}")
        unzip(file, "static")
        return f"Image sended static/{file.filename}"
    except Exception as e:
        return f"Error while sending file: {e}"
