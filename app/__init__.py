# app/__init__.py
from flask import Flask
from flask_cors import CORS  # ← tambahkan ini

def create_app():
    app = Flask(__name__)
    CORS(app)  # ← aktifkan CORS untuk semua route
    
    @app.route('/')
    def home():
        return {
            "message": "✅ Flask API sudah berjalan!",
            "note": "Frontend bisa terhubung sekarang."
        }

    from app.routes import predict
    app.register_blueprint(predict.bp)
    
    return app