"""Shopwise Demo Store: a tiny web app used as a stable, local target for the UI test frameworks.

Why it exists: public demo sites change without notice and are blocked in many CI networks.
A small app that ships with the repository makes the Selenium and Playwright suites
deterministic, offline and free to run anywhere.

    python demo-app/app.py --port 5000

Login: the user and password come from DEMO_USER and DEMO_PASSWORD. The defaults are fixture
values for this local app only and protect nothing. The user "locked.user" is always locked.
"""
import argparse
import os
import secrets

from flask import Flask, jsonify, redirect, render_template_string, request, session, url_for

PRODUCTS = [
    {"id": 1, "name": "Backpack", "price": 29.99},
    {"id": 2, "name": "Bike Light", "price": 9.99},
    {"id": 3, "name": "Bolt T-Shirt", "price": 15.99},
    {"id": 4, "name": "Fleece Jacket", "price": 49.99},
    {"id": 5, "name": "Onesie", "price": 7.99},
    {"id": 6, "name": "Test.allTheThings() T-Shirt", "price": 15.99},
]
BY_ID = {p["id"]: p for p in PRODUCTS}

LAYOUT = """<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Shopwise Demo Store</title>
<style>body{font-family:sans-serif;margin:2rem auto;max-width:720px}.item{border:1px solid #ccc;padding:.6rem;margin:.4rem 0}
.error{color:#b00020}nav a{margin-right:1rem}</style></head><body>
<header><h1>Shopwise Demo Store</h1>
{% if session.get('user') %}<nav><a href="{{ url_for('inventory') }}">Products</a>
<a href="{{ url_for('cart') }}" data-testid="cart-link">Cart (<span data-testid="cart-count">{{ session.get('cart', [])|length }}</span>)</a>
<a href="{{ url_for('logout') }}" data-testid="logout">Log out</a></nav>{% endif %}</header>
<main>{{ body|safe }}</main></body></html>"""


def page(body: str, **ctx):
    return render_template_string(LAYOUT, body=render_template_string(body, **ctx))


def create_app() -> Flask:
    app = Flask(__name__)
    app.secret_key = os.getenv("DEMO_SECRET", secrets.token_hex(16))
    demo_user = os.getenv("DEMO_USER", "qa.demo")
    demo_password = os.getenv("DEMO_PASSWORD", "demo-pass")

    def logged_in() -> bool:
        return bool(session.get("user"))

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.get("/")
    def index():
        return redirect(url_for("login"))

    @app.route("/login", methods=["GET", "POST"])
    def login():
        error = ""
        if request.method == "POST":
            user = request.form.get("username", "").strip()
            password = request.form.get("password", "")
            if not user:
                error = "Username is required"
            elif not password:
                error = "Password is required"
            elif user == "locked.user":
                error = "This account is locked"
            elif user == demo_user and password == demo_password:
                session["user"], session["cart"] = user, []
                return redirect(url_for("inventory"))
            else:
                error = "Invalid username or password"
        return page(
            """<form method="post" data-testid="login-form">
<label>Username <input name="username" data-testid="username"></label><br>
<label>Password <input name="password" type="password" data-testid="password"></label><br>
<button type="submit" data-testid="login-button">Log in</button>
{% if error %}<p class="error" data-testid="login-error">{{ error }}</p>{% endif %}</form>""",
            error=error,
        )

    @app.get("/logout")
    def logout():
        session.clear()
        return redirect(url_for("login"))

    @app.get("/inventory")
    def inventory():
        if not logged_in():
            return redirect(url_for("login"))
        key = request.args.get("sort", "name")
        items = sorted(PRODUCTS, key=(lambda p: p["price"]) if key == "price" else (lambda p: p["name"]))
        return page(
            """<form method="get"><label>Sort by
<select name="sort" data-testid="sort" onchange="this.form.submit()">
<option value="name" {{ 'selected' if key == 'name' }}>Name</option>
<option value="price" {{ 'selected' if key == 'price' }}>Price</option></select></label></form>
<h2>Products</h2>
{% for p in items %}<div class="item" data-testid="product" data-id="{{ p.id }}">
<span data-testid="product-name">{{ p.name }}</span> -
<span data-testid="product-price">{{ '%.2f'|format(p.price) }}</span>
<form method="post" action="{{ url_for('cart_add', product_id=p.id) }}" style="display:inline">
{% if p.id in session.get('cart', []) %}<button data-testid="remove-{{ p.id }}" formaction="{{ url_for('cart_remove', product_id=p.id) }}">Remove</button>
{% else %}<button data-testid="add-{{ p.id }}">Add to cart</button>{% endif %}</form></div>{% endfor %}""",
            items=items,
            key=key,
        )

    @app.post("/cart/add/<int:product_id>")
    def cart_add(product_id: int):
        if not logged_in():
            return redirect(url_for("login"))
        cart = session.get("cart", [])
        if product_id in BY_ID and product_id not in cart:
            cart.append(product_id)
        session["cart"] = cart
        return redirect(request.referrer or url_for("inventory"))

    @app.post("/cart/remove/<int:product_id>")
    def cart_remove(product_id: int):
        if not logged_in():
            return redirect(url_for("login"))
        session["cart"] = [i for i in session.get("cart", []) if i != product_id]
        return redirect(request.referrer or url_for("inventory"))

    @app.get("/cart")
    def cart():
        if not logged_in():
            return redirect(url_for("login"))
        items = [BY_ID[i] for i in session.get("cart", [])]
        total = round(sum(p["price"] for p in items), 2)
        return page(
            """<h2>Your cart</h2>
{% for p in items %}<div class="item" data-testid="cart-item"><span data-testid="cart-item-name">{{ p.name }}</span> -
{{ '%.2f'|format(p.price) }}
<form method="post" action="{{ url_for('cart_remove', product_id=p.id) }}" style="display:inline">
<button data-testid="cart-remove-{{ p.id }}">Remove</button></form></div>
{% else %}<p data-testid="cart-empty">Your cart is empty</p>{% endfor %}
<p>Total: <span data-testid="cart-total">{{ '%.2f'|format(total) }}</span></p>
{% if items %}<a href="{{ url_for('checkout') }}" data-testid="checkout-link">Checkout</a>{% endif %}""",
            items=items,
            total=total,
        )

    @app.route("/checkout", methods=["GET", "POST"])
    def checkout():
        if not logged_in():
            return redirect(url_for("login"))
        error = ""
        if request.method == "POST":
            first, last, postal = (request.form.get(k, "").strip() for k in ("first_name", "last_name", "postal_code"))
            if not first:
                error = "First name is required"
            elif not last:
                error = "Last name is required"
            elif not postal:
                error = "Postal code is required"
            else:
                session["cart"] = []
                return redirect(url_for("done"))
        return page(
            """<h2>Checkout</h2><form method="post">
<label>First name <input name="first_name" data-testid="first-name"></label><br>
<label>Last name <input name="last_name" data-testid="last-name"></label><br>
<label>Postal code <input name="postal_code" data-testid="postal-code"></label><br>
<button type="submit" data-testid="finish">Finish</button>
{% if error %}<p class="error" data-testid="checkout-error">{{ error }}</p>{% endif %}</form>""",
            error=error,
        )

    @app.get("/done")
    def done():
        if not logged_in():
            return redirect(url_for("login"))
        return page('<h2 data-testid="order-complete">Thank you for your order</h2>')

    @app.get("/api/products")
    def api_products():
        return jsonify(PRODUCTS)

    return app


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Shopwise Demo Store")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5000)
    args = parser.parse_args()
    create_app().run(host=args.host, port=args.port)

