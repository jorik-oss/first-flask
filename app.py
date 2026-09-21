from flask import Flask, request, jsonify

app = Flask(__name__)
app.json.ensure_ascii = False

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


menu = [
    {"id": 1, "name": "Плов",      "category": "main",  "price": 40, "available": True},
    {"id": 2, "name": "Шурпа",     "category": "soup",  "price": 30, "available": True},
    {"id": 3, "name": "Самса",     "category": "snack", "price": 10, "available": True},
    {"id": 4, "name": "Чай",       "category": "drink", "price": 5,  "available": True},
    {"id": 5, "name": "Кофе",      "category": "drink", "price": 15, "available": False},
]

@app.route("/menu", methods=["GET"])
def get_menu():
    availeble = request.args.get("available")
    max_price = request.args.get("max_price")
    
    filtered_menu = menu
    
    if availeble is not None:  
        if availeble == "true":
            filtered_menu = [item for item in menu if item["available"]]
        elif availeble == "false":
            filtered_menu = [item for item in menu if not item["available"]]
    
    if max_price is not None:
            max_price = int(max_price)
            filtered_menu = [item for item in filtered_menu if item["price"] <= max_price]
            
    return jsonify(filtered_menu)



@app.route("/menu/<int:id>", methods=["GET"])
def get_menu_item(id):
    for item in menu:
        if item["id"] == id:
            return jsonify(item)

    return jsonify({"error": "Блюдо не найдено"}), 404

@app.route("/menu/category/<string:category>", methods=["GET"])
def get_menu_by_category(category):
    filtered_items = [item for item in menu if item["category"] == category]
    return jsonify(filtered_items)

@app.route("/menu", methods=["POST"])
def add_menu_item():
    data = request.get_json()

    if "name" not in data or "category" not in data or "price" not in data:
        return jsonify({"error": "Нужны поля name, category и price"}), 400

    new_id = max(item["id"] for item in menu) + 1

    new_item = {
        "id": new_id,
        "name": data["name"],
        "category": data["category"],
        "price": data["price"],
        "available": data.get("available", True)
    }

    menu.append(new_item)

    return jsonify(new_item), 201

@app.route("/menu/stats", methods=["GET"])
def get_menu_stats():
    total_items = len(menu)
    available_items = sum(1 for item in menu if item["available"])
    unavailable_items = sum(1 for item in menu if not item["available"])
    avg_price = sum(item["price"] for item in menu) / total_items
    categories = (item["category"] for item in menu)
    

    return jsonify({
        "total_items": total_items,
        "available_items": available_items,
        "unavailable_items": unavailable_items,
        "avg_price": avg_price ,
        "categories": list(categories)
    })
    
@app.route("/menu/<int:id>", methods=["PATCH"])
def update_menu_item(id):
    data = request.get_json()
    for item in menu:
        if item["id"] == id:
            for key, value in data.items():
                if key in item:
                    item[key] = value
            return jsonify(item)
    return jsonify({"error": "Блюдо не найдено"}), 404

@app.route("/menu/<int:id>", methods=["DELETE"])
def delete_menu_item(id):
    for item in menu:
        if item["id"] == id:
            menu.remove(item)
            return jsonify({"status": "deleted", "id": id})
    return jsonify({"error": "Блюдо не найдено"}), 404

@app.route("/menu/<int:id>/toggle", methods=["POST"])
def toggle_menu_item(id):
    for item in menu:
        if item["id"] == id:
            item["available"] = not item["available"]
            return jsonify(item)
    return jsonify({"error": "Блюдо не найдено"}), 404

if __name__ == "__main__":
    app.run(debug=True)
    

