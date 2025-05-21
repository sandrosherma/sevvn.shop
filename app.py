from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
import os
import json

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join('static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_products():
    if os.path.exists("products.json"):
        try:
            with open("products.json", "r") as f:
                return json.load(f)
        except:
            return []
    return []

def save_products(products):
    with open("products.json", "w") as f:
        json.dump(products, f, indent=2)

@app.route('/')
def index():
    products = load_products()
    featured = products[:3] 
    return render_template('index.html', products=featured)

@app.route('/shop')
def shop():
    products = load_products()  
    return render_template('shop.html', products=products)


@app.route("/admin/894853")
def admin_panel():
    products = load_products()
    return render_template("admin.html", products=products)

@app.route("/product/<int:product_id>")
def product_detail(product_id):
    products = load_products()
    product = next((p for p in products if p["id"] == product_id), None)
    if product:
        return render_template("product_detail.html", product=product)
    else:
        return 'Product not found', 404
@app.route("/add_product", methods=["POST"])
def add_product():
    name = request.form["name"]
    price = request.form["price"]
    description = request.form["description"]
    image = request.files["image"]
    

    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(path)
        image_url = f"/static/uploads/{filename}"
    else:
        image_url = ""

    products = load_products()
    new_product = {
        "id": len(products) + 1,
        "name": name,
        "price": price,
        "description": description,
        "image": image_url
    }
    products.append(new_product)
    save_products(products)
    return redirect("/admin/894853")

@app.route("/delete_product/<int:product_id>", methods=["POST"])
def delete_product(product_id):
    products = load_products()
    products = [p for p in products if p["id"] != product_id]
    save_products(products)
    return redirect("/admin/894853")



if __name__ == "__main__":
    app.run(debug=True)
