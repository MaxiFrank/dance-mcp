"""
Spotify PKCE Oauth module that fetches the access token the
application needs to order to access the user's Spotify account
on their behalf.
"""

import base64
import hashlib
import json
import os
from urllib.parse import urlencode
import secrets
import string

from dotenv import load_dotenv
from flask import Flask, redirect, request
import requests

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_REDIRECT_URL = "http://127.0.0.1:8080/callback"
SCOPE = "user-read-private user-read-email"
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"


def generate_random_string(length=64) -> str:
    """
    input: int
    should be between 43 and 128
    """
    possible = string.ascii_letters + string.digits
    # get binary data
    values = secrets.token_bytes(length)
    # converts bytes to strings
    code_verifier = "".join(possible[b % len(possible)] for b in values)
    return code_verifier


def generate_code_challenge(code_verifier):
    """
    Generate code challenge using code_verifier as part of the query in the url
    sent to the Spotify authentication server.
    """
    bytes_data = code_verifier.encode("utf-8")
    hashed_object = hashlib.sha256(bytes_data)
    hash_bytes: bytes = hashed_object.digest()
    b64 = base64.b64encode(hash_bytes).decode("utf-8")
    # need url safe string as code challenges are sent in URL query parameters
    b64url = b64.replace("+", "-").replace("/", "_").rstrip("=")
    return b64url


def request_user_auth(client_id, code_challenge):
    """
    Should return a url with query parameters
    """
    params = {
        "response_type": "code",
        "client_id": client_id,
        "scope": SCOPE,
        "code_challenge_method": "S256",
        "code_challenge": code_challenge,
        "redirect_uri": SPOTIFY_REDIRECT_URL,
    }
    query_string = urlencode(params)
    auth_url = f"{SPOTIFY_AUTH_URL}?{query_string}"

    return auth_url


def request_access_token(code, code_verifier):
    """
    Send requst to spotify token API to get token and relevant data
    note that the actual sending post request is handled by Flask for now
    """
    payload = {
        "client_id": SPOTIFY_CLIENT_ID,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": SPOTIFY_REDIRECT_URL,
        "code_verifier": code_verifier,
    }
    response = requests.post(
        url=SPOTIFY_TOKEN_URL,
        data=payload,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=30,
    )

    # TODO: Need to throw exception if response isn't 200
    return response.json()


def get_valid_access_token():
    """
    Retrieves access token after the user logged in.
    """
    # TODO: throw error if file not here
    with open(".spotify_oauth.json", "r", encoding="utf-8") as f:
        stored_data = json.load(f)
        access_token = stored_data.get("access_token")
    return access_token


app = Flask(__name__)


@app.route("/auth")
def authenticate():
    """
    Start PKCE OAuth - generate code challenge and send to Spotify auth server
    """
    code_verifier = generate_random_string()
    code_challenge = generate_code_challenge(code_verifier)
    # Likely won't need the code_verifier in the future
    with open(".spotify_code_verifier.json", "w", encoding="utf-8") as f:
        json.dump({"code_verifier": code_verifier}, f)
    auth_url = request_user_auth(SPOTIFY_CLIENT_ID, code_challenge=code_challenge)
    return redirect(auth_url)


@app.route("/callback")
def spotify_callback():
    """
    Handle spotify call back the should give me the code and status
    """
    data = {}
    code = request.args.get("code")
    data["code"] = code
    data["client_id"] = SPOTIFY_CLIENT_ID
    # if error exists and I don't get the code, need to retry at some point
    if not code:
        error = request.args.get("error")
        return error
    # TODO: add exception if file doesn't exist or if key doesn't exist
    with open(".spotify_code_verifier.json", "r", encoding="utf-8") as f:
        stored_data = json.load(f)
        code_verifier = stored_data.get("code_verifier")
    token = request_access_token(code, code_verifier)

    if token:
        data["access_token"] = token["access_token"]
        data["token_type"] = token["token_type"]
        data["expires_in"] = token["expires_in"]
        data["refresh_token"] = token["refresh_token"]
        data["scope"] = token["scope"]

        with open(".spotify_oauth.json", "w", encoding="utf-8") as f:
            json.dump(data, f)
        # TODO: need to track time out so I can make a new request if need be
        return "Your request for access token is successful"
    return "You did not get a token from Spotify"


if __name__ == "__main__":
    # add /auth to path
    app.run(host="127.0.0.1", port=8080, debug=True)
