# app/routes/predict.py
from flask import Blueprint, request, jsonify
from app.controllers.ml_controller import predict_ml  # ← pastikan ini fungsi yang terima (method, fitur_list)
import datetime

bp = Blueprint('predict', __name__, url_prefix='/predict')

@bp.route('/', methods=['POST'])
def predict():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n[INFO] 🕒 {timestamp} - Menerima request prediksi...")
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": False, "error": "Request body harus berupa JSON"}), 400
        
        # ✅ SESUAIKAN DENGAN FRONTEND: baca 'method' dan 'fitur'
        method = data.get('method')
        fitur = data.get('fitur')  # ← nama field = 'fitur', tipe = list

        if not method:
            return jsonify({"status": False, "error": "Parameter 'method' wajib diisi"}), 400
        
        if not isinstance(fitur, list):
            return jsonify({"status": False, "error": "Parameter 'fitur' harus berupa list/array angka"}), 400

        if len(fitur) != 11:
            return jsonify({"status": False, "error": "Harus ada 11 nilai fitur"}), 400

        print(f"[INFO] Method: {method}, Fitur: {fitur}")

        # ✅ Panggil controller dengan (method, fitur_list)
        result = predict_ml(method, fitur)

        if not result["status"]:
            print(f"[ERROR] ❌ {result['error']}")
            return jsonify(result), 400

        print(f"[SUCCESS] ✅ Prediksi: {result['hasil_prediksi']}")
        return jsonify(result)

    except Exception as e:
        error_msg = f"Error tidak terduga: {str(e)}"
        print(f"[CRITICAL] 💥 {error_msg}")
        return jsonify({"status": False, "error": error_msg}), 500