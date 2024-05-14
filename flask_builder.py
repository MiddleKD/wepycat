import re, os
from glob import glob

def make_flask_app_py(page_dir_name):

    app_template = """import os, json
from flask import Flask
from flask import request

def register_routes(app, domain_map):
"""

    for html_fn in glob(os.path.join(page_dir_name, "*.html")):
        routing = re.search(fr"(?<={page_dir_name}).*(?=\.html)", html_fn)[0]
        function_name = re.sub(r'\W+', '_', page_dir_name.replace("./","")+routing)
        
        if "home" in routing:
            routing = "/"
        
        route_template = f"""
    @app.route("{routing}")
    def {function_name}():
        web_name = domain_map.get(request.host, None)
        if web_name is not None:
            return app.send_static_file(f"{{web_name}}{html_fn.replace(page_dir_name, "")}")
        else:
            return app.send_static_file("default_web{html_fn.replace(page_dir_name, "")}")
"""

        app_template += route_template

    app_template += f"""
if __name__ == '__main__':
    with open(os.path.join(os.path.dirname(__file__), "domain_map.json"), mode="r") as f:
        domain_map = json.load(f)
    app = Flask(__name__, static_folder="..", static_url_path="/")
    register_routes(app, domain_map)
    app.run(debug=True, port=8000, host="0.0.0.0")
"""

    return app_template

def save_flask_app_file(falsk_app_py:str, outpu_path:str):
    with open(outpu_path, mode="w") as f:
        f.write(falsk_app_py)