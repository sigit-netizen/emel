document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('predictionForm');
    const resultBox = document.getElementById('result');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Ambil model
        const model = document.getElementById('model').value;
        if (!model) {
            showResult('error', 'Silakan pilih model terlebih dahulu!');
            return;
        }

        // Ambil 11 nilai fitur sesuai ID
        const fitur = [
            parseFloat(document.getElementById('fixed_acidity').value),
            parseFloat(document.getElementById('volatile_acidity').value),
            parseFloat(document.getElementById('citric_acid').value),
            parseFloat(document.getElementById('residual_sugar').value),
            parseFloat(document.getElementById('chlorides').value),
            parseFloat(document.getElementById('free_sulfur_dioxide').value),
            parseFloat(document.getElementById('total_sulfur_dioxide').value),
            parseFloat(document.getElementById('density').value),
            parseFloat(document.getElementById('ph').value),
            parseFloat(document.getElementById('sulphates').value),
            parseFloat(document.getElementById('alcohol').value)
        ];

        // Validasi semua angka
        if (fitur.some(isNaN)) {
            showResult('error', 'Semua input harus berupa angka!');
            return;
        }

        showResult('loading', 'Mengirim ke server...');

        try {
            const response = await fetch('http://127.0.0.1:5000/predict/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ method: model, fitur: fitur })
            });

            const data = await response.json();

            if (data.status) {
                showResult('success', `
                    <strong>Model:</strong> ${data.model}<br>
                    <strong>Hasil Prediksi:</strong> ${data.hasil_prediksi}<br>
                    <small>Input: [${data.input.join(', ')}]</small>
                `);
            } else {
                showResult('error', data.error || 'Terjadi kesalahan pada server.');
            }
        } catch (err) {
            showResult('error', `Gagal terhubung ke API: ${err.message}`);
        }
    });
});

function showResult(type, message) {
    const resultBox = document.getElementById('result');
    resultBox.innerHTML = `
        <h3>${type === 'success' ? '✅ Sukses!' : type === 'error' ? '❌ Error!' : '⏳ Loading...'}</h3>
        <p>${message}</p>
    `;
    resultBox.className = `result-box ${type}`;
    resultBox.style.display = 'block';
}