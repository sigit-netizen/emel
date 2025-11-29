import os
import pickle

# Tentukan path relatif dari file ini ke root proyek
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

MODEL_PATHS = {
    "naive_bayes": os.path.join(ROOT_DIR, "app", "ml", "models", "naive_bayes.pkl"),
    "id3": os.path.join(ROOT_DIR, "app", "ml", "models", "id3.pkl"),
}

def load_model(method):
    """Load model sesuai method."""
    if method not in MODEL_PATHS:
        return None, f"Model '{method}' tidak ditemukan!"

    path = MODEL_PATHS[method]

    if not os.path.exists(path):
        return None, f"File model '{method}' belum tersedia di: {path}"

    try:
        with open(path, "rb") as f:
            model = pickle.load(f)
        return model, None
    except Exception as e:
        return None, f"Gagal memuat model '{method}': {str(e)}"


def predict_ml(method, fitur):
    """
    Fungsi prediksi murni — tidak tergantung Flask request.
    Input: method (str), fitur (list)
    Output: dict hasil atau error
    """
    if not method:
        return {"status": False, "error": "Parameter 'method' harus diisi!"}

    if not isinstance(fitur, list):
        return {"status": False, "error": "Parameter 'fitur' harus berupa list/array!"}

    # Load model
    model, err = load_model(method)
    if err:
        return {"status": False, "error": err}

    # Pastikan fitur adalah list numerik (sesuaikan jika data kategorikal)
    try:
        # Prediksi
        hasil = model.predict([fitur])  # sklearn: butuh 2D array
        hasil_prediksi = hasil[0].item()
    except Exception as e:
        return {
            "status": False,
            "error": f"Kesalahan saat proses prediksi: {str(e)}"
        }

    return {
        "status": True,
        "model": method,
        "input": fitur,
        "hasil_prediksi": hasil_prediksi
    }