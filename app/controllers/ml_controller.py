# import os
# import pickle

# # Tentukan path relatif dari file ini ke root proyek
# ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# MODEL_PATHS = {
#     "naive_bayes": os.path.join(ROOT_DIR, "app", "ml", "models", "naive_bayes.pkl"),
#     "id3": os.path.join(ROOT_DIR, "app", "ml", "models", "id3.pkl"),
# }

# def load_model(method):
#     """Load model sesuai method."""
#     if method not in MODEL_PATHS:
#         return None, f"Model '{method}' tidak ditemukan!"

#     path = MODEL_PATHS[method]

#     if not os.path.exists(path):
#         return None, f"File model '{method}' belum tersedia di: {path}"

#     try:
#         with open(path, "rb") as f:
#             model = pickle.load(f)
#         return model, None
#     except Exception as e:
#         return None, f"Gagal memuat model '{method}': {str(e)}"


# def predict_ml(method, fitur):
#     """
#     Fungsi prediksi murni — tidak tergantung Flask request.
#     Input: method (str), fitur (list)
#     Output: dict hasil atau error
#     """
#     if not method:
#         return {"status": False, "error": "Parameter 'method' harus diisi!"}

#     if not isinstance(fitur, list):
#         return {"status": False, "error": "Parameter 'fitur' harus berupa list/array!"}

#     # Load model
#     model, err = load_model(method)
#     if err:
#         return {"status": False, "error": err}

#     # Pastikan fitur adalah list numerik (sesuaikan jika data kategorikal)
#     try:
#         # Prediksi
#         hasil = model.predict([fitur])  # sklearn: butuh 2D array
#         hasil_prediksi = hasil[0].item()
#     except Exception as e:
#         return {
#             "status": False,
#             "error": f"Kesalahan saat proses prediksi: {str(e)}"
#         }

#     return {
#         "status": True,
#         "model": method,
#         "input": fitur,
#         "hasil_prediksi": hasil_prediksi
#     }

import os
import pickle
import pandas as pd

# Tentukan path encoder dan model
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENCODER_PATH = os.path.join(ROOT_DIR, "app", "ml", "models", "encoders.pkl")
MODEL_PATHS = {
    "random_forest": os.path.join(ROOT_DIR, "app", "ml", "models", "random_forest.pkl"),
    "xgboost": os.path.join(ROOT_DIR, "app", "ml", "models", "xgboost.pkl"),
    "naive_bayes": os.path.join(ROOT_DIR, "app", "ml", "models", "naive_bayes.pkl"),
    "id3": os.path.join(ROOT_DIR, "app", "ml", "models", "id3.pkl"),
}

# Load encoder dan fitur
with open(ENCODER_PATH, "rb") as f:
    saved_data = pickle.load(f)

fitur_train = saved_data["columns"]  # list nama kolom fitur
encoders = saved_data["encoders"]    # dict LabelEncoder

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

def predict_ml(method, fitur_list):
    """
    Predict ML
    Input: 
        method: nama model
        fitur_list: list nilai fitur sesuai urutan
    Output: dict hasil prediksi
    """
    # Validasi input
    if not method:
        return {"status": False, "error": "Parameter 'method' harus diisi!"}
    if not isinstance(fitur_list, list):
        return {"status": False, "error": "Parameter 'fitur' harus berupa list/array!"}
    if len(fitur_list) != len(fitur_train):
        return {"status": False, "error": f"Harus ada {len(fitur_train)} nilai fitur!"}

    # Load model
    model, err = load_model(method)
    if err:
        return {"status": False, "error": err}

    try:
        # Konversi list input jadi dict sesuai urutan kolom
        fitur_dict = {col: val for col, val in zip(fitur_train, fitur_list)}
        df_input = pd.DataFrame([fitur_dict])

        # Encode kategori sesuai encoder training
        for col, le in encoders.items():
            if col in df_input.columns:
                val = df_input[col].iloc[0]
                if val not in le.classes_:
                    return {
                        "status": False,
                        "error": f"Value '{val}' untuk kolom '{col}' tidak valid. Pilihan: {list(le.classes_)}"
                    }
                df_input[col] = le.transform(df_input[col])

        # Pastikan urutan kolom sama seperti saat training
        df_input = df_input[fitur_train]

        # Prediksi
        hasil = model.predict(df_input)
        hasil_prediksi = hasil[0].item()

    except Exception as e:
        return {"status": False, "error": f"Kesalahan saat proses prediksi: {str(e)}"}

    return {
        "status": True,
        "model": method,
        "input": fitur_list,
        "hasil_prediksi": hasil_prediksi
    }
