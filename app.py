import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)
app.json.ensure_ascii = False

def get_db_connection():
    conn = sqlite3.connect("menu.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    return "Привет, мир!"

@app.route("/about")
def about():
    return "Это страница о нас."

@app.route("/contact")
def contact():
    return "Пишите нам: info@example.com"

@app.route("/user")
def user():
    return {
        "id": 1,
        "name": "Джурашо",
        "city": "Душанбе",
        "skills": ["Python"]
    }

@app.route("/hello/<name>")
def hello(name):
    return f"Привет, {name}!"

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Нет данных"
        }), 400

    name = data.get("name")
    age = data.get("age")

    if not name:
        return jsonify({
            "error": "Поле name обязательно"
        }), 400

    return jsonify({
        "status": "ok",
        "message": f"Пользователь {name} создан",
        "user": {
            "name": name,
            "age": age
        }
    }), 201

@app.route("/search")
def search():
    query = request.args.get("q")

    if not query:
        return "Введите запрос"

    return f"Ищем: {query}"


@app.route("/product-search")
def product_search():
    category = request.args.get("category")
    max_price = request.args.get("max_price")

    return f"Категория: {category}, максимальная цена: {max_price}"

products = [
    {
        "id": 1,
        "name": "Ноутбук",
        "price": 1200
    },
    {
        "id": 2,
        "name": "Мышка",
        "price": 25
    },
    {
        "id": 3,
        "name": "Клавиатура",
        "price": 80
    }
]

@app.route("/products", methods=["GET"])
def get_products():
    return jsonify(products)


@app.route("/products/<int:id>", methods=["GET"])
def get_product(id):
    for product in products:
        if product["id"] == id:
            return jsonify(product)

    return jsonify({
        "error": "Товар не найден"
    }), 404


@app.route("/products", methods=["POST"])
def add_product():
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Нет данных"
        }), 400

    if "name" not in data or "price" not in data:
        return jsonify({
            "error": "Нужны поля name и price"
        }), 400

    new_id = max(product["id"] for product in products) + 1

    new_product = {
        "id": new_id,
        "name": data["name"],
        "price": data["price"]
    }

    products.append(new_product)

    return jsonify(new_product), 201

notes = [
    {
        "id": 1,
        "title": "Первая заметка",
        "text": "Изучаю Flask"
    },
    {
        "id": 2,
        "title": "Вторая заметка",
        "text": "Сегодня изучaю POST и JSON"
    }
]


@app.route("/notes", methods=["GET"])
def get_notes():
    return jsonify(notes)


@app.route("/notes/<int:id>", methods=["GET"])
def get_note(id):
    for note in notes:
        if note["id"] == id:
            return jsonify(note)

    return jsonify({"error": "Заметка не найдена"}), 404


@app.route("/notes", methods=["POST"])
def add_note():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Нет данных"}), 400

    if "title" not in data or "text" not in data:
        return jsonify({"error": "Нужны поля title и text"}), 400

    new_id = max(note["id"] for note in notes) + 1

    new_note = {
        "id": new_id,
        "title": data["title"],
        "text": data["text"]
    }

    notes.append(new_note)

    return jsonify(new_note), 201


@app.route("/notes/<int:id>", methods=["DELETE"])
def delete_note(id):
    for note in notes:
        if note["id"] == id:
            notes.remove(note)
            return jsonify({"status": "deleted"})

    return jsonify({"error": "Заметка не найдена"}), 404



@app.route("/menu", methods=["GET"])
def get_menu():
    category = request.args.get("category")
    max_price = request.args.get("max_price")
    available = request.args.get("available")
    
    query = "SELECT * FROM dishes WHERE 1=1"
    
    params = []
    
    if category:
        query += " AND category = ?"
        params.append(category)
        
    if max_price:
        query += " AND price <= ?"
        params.append(max_price)
        
    if available is not None:
        query += " AND available = ?"
        params.append(1 if available.lower() == "true" else 0)
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    
    conn.close()
    
    dishes = []
    
    for row in rows:
        dishes.append({
            "id": row["id"],
            "name": row["name"],
            "category": row["category"],
            "price": row["price"],
            "available": bool(row["available"])
        })
        
    return jsonify(dishes)


@app.route("/menu/<int:id>", methods=["GET"])
def get_dish(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM dishes WHERE id = ?", (id,))
    row = cursor.fetchone()
    
    conn.close()
    
    if row is None:
        return jsonify({"error": "Dish not found"}), 404
    
    dish = {
        "id": row["id"],
        "name": row["name"],
        "category": row["category"],
        "price": row["price"],
        "available": bool(row["available"])
    }
    
    return jsonify(dish)

@app.route("/menu", methods=["POST"])
def add_dish():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    name = data.get("name")
    category = data.get("category")
    price = data.get("price")
    available = data.get("available", True)
    
    if not name or not category or price is None:
        return jsonify({"error": "Fields name, category, price are required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO dishes (name, category, price, available) VALUES (?, ?, ?, ?)",
                   (name, category, price, 1 if available else 0))
    
    new_id = cursor.lastrowid
    
    conn.commit()
    conn.close()

    return jsonify({
        "id": new_id,
        "name": name,
        "category": category,
        "price": price,
        "available": available
        }), 201
    
    
@app.route("/menu/<int:id>", methods=["DELETE"])
def delete_dish(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM dishes WHERE id = ?", (id,))
    
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({"error": "Dish not found"}), 404
    
    conn.commit()
    conn.close()
    
    return jsonify({"status": "deleted"}), 200
    
    
@app.route("/menu/<int:id>", methods=["PATCH"])

def update_dish(id):
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    allowed_fields = ["name", "category", "price", "available"]
    
    fields = []
    values = []
    
    for field in allowed_fields:
        if field in data:
            fields.append(f"{field} = ?")
            if field == "available":
                values.append(1 if data[field] else 0)
            else:
                values.append(data[field])

    if not fields:
        return jsonify({"error": "No valid fields to update"}), 400

    values.append(id)

    conn = get_db_connection()
    cursor = conn.cursor()

    query = f"""UPDATE dishes SET {', '.join(fields)} WHERE id = ?"""

    cursor.execute(query, values)

    if cursor.rowcount == 0:
        conn.close()
        return jsonify({"error": "Dish not found"}), 404

    conn.commit()
    
    cursor.execute("SELECT * FROM dishes WHERE id = ?", (id,))
    row = cursor.fetchone()
    
    conn.close()

    return jsonify({
        "id": row["id"],
        "name": row["name"],
        "category": row["category"],
        "price": row["price"],
        "available": bool(row["available"])
    }), 200

if __name__ == "__main__":
    app.run(debug=True)
    

