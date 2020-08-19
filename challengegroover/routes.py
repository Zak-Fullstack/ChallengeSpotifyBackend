import requests
import json
from flask import Blueprint, redirect, request, jsonify, render_template
from .spotify_auth import SpotifyAuth


# Landing page of the app.
root = Blueprint("root", "root", url_prefix="/")

@root.route("/")
def index():
    return render_template("index.html")


# Spotify Authorization.
auth = Blueprint("auth", "auth", url_prefix="/auth")


@auth.route("/")
def get_user():
    response = SpotifyAuth().getUser()
    return redirect(response)


@auth.route("/callback")
def callback():
    code = request.values["code"]
    tokens = SpotifyAuth().getUserToken(code)
    return jsonify(tokens)


# API
api = Blueprint("api", "api", url_prefix="/api")

@api.route('/artists')
def display_artists():
    with open('challengegroover/data/data.json') as json_file:
        data = json.load(json_file)
    return data