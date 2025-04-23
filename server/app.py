from flask import Flask, request, jsonify
from flask_cors import CORS
from db import get_db_connection

from flask_mail import Mail, Message
# from flask_mysql import MySQL

app = Flask(__name__)
CORS(app)

# Thiết lập cấu hình cho Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'phu272401@gmail.com'  # Thay bằng email của bạn
app.config['MAIL_PASSWORD'] = '#8888phu272401@'  # Thay bằng mật khẩu ứng dụng
mail = Mail(app)

# Lấy danh sách sản phẩm
@app.route('/products', methods=['GET'])
def get_products():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    return jsonify(products)

# Thêm sản phẩm
@app.route('/products', methods=['POST'])
def add_product():
    data = request.json
    name = data['name']
    price = data['price']
    description = data['description']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO products (name, price, description) VALUES (%s, %s, %s)",
        (name, price, description)
    )
    conn.commit()
    conn.close()
    return jsonify({'message': 'Product added successfully'}), 201

# Sửa sản phẩm
@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.json
    name = data['name']
    price = data['price']
    description = data['description']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE products SET name = %s, price = %s, description = %s WHERE id = %s",
        (name, price, description, id)
    )
    conn.commit()
    conn.close()
    return jsonify({'message': 'Product updated successfully'})

# Xóa sản phẩm
@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Product deleted successfully'})

#Tạo API để nhận và xử lý thông tin liên hệ từ người dùng
@app.route('/api/contact', methods=['POST'])
def contact():
    data = request.get_json()

    name = data.get('name')
    email = data.get('email')
    message = data.get('message')

    if not name or not email or not message:
        return jsonify({'error': 'Thiếu thông tin cần thiết'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Lưu thông tin vào cơ sở dữ liệu
        cursor.execute(
            "INSERT INTO contact_messages (name, email, message) VALUES (%s, %s, %s)",
            (name, email, message)
        )
        conn.commit()

        # Gửi email thông báo
        msg = Message(f"Liên hệ từ {name}",
                        recipients=["your-email@gmail.com"],
                        body=f"Bạn có một tin nhắn mới từ {name} ({email}):\n\n{message}")
        mail.send(msg)

        return jsonify({'message': 'Thông tin đã được gửi và lưu trữ thành công!'}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({'error': f'Đã xảy ra lỗi: {str(e)}'}), 500

    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000 )
