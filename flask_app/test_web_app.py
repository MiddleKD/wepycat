import os, json
from flask import Flask
from flask import request

def register_routes(app, domain_map):

    @app.route("/offer")
    def test_web_offer():
        web_name = domain_map.get(request.host, None)
        if web_name is not None:
            return app.send_static_file(f"{web_name}/offer.html")
        else:
            return app.send_static_file("default_web/offer.html")

    @app.route("/projects")
    def test_web_projects():
        web_name = domain_map.get(request.host, None)
        if web_name is not None:
            return app.send_static_file(f"{web_name}/projects.html")
        else:
            return app.send_static_file("default_web/projects.html")

    @app.route("/gallery")
    def test_web_gallery():
        web_name = domain_map.get(request.host, None)
        if web_name is not None:
            return app.send_static_file(f"{web_name}/gallery.html")
        else:
            return app.send_static_file("default_web/gallery.html")

    @app.route("/price-list")
    def test_web_price_list():
        web_name = domain_map.get(request.host, None)
        if web_name is not None:
            return app.send_static_file(f"{web_name}/price-list.html")
        else:
            return app.send_static_file("default_web/price-list.html")

    @app.route("/about-us")
    def test_web_about_us():
        web_name = domain_map.get(request.host, None)
        if web_name is not None:
            return app.send_static_file(f"{web_name}/about-us.html")
        else:
            return app.send_static_file("default_web/about-us.html")

    @app.route("/")
    def test_web_home():
        web_name = domain_map.get(request.host, None)
        if web_name is not None:
            return app.send_static_file(f"{web_name}/home.html")
        else:
            return app.send_static_file("default_web/home.html")

    @app.route("/contact")
    def test_web_contact():
        web_name = domain_map.get(request.host, None)
        if web_name is not None:
            return app.send_static_file(f"{web_name}/contact.html")
        else:
            return app.send_static_file("default_web/contact.html")

if __name__ == '__main__':
    with open(os.path.join(os.path.dirname(__file__), "domain_map.json"), mode="r") as f:
        domain_map = json.load(f)
    app = Flask(__name__, static_folder="..", static_url_path="/")
    register_routes(app, domain_map)
    app.run(debug=True, port=8000, host="0.0.0.0")
