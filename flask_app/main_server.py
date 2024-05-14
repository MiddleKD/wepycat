import os, json
from glob import glob
from flask import Flask

with open(os.path.join(os.path.dirname(__file__), "domain_map.json"), mode="r") as f:
    domain_map = json.load(f)
app = Flask(__name__, static_folder="..", static_url_path="/")
app_fns = glob("./*_app.py")

for module in app_fns:
    module_name = os.path.splitext(os.path.basename(module))[0]
    module = __import__(module_name)
    module.register_routes(app, domain_map)

if __name__ == "__main__":
    app.run(debug=True, port=8000, host="0.0.0.0")
