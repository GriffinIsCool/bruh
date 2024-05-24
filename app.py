import os
import requests
import urllib.parse

# Get the environment variables
CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
REDIRECT_URI = os.environ["REDIRECT_URI"]

# The URL of Xbox Live's token endpoint
TOKEN_URL = "https://login.live.com/oauth20_token.srf"

# The URL parameters for the token request
TOKEN_PARAMS = {
    "grant_type": "authorization_code",
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "code": "", # Add the code parameter here
    "redirect_uri": REDIRECT_URI,
}

# Exchange the authorization code for an access token
def exchange_code_for_token(code):
    global TOKEN_PARAMS
    TOKEN_PARAMS["code"] = code
    response = requests.post(TOKEN_URL, data=TOKEN_PARAMS)
    return response.json()

# Handle the callback request from Xbox Live
def handle_callback(request):
    # Get the authorization code from the URL parameters
    code = urllib.parse.parse_qs(request.GET.urlencode()).get("code")[0]

    # Exchange the authorization code for an access token
    token_response = exchange_code_for_token(code)

    # Extract the access token from the response
    access_token = token_response["access_token"]

    # TODO: Store the access token securely
    print("Access token:", access_token)

    # Redirect the user to a success page
    return redirect("/success")

# Handle the success request
def handle_success(request):
    return "<html><body><h1>Success! Your Minecraft account has been verified.</h1></body></html>"

# Handle the main request
def handle_request(request):
    if request.method == "GET" and request.GET.get("state") == "STATE_VALUE":
        return handle_callback(request)
    else:
        return handle_success(request)

# Start the server
if __name__ == "__main__":
    from wsgiref.simple_server import make_server
    httpd = make_server("0.0.0.0", 80, handle_request)
    httpd.serve_forever()
