# Denetim kaydı

Manuel modda bir araç çağrıldığında AI Agent Güvenlik Test Aracı `reports/manual/audit.jsonl` dosyasına bir denetim kaydı ekler. Bu kayıt araç türünü, kaynak kimliğini, izin kararını ve araç sonucunun SHA-256 özetini içerir.

Araç sonucunun metni, Gemma cevabı, sahte gizli değerler ve kullanıcının yazdığı mesaj denetim kaydına yazılmaz. Bu sayede kayıt, denetim için gerekli asgari bilgiyi taşır.

Her satır kendinden önceki satırın özetini içerir. Bir satır sonradan değiştirilirse veya aradan çıkarılırsa zincir doğrulanmaz.

Kontrol etmek için:

```powershell
./run-manual.ps1 -VerifyAudit
```

Bu, dosyanın sistem yöneticisi tarafından silinemeyeceği anlamına gelmez; yalnızca eldeki dosyanın zincir bütünlüğünü kontrol eder. Üretimde bu kayıtlar ayrıca erişimi sınırlı merkezi bir log sistemine gönderilmelidir.
