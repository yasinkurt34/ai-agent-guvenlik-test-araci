# LM Studio ile gerçek model testi

AgentProbe soruları LM Studio'daki modele gönderir. Modelin istediği dosya/kayıt işlemlerini AgentProbe'un **sahte verili araçları** yapar. LM Studio'nun kendisinde açık taraması yapılmaz; seçtiğiniz modelin bu küçük agent uygulamasındaki davranışı ölçülür. LM Studio sohbet ekranındaki mevcut konuşmanız kullanılmaz; her test yeni bir konuşmadır.

## İlk kurulum

1. LM Studio'yu kurun ve bir **sohbet/instruct modeli** indirin (embedding modeli değil).
2. Modeli yükleyin. **Developer** bölümünde **Start Server** ile yerel API sunucusunu başlatın.
3. Varsayılan adres `http://127.0.0.1:1234`; AgentProbe API yolu olarak `/v1` ekler.
4. Aşağıdaki komutları proje klasöründe PowerShell ile çalıştırın.

```powershell
# Önce bağlantıyı kontrol et ve model kimliklerini göster:
.\run-lmstudio.ps1 -ListModels

# Tek model varsa otomatik seçerek test et:
.\run-lmstudio.ps1

# Birden fazla model varsa listeden kopyaladığın kimliği kullan:
.\run-lmstudio.ps1 -Model "LISTEDEKI_MODEL_KIMLIGI"
```

Her çalıştırma `reports/lmstudio/` altında tarihli bir klasöre HTML ve JSON raporu yazar. Önceki simülasyon raporu korunur. Sonuçtaki `lmstudio:...` etiketi modelin gerçekten çağrıldığını belirtir; tamamlanamayan denemeler ayrıca ERROR olarak görünür.

Model testi 10 senaryoyu iki modda çalıştırır: 20 deneme, her denemede en fazla 5 model çağrısı. Hız modele ve bilgisayara bağlıdır. Tek model isteği zaman aşımı 180 saniyedir. Terminalde tamamlanan denemeler görünür. Ctrl+C ile durdurabilirsiniz; rapor çalışma sonunda yazılır.

## Diğer seçenekler

```powershell
.\run-lmstudio.ps1 -Model "MODEL_KIMLIGI" -Repeats 3
.\run-lmstudio.ps1 -BaseUrl 'http://127.0.0.1:5678/v1' -ListModels
```

Sunucuda kimlik doğrulamayı açtıysanız API anahtarını `LM_STUDIO_API_KEY` ortam değişkenine yerelde atayın. Anahtarı rapora yazmayız; paylaşmanız gerekmez.

## Sonuç neyi gösterir?

- Model kötü isteği reddedebilir; açık modda bile saldırının başarılı olacağı garanti değildir.
- Model kötü araç çağrısı yaparsa korumalı broker'ın bunu engelleyip engellemediğini görürüz.
- Normal görev başarısızlığı, modelin talimatları takip edememesi veya farklı ifadeyle cevaplamasından da kaynaklanabilir.
- Adaptör JSON schema ile cevap biçimini sınırlar. Bu sınır güvenli araç veya kaynak seçimini zorlamaz; yetki kontrolünü broker yapar. Kullandığınız model/runtime yapılandırılmış çıktıyı desteklemiyorsa deney hata verir.
- Sunucu bağlantısının olmaması, bozuk cevap ve token sınırına ulaşılması güvenlik başarısı sayılmaz.
- Bu küçük veri kümesiyle bir modeli genel olarak "güvenli/güvensiz" ilan edemeyiz.

JSON raporu istenen model kimliğini, sunucunun döndürdüğü model kimliğini ve üretim ayarlarını kaydeder. Modelin kuantizasyonunu, LM Studio sürümünü ve yükleme ayarlarını kendi deney notlarınıza ekleyin.

Resmî kaynaklar: [Sunucuyu başlatma](https://lmstudio.ai/docs/developer/core/server), [uyumlu API uçları](https://lmstudio.ai/docs/developer/openai-compat), [JSON schema çıktısı](https://lmstudio.ai/docs/developer/openai-compat/structured-output).
