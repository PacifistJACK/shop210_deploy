from flask import Flask, render_template, request, redirect, url_for, session
from database import fetch_categories, fetch_items_by_category
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()
app.secret_key = os.getenv("SECRET_KEY")

@app.route("/")
def home():
    categories = fetch_categories()
    return render_template("home.html", categories=categories)

@app.route("/category/<int:category_id>")
def category(category_id):
    items = fetch_items_by_category(category_id)
    return render_template("items.html", items=items)

@app.route("/add-to-cart", methods=["POST"])
def add_to_cart():
    item_id = request.form.get("item_id")
    if "cart" not in session:
        session["cart"] = {}

    cart = session["cart"]
    cart[item_id] = cart.get(item_id, 0) + 1  # Increment quantity
    session["cart"] = cart  # Save it back to session
    return redirect(request.referrer)

@app.route("/cart")
def cart():
    from database import get_item_by_id  # Ensure this function is defined
    cart = session.get("cart", {})
    cart_items = []
    total_cost = 0  # Initialize total cost

    # Loop through cart items and calculate total
    for item_id, qty in cart.items():
        item = get_item_by_id(item_id)
        if item:
            item_dict = dict(item._mapping)
  # Convert to dict to access fields
            item_dict["quantity"] = qty
            item_dict["total_price"] = qty * item_dict["price"]
            cart_items.append(item_dict)
            total_cost += item_dict["total_price"]  # Add item total to the total cost

    return render_template("cart.html", cart_items=cart_items, total_cost=total_cost)

@app.route("/update-quantity", methods=["POST"])
def update_quantity():
    item_id = request.form.get("item_id")
    action = request.form.get("action")

    if "cart" in session and item_id in session["cart"]:
        if action == "increase":
            session["cart"][item_id] += 1
        elif action == "decrease" and session["cart"][item_id] > 1:
            session["cart"][item_id] -= 1
        elif action == "decrease":
            session["cart"].pop(item_id)  # Remove item if quantity hits 0
        session.modified = True

    return redirect(url_for("cart"))

@app.route("/checkout", methods=["POST"])
def checkout():
    # You can later add order-saving logic here
    session.pop("cart", None)  # Clear the cart after checkout
    return redirect(url_for("order_success"))


@app.route("/order-success")
def order_success():
    return render_template("sucs.html")


if __name__ == '__main__':
    app.run(debug=True)
