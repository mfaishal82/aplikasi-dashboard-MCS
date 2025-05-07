# Aplikasi Dashboard MCS

Dashboard untuk monitoring dan analisis data pendidikan MCS.

## Fitur

1. **Overview**
   - Statistik total siswa dan pengajar
   - Distribusi gender
   - Rasio siswa:pengajar
   - Total kelas dan halaqoh aktif

2. **Akademik**
   - Distribusi siswa per kelas
   - Distribusi siswa per halaqoh
   - Analisis kapasitas kelas

3. **Monitoring Halaqoh**
   - Kapasitas halaqoh (ideal vs aktual)
   - Performa halaqoh berdasarkan setoran
   - Tren setoran harian

## Instalasi

1. Clone repository ini
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Buat file `.env` dengan konfigurasi berikut:
   ```
   SUPABASE_CONNECTION_STRING=postgresql://[user]:[password]@[host]:[port]/[database]
   ```

## Penggunaan

Jalankan aplikasi dengan perintah:
```bash
streamlit run app.py
```

## Teknologi

- Streamlit
- Pandas
- Plotly
- SQLAlchemy
- PostgreSQL (via Supabase)
