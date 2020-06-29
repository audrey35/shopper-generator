from flask import Flask, render_template, request, redirect, url_for, flash, abort, session, jsonify
import json
import os.path
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "h4323dfgd23sdffgs343dfg"


@app.route('/')
def home():
    # can display an html rather than a long string
    # can pass a variable to be used in the html
    return render_template("home.html", name="Audrey", codes=session.keys())


@app.route("/about")
def about():
    # string can be displayed in the about page
    return "This is a URL shortener."


@app.route("/your-url", methods=["GET", "POST"])
def your_url():
    if request.method == "POST":
        urls = {}

        if os.path.exists("urls.json"):
            with open("urls.json", "r") as urls_file:
                urls = json.load(urls_file)

        if request.form["code"] in urls.keys():
            flash("That short name has already been taken. Please select another name.")
            return redirect(url_for("home"))

        if "url" in request.form.keys():
            urls[request.form["code"]] = {"url": request.form["url"]}
        else:
            f = request.files["file"]
            full_name = request.form["code"] + secure_filename(f.filename)
            f.save("/Users/audrey/PycharmProjects/5500Project/flasktutorial/static/user_files/" + full_name)
            urls[request.form["code"]] = {"file": full_name}

        with open("urls.json", "w") as url_file:
            json.dump(urls, url_file)
            session[request.form["code"]] = True
        return render_template("your_url.html", code=request.form["code"])
    return redirect(url_for("home"))


@app.route("/<string:code>")  # look for a string after the slash and store it in a variable called code
def redirect_to_url(code):  # code variable created above gets passed in as param
    if os.path.exists("urls.json"):
        with open("urls.json", "r") as urls_file:
            urls = json.load(urls_file)
            if code in urls.keys():
                if "url" in urls[code].keys():
                    return redirect(urls[code]["url"])
                return redirect(url_for("static", filename="user_files/" + urls[code]["file"]))
    return abort(404)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("page_not_found.html"), 404

@app.route("/api")
def session_api():
    return jsonify(list(session.keys()))
