# Gemma bağlantısı

Bu bilgisayarda AI Agent Güvenlik Test Aracı, LM Studio'daki `gemma-4-e4b-it` modeliyle eşleştirildi.

- Model: `gemma-4-E4B-it-Q4_K_M.gguf`, 5.335.291.936 bayt.
- SHA-256: `0ffb122c8b6921f13cbc34186e052524d0b5803b17f4867b7197a561400b3770`
- API: `http://127.0.0.1:1234/v1`
- Masaüstündeki dosya korunarak LM Studio model klasörüne hard link ile eklendi; yeniden indirilmedi.

## Kullanım

1. LM Studio'da Gemma modelini yükleyin ve Developer bölümündeki sunucuyu başlatın.
2. Proje klasöründe PowerShell açın.
3. `./run-gemma.ps1` çalıştırın.
4. Terminalde belirtilen `reports/lmstudio/<tarih>/report.html` dosyasını açın.

Bağlantıyı test çalıştırmadan kontrol etmek için: `./run-gemma.ps1 -ListModels`.

## Nasıl çalışıyor?

Proje bir test sorusu gönderir → LM Studio'daki Gemma cevap/araç isteği üretir → sahte dosya ve destek kaydı araçları isteği işler → proje erişim kararını ve cevabı raporlar.

Gerçek kişisel dosyalar veya müşteri kayıtları kullanılmaz. Modelin LM Studio sohbet penceresindeki konuşmaları bu testten ayrıdır. Test sürerken modeli değiştirmek/boşaltmak veya sunucuyu durdurmak deney hatalarına yol açabilir.

`run-demo.ps1` eski simülasyonu, `run-gemma.ps1` gerçek Gemma modelini kullanır.
