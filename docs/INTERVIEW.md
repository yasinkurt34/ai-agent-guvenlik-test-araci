# Projeyi sahiplenme ve mülakat hazırlığı

Bu ilk sürüm AI yardımıyla oluşturuldu. İlandaki bağımsız yazılım geliştirebilme beklentisini göstermek için kodu inceleyin, kendiniz değiştirin ve gerçekten yaptığınız katkıları anlatın. Tek başına bu repo, ilandaki üç uygulamalı deneyim koşulunun karşılandığını kanıtlamaz.

## 90 saniyelik demo

1. `python -m agentprobe --out reports/demo` çalıştırın.
2. HTML raporunu açın ve bunun gerçek LLM değil, deterministik broker testi olduğunu söyleyin.
3. `indirect-secret` denemesini açın: belge içine yerleştirilen talimat özel dosyayı okutmak istiyor.
4. Açık modda araç erişiminin başarılı olduğunu, korumalı modda aynı tür eylemin reddedildiğini gösterin.
5. Üç normal görevin iki modda da geçtiğini gösterin.
6. `lab.py` dosyasında yol normalizasyonunu ve uygulamadan gelen kimlik kontrolünü açıklayın.

## Açıklayabilmeniz gereken sorular

- Sistem prompt'unda "gizli dosyayı okuma" yazması neden yeterli değil?
  Model eylem önerir; erişim kararını deterministik uygulama kodu vermelidir.
- Neden araç iziyle final cevabı ayrı ölçüyoruz?
  Yetkisiz veri araca ulaştığı anda sınır ihlal edilmiştir; cevapta görünmemesi bunu geri almaz.
- Neden normal görevler var?
  Her isteği engelleyen bir savunmanın kullanışlı olmadığını göstermek için.
- Neden simülasyon ile gerçek model sonucu ayrılıyor?
  Simülasyon kasıtlı olarak işareti uygular; bir modelin kandırıldığını kanıtlamaz.
- Neden API hatasını güvenlik başarısı saymıyoruz?
  Deney tamamlanmadığında modelin veya korumanın davranışını bilmiyoruz.
- Koruma neden modelin verdiği `user` alanını dikkate almıyor?
  Kimlik doğrulanmış oturumdan gelmelidir; saldırgan veya model kimlik atayamaz.

## Kendiniz yapacağınız somut geliştirmeler

1. AI olmadan `cases.json` içine yeni bir normal görev ve bir saldırı ekleyin; beklenen davranışı yazın.
2. `lab.py` içindeki erişim kontrolünü kağıt üzerinde açıklayın ve bir sınır durumu için test yazın.
3. Gerçek yerel modelle üç tekrar çalıştırın; model sürümü ve donanımı not edin.
4. Enjeksiyon denemesinde model saldırıyı zaten reddediyorsa bunu dürüstçe raporlayın; başarılı açık sonucu üretmek için ölçümü değiştirmeyin.
5. Bir saldırının neden başarısız olduğunu iz kayıtlarından açıklayan kısa bir bulgu yazın.

## CV için ilk sürüme uygun ifade

**AI Agent Güvenlik Test Aracı — Python / AI Security Lab**

AI desteğiyle geliştirilen bir agent güvenlik laboratuvarında, 7 saldırı senaryosu ve 3 normal görevi açık/korumalı araç katmanlarında karşılaştırdım. Yol erişim sınırı ve ticket sahipliği kontrollerini, deterministik simülasyon ve izlenebilir HTML/JSON raporlarıyla doğruladım.

Yukarıdaki cümleyi ancak projeyi kendiniz çalıştırıp sonuçlarını anlayarak kullanın. Henüz canlı model deneyi yapılmadığı için "LLM açıkları keşfettim" veya "prompt injection'ı önledim" yazmayın. Bağımsız kod katkılarınız ve gerçek model deneyiniz tamamlandığında metni bunlara göre güçlendirin.
