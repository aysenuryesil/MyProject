# Hata olursa scripti durdur
$ErrorActionPreference = "Stop"

# Paketleri yükle
pip install -r requirements.txt

# Statik dosyaları topla
python manage.py collectstatic --no-input

# Veritabanı migrasyonlarını uygula
python manage.py migrate

Write-Host "Build script completed successfully!"
