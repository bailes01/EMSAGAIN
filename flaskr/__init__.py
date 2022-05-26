# importing the required libraries
from SizeCounterEMS import convert
from tkinter import messagebox
import time
import glob
import os
import shutil
from flask import (
    Flask,
    redirect,
    render_template,
    request,
    send_file,
    send_from_directory,
    after_this_request,
)

from werkzeug.utils import secure_filename
import os

upload_file_path = ""
short_upload_file_path = ""


def check_is_csv(filename):
    return "." in filename and filename.rsplit(".", 1)[1] == "csv"


def create_app(test_config=None):
    # create and configure the app

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    short_upload_file_path = ""
    upload_folder = "uploads/"
    if not os.path.exists(upload_folder):
        os.mkdir(upload_folder)

    app.config["UPLOAD_FOLDER"] = upload_folder

    # a simple page that says hello
    @app.route("/")
    def upload_file():
        list_of_files = glob.glob(
            "C:/programming/python/EMSAGAIN/processed/*"
        )  # * means all if need specific format then *.csv
        if list_of_files != []:
            latest_file_processed = max(list_of_files, key=os.path.getctime).replace(
                "\\", "/"
            )
            os.remove(latest_file_processed)
        return render_template("upload.html")

    @app.route("/uploaded", methods=["GET", "POST"])
    def uploadfile():
        if request.method == "POST":  # check if the method is post
            f = request.files["file"]  # get the file from the files object
            # Saving the file in the required destination
            if check_is_csv(f.filename):
                short_upload_file_path = f.filename
                upload_file_path = os.path.join(
                    app.config["UPLOAD_FOLDER"], secure_filename(f.filename)
                )
                f.save(upload_file_path)  # this will secure the file
                return redirect("/processing")
                # Display thsi message after uploading
            else:
                return messagebox.showerror("Error", "Please upload a csv file")

    @app.route("/processing", methods=["GET", "POST"])
    def processing():
        list_of_files = glob.glob(
            "C:/programming/python/EMSAGAIN/uploads/*"
        )  # * means all if need specific format then *.csv
        src = max(list_of_files, key=os.path.getctime).replace("\\", "/")

        dst = "C:/programming/python/EMSAGAIN/processed/"

        convert([src, dst])
        # shutil.copyfile(src, dst)
        return redirect("/download")

    @app.route("/download", methods=["GET", "POST"])
    def download_():
        return render_template("download.html")

    @app.route("/dl", methods=["GET", "POST"])
    def dl():
        list_of_files = glob.glob(
            "C:/programming/python/EMSAGAIN/uploads/*"
        )  # * means all if need specific format then *.csv
        latest_file_uploaded = max(list_of_files, key=os.path.getctime).replace(
            "\\", "/"
        )
        os.remove(latest_file_uploaded)
        list_of_files = glob.glob(
            "C:/programming/python/EMSAGAIN/processed/*"
        )  # * means all if need specific format then *.csv
        latest_file_processed = max(list_of_files, key=os.path.getctime).replace(
            "\\", "/"
        )
        return send_file(str(latest_file_processed), as_attachment=False)

    return app
