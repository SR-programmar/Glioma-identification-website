### Modules ###

import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session, flash
from helper import clear_dir, predict_image, valid_extension
# App
app = Flask(__name__)
app.secret_key = "12345"

## Image will be saved here temporarily
LOCAL_IMAGE = "local_image"

# Set the directory to an environment variable
app.config["LOCAL_IMAGE"] = "local_image"
# Set image result to None

# Create local directory
os.makedirs(LOCAL_IMAGE, exist_ok=True)

# Home Page
@app.route("/")
def home_page():
    session["result"] = None

    return render_template("index.html", file=None, result=session["result"])

# Home Page
@app.route("/<filename>")
def home_page_filename(filename):
    return render_template("index.html", file=filename, result=session["result"])

# Get uploaded file and save it to local
@app.route("/upload_image", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        clear_dir()
        file = request.files["file"]
        
        if file.filename == '':
            flash("No image was uploaded")
        elif not valid_extension(file.filename):
            flash("Image must be PNG or JPG format")
        else:
            print("File name is blank")
            filepath = os.path.join(app.config["LOCAL_IMAGE"], file.filename)

            file.save(filepath)
            
            prediction = predict_image()
            session["result"] = prediction

            return redirect(url_for('home_page_filename', filename=file.filename))

    return redirect(url_for("home_page"))

# Retrieves an image from local directory to be displayed
@app.route("/retrieve_image/<filename>")
def retrieve_image(filename):
    return send_from_directory(app.config["LOCAL_IMAGE"], filename)

# Run 
if __name__ == '__main__':
    app.run(debug=True) # Don't use 'Debug=True in production'