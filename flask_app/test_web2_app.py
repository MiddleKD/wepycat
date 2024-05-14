import os, json
from flask import Flask
from flask import request

def register_routes(app, domain_map):

    @app.route("/offer")
    def test_web2_offer():
        web_name = domain_map.get(request.host, None)
        if web_name is not None:
            return app.send_static_file(f"{web_name}/offer.html")
        else:
            return app.send_static_file("default_web/offer.html")

    @app.route("/portfolio")
    def test_web2_portfolio():
        web_name = domain_map.get(request.host, None)
        if web_name is not None:
            return app.send_static_file(f"{web_name}/portfolio.html")
        else:
            return app.send_static_file("default_web/portfolio.html")

    @app.route("/gallery")
    def test_web2_gallery():
        web_name = domain_map.get(request.host, None)
        if web_name is not None:
            return app.send_static_file(f"{web_name}/gallery.html")
        else:
            return app.send_static_file("default_web/gallery.html")

    @app.route("/pricing")
    def test_web2_pricing():
        web_name = domain_map.get(request.host, None)
        if web_name is not None:
            return app.send_static_file(f"{web_name}/pricing.html")
        else:
            return app.send_static_file("default_web/pricing.html")

    @app.route("/offer?anchorElement=wSection_23&amp;scrollMargin=50")
    def test_web2_offer_anchorElement_wSection_23_amp_scrollMargin_50():
        web_name = domain_map.get(request.host, None)
        if web_name is not None:
            return app.send_static_file(f"{web_name}/offer?anchorElement=wSection_23&amp;scrollMargin=50.html")
        else:
            return app.send_static_file("default_web/offer?anchorElement=wSection_23&amp;scrollMargin=50.html")

    @app.route("/offer?anchorElement=wSection_11&amp;scrollMargin=50")
    def test_web2_offer_anchorElement_wSection_11_amp_scrollMargin_50():
        web_name = domain_map.get(request.host, None)
        if web_name is not None:
            return app.send_static_file(f"{web_name}/offer?anchorElement=wSection_11&amp;scrollMargin=50.html")
        else:
            return app.send_static_file("default_web/offer?anchorElement=wSection_11&amp;scrollMargin=50.html")

    @app.route("/about-us")
    def test_web2_about_us():
        web_name = domain_map.get(request.host, None)
        if web_name is not None:
            return app.send_static_file(f"{web_name}/about-us.html")
        else:
            return app.send_static_file("default_web/about-us.html")

    @app.route("/")
    def test_web2_home():
        web_name = domain_map.get(request.host, None)
        if web_name is not None:
            return app.send_static_file(f"{web_name}/home.html")
        else:
            return app.send_static_file("default_web/home.html")

    @app.route("/contact")
    def test_web2_contact():
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
