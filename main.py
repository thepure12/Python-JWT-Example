from bottle import Bottle, static_file, request
from bottle_jwt import JWTPlugin
import json
from datetime import datetime, timedelta
import random

debug = False
app = Bottle()
jwt_key = "changeme" # Changing will invalidate all current tokens
token_exp = 30 # When should the token (in seconds)

def auth(username=None, password=None):
  if debug:
    print(f"main.py: username: {username} - password: {password}")
    
  users = json.load(open("users.json")) # Load users db
  if username in users and users[username]["password"] == password:
    return { 
      "permissions": users[username]["permissions"],
      "username": username if username else "someuser",
      "exp": datetime.now() + timedelta(seconds=token_exp)
      # Add more claims
    }

# Install plugins
plugin = JWTPlugin(jwt_key, auth_func=auth, debug=debug)
app.install(plugin)

@app.route("/")
def index():
  return static_file("index.html", ".")

@app.route("/<filename>.js")
def js(filename):
  return static_file(f"{filename}.js", ".")

@app.route("/token", method=["POST"])
def token():
  # Empty function to create the token route
  # Route is handled in JWTPlugin
  pass

#------------------------------------------------------------------
# Protected routes
# Use the permissions argument to set permissions for the route
# The permissions argument is used by the JWTPlugin
#------------------------------------------------------------------

@app.route("/user", method=["GET"], permissions=["user"])
def user():
  # JWTPlugin adds a user attribute to the bottle request object 
  # and sets it to the decode value of the recieved token 
  return request.user

@app.route("/protected", method=["GET"], permissions=["user"])
def protected():
  return {"message": "some secret API resource for users"}

@app.route("/adminonly", method=["GET"], permissions=["admin"])
def adminOny():
  return {"message": "some secret API resource for admins"}

@app.route("/invalidateall", method=["GET"], permissions=["admin"])
def invalidateAll():
  # Change jwt_key until next restart
  plugin.jwt_key = ''.join(random.choice("qwertyuioplkjhgfdsazxcvbnm") for i in range(10))
  return {"message": "all token are now invalid"}
  
# Start server
app.run(host="0.0.0.0", debug=debug, reloader=True)