import os
from flask import Flask, render_template, request, redirect, url_for, session
import stripe

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Configure Stripe
stripe.api_key = "your_stripe_secret_key"
stripe_publishable_key = "your_stripe_publishable_key"

# Sample product data (you can replace this with a database)
products = [
    {"id": 1, "name": "Product 1", "price": 1000},
    {"id": 2, "name": "Product 2", "price": 2000},
    # Add more products
]

@app.route("/")
def index():
    return render_template("index.html", products=products, stripe_publishable_key=stripe_publishable_key)

@app.route("/cart", methods=["GET", "POST"])
def cart():
    if request.method == "POST":
        product_id = int(request.form["product_id"])
        product = next((p for p in products if p["id"] == product_id), None)
        if product:
            session.setdefault("cart", []).append(product)
    return render_template("cart.html", cart=session.get("cart", []), stripe_publishable_key=stripe_publishable_key)

@app.route("/checkout", methods=["POST"])
def checkout():
    cart = session.get("cart", [])
    total_amount = sum(product["price"] for product in cart)

    session["cart"] = []  # Clear the cart after checkout
    return render_template("checkout.html", total_amount=total_amount, stripe_publishable_key=stripe_publishable_key)

if __name__ == "__main__":
    app.run(debug=True)
