### Modules ###

import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory

# App
app = Flask(__name__)

## Image will be saved here temporarily
LOCAL_IMAGE = "local_image"

# Set the directory to an environment variable
app.config["LOCAL_IMAGE"] = "local_image"

# Create local directory
os.makedirs(LOCAL_IMAGE, exist_ok=True)

# Home Page
@app.route("/")
def home_page():
    return render_template("index.html", file=None)

# Home Page
@app.route("/<filename>")
def home_page_filename(filename):
    return render_template("index.html", file=filename)

# Get uploaded file and save it to local
@app.route("/upload_image", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        file = request.files["file"]
        filepath = os.path.join(app.config["LOCAL_IMAGE"], file.filename)
        file.save(filepath)
        

    return redirect(url_for('home_page_filename', filename=file.filename))


# Retrieves an image from local directory to be displayed
@app.route("/retrieve_image/<filename>")
def retrieve_image(filename):
    print(f"File name: {filename}")
    return send_from_directory(app.config["LOCAL_IMAGE"], filename)

# Run 
if __name__ == '__main__':
    app.run(debug=True) # Don't use 'Debug=True in production'