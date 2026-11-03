import os

from flask import render_template, redirect, request, session, abort

from flask_app import app
from flask_app.config.db import db_enabled
from flask_app.models.nate import Nate


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/info")
def inf():
    # Lists every comment, so it's protected: visit /info?key=<ADMIN_KEY>
    admin_key = os.environ.get("ADMIN_KEY")
    if not admin_key or request.args.get("key") != admin_key or not db_enabled():
        abort(404)
    users = Nate.get_all()
    return render_template("info.html", users=users)


@app.route("/new", methods=["POST"])
def addInfo():
    if not db_enabled():
        return redirect("/?comments=off#contact")
    data = {
        "fname": request.form.get("fname", "").strip()[:100],
        "lname": request.form.get("lname", "").strip()[:100],
        "email": request.form.get("email", "").strip()[:255],
        "comment": request.form.get("comment", "").strip()[:5000],
    }
    if not all(data.values()):
        return redirect("/#contact")
    comment_id = Nate.save(data)
    session["last_comment_id"] = comment_id
    return redirect(f"/one/{comment_id}")


@app.route("/one/<int:user_id>")
def addOne(user_id):
    # Only the person who just submitted can see their own comment.
    if session.get("last_comment_id") != user_id:
        abort(404)
    user = Nate.get_one({"user_id": user_id})
    if user is None:
        abort(404)
    return render_template("formData.html", user=user)
