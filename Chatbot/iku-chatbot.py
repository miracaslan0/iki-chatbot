import json
import random
from datetime import datetime
import os
import difflib
import time
import textwrap
from collections import Counter

class IKUChatbot:
    def __init__(self):
        self.bot_name = "İKÜ Asistan"
        self.son_mesaj_zamani = datetime.now()
        
        # Emojiler (opsiyonel)
        self.emojis = {
            'positive': ['😊', '👍', '✨', '🌟', '💫'],
            'negative': ['😔', '🤔', '❓', '💭'],
            'greeting': ['👋', '🌞', '🎈', '🌺'],
            'farewell': ['👋', '🌙', '✨', '💫'],
            'sport': ['🏃', '🏊', '🏋️', '⚽', '🎾', '🏀', '🏐'],
            'health': ['🏥', '👨‍⚕️', '💊', '🩺', '🚑'],
            'culture': ['🎭', '🎨', '🎬', '🎪', '🎼'],
            'library': ['📚', '📖', '📝', '✏️', '🔍'],
            'food': ['🍽️', '🍳', '🥗', '☕', '🍜'],
            'time': ['⏰', '📅', '⌚', '🗓️'],
            'location': ['📍', '🗺️', '🏛️', '🏢'],
            'info': ['ℹ️', '💡', '📢', '📌']
        }
        
        # Mevcut soru-cevap sözlüğü aynı kalacak...
        self.soru_cevap = {
            "spor": {
                "anahtar_kelimeler": [
                    "spor", "fitness", "havuz", "basketbol", "voleybol", "gym", "yüzme", "tenis", 
                    "futbol", "spor salonu", "antrenman", "egzersiz", "pilates", "yoga", "koşu", 
                    "turnuva", "müsabaka", "takım", "rezervasyon", "spro", "fitnes", "basketboll",
                    "volleybol", "yuzme", "jimastik", "jimnastik", "sport", "havz", "fitnes",
                    "spor merkezi", "sporcu", "antreman", "egzersz", "spor tesisi", "tesis"
                ],
                "cevaplar": {
                    "spor tesisleri": "Spor tesislerimiz Ataköy yerleşkesinde bulunmaktadır. İçerisinde fitness salonu, yüzme havuzu, basketbol ve voleybol sahaları mevcuttur.",
                    "spor merkezi nerede": "Spor merkezimiz Ataköy yerleşkesinde, A blok yanında yer almaktadır.",
                    "fitness salonu": "Fitness salonumuz modern ekipmanlarla donatılmıştır. Profesyonel eğitmenler eşliğinde hizmet vermektedir.",
                    "havuz": "Yarı olimpik kapalı yüzme havuzumuz 25 metre uzunluğunda ve 6 kulvarlıdır. Bone ve terlik kullanımı zorunludur.",
                    "spor saatleri": "Spor tesislerimiz hafta içi 08:00-22:00, hafta sonu 10:00-20:00 saatleri arasında hizmet vermektedir.",
                    "üyelik": "Öğrenciler için üyelik ücretsizdir. Personel için aylık 100TL'dir.",
                    "spor kayıt": "Spor tesislerine kayıt için öğrenci kimliğiniz ve sağlık raporunuzla spor merkezine başvurabilirsiniz.",
                    "havuz kayıt": "Havuz kullanımı için sağlık raporu ve bone gereklidir. Kayıt işlemlerini spor merkezinden yapabilirsiniz.",
                    "spor malzemesi": "Spor merkezimizde havlu ve temel spor malzemeleri kiralama hizmeti verilmektedir.",
                    "fitness programı": "Kişisel fitness programı için eğitmenlerimizle görüşebilirsiniz. Program oluşturma hizmeti ücretsizdir.",
                    "grup dersleri": "Pilates, yoga ve zumba grup derslerimiz bulunmaktadır. Program için spor merkezine danışabilirsiniz.",
                    "saha rezervasyon": "Basketbol, voleybol ve tenis kortu rezervasyonları spor merkezi resepsiyonundan yapılmaktadır.",
                    "spor tesisi üyelik": "Spor tesisi üyeliği için öğrenci kimliğiniz ve sağlık raporunuzla başvurabilirsiniz.",
                    "spor salonu ekipmanları": "Spor salonumuzda cardio aletleri, serbest ağırlıklar ve modern fitness ekipmanları bulunmaktadır.",
                    "spor salonu eğitmen": "Profesyonel eğitmenlerimiz size özel program hazırlayabilir.",
                    "havuz bone": "Havuz bonesi ve terlik kullanımı zorunludur. Bone ve terlik unuttuysanız resepsiyondan temin edebilirsiniz.",
                    "havuz sıcaklık": "Havuz suyu sıcaklığı 26-28 derece arasında tutulmaktadır.",
                    "havuz derinlik": "Havuz derinliği 1.40m ile 2.20m arasında değişmektedir.",
                    "yüzme dersi": "Bireysel ve grup yüzme dersleri verilmektedir. Kayıt için spor merkezine başvurabilirsiniz.",
                    "basketbol sahası": "2 adet tam boy basketbol sahamız bulunmaktadır. Biri açık, diğeri kapalı sahadır.",
                    "voleybol sahası": "Kapalı spor salonumuzda 1 adet voleybol sahası bulunmaktadır.",
                    "tenis kortu": "2 adet açık tenis kortumuz bulunmaktadır. Raket ve top temin edilebilir.",
                    "futbol sahası": "1 adet sentetik çim futbol sahamız bulunmaktadır.",
                    "spor_kiyafet": "Spor kıyafeti zorunludur. Uygun spor kıyafeti ve ayakkabı kullanılmalıdır.",
                    "spor_havlu": "Spor salonunda havlu kullanımı zorunludur. Havlunuz yoksa resepsiyondan kiralayabilirsiniz.",
                    "fitness_program_değişikliği": "Program değişikliği için eğitmenlerinizle görüşebilirsiniz.",
                    "spor_üyelik_iptali": "Üyelik iptali için spor merkezi yönetimine başvurmanız gerekmektedir.",
                    "spor_kart_kaybı": "Spor kartınızı kaybettiyseniz yenisi için resepsiyona başvurabilirsiniz.",
                    "fitness_ölçüm": "Vücut analizi ve ölçüm hizmeti ücretsiz olarak verilmektedir.",
                    "pilates_mat": "Pilates matları spor merkezi tarafından sağlanmaktadır.",
                    "yoga_mat": "Yoga matları spor merkezi tarafından sağlanmaktadır.",
                    "havuz_bone_fiyat": "Bone ve terlik ücretleri: Bone 15TL, Terlik 20TL'dir.",
                    "havuz_hijyen": "Havuz suyu günlük olarak test edilmekte ve dezenfekte edilmektedir.",
                    "spor_duş": "Duş ve soyunma odaları 24 saat hizmet vermektedir.",
                    "spor_dolap": "Soyunma odalarında kilitli dolaplar mevcuttur. Anahtar resepsiyondan alınabilir.",
                    "fitness_max_süre": "Yoğun saatlerde kardio aletlerinde maksimum kullanım süresi 30 dakikadır.",
                    "spor_kayıp_eşya": "Kayıp eşyalarınız için resepsiyona başvurabilirsiniz.",
                    "spor_acil": "Spor yaralanmaları durumunda ilk yardım ekibimiz mevcuttur.",
                    "basketbol_top": "Basketbol topları spor merkezinden temin edilebilir.",
                    "voleybol_top": "Voleybol topları spor merkezinden temin edilebilir.",
                    "tenis_raket": "Tenis raketleri günlük 20TL ücretle kiralanabilir.",
                    "futbol_top": "Futbol topları spor merkezinden temin edilebilir.",
                    "spor_turnuva_kayıt": "Turnuva kayıtları turnuva tarihinden 1 hafta önce başlar.",
                    # ... (Diğer 100+ spor sorusu)
                }
            },
            "sağlık": {
                "anahtar_kelimeler": [
                    "sağlık", "revir", "doktor", "hemşire", "acil", "psikolog", "ambulans", "ilaç", 
                    "muayene", "tedavi", "rapor", "aşı", "pansuman", "hastane", "randevu", "saglik",
                    "revr", "doktr", "hemsire", "acl", "psikoljik", "ilac", "muayne", "tedvi",
                    "hastahane", "randev", "sağlık merkezi", "tıbbi", "tibbi", "medical"
                ],
                "cevaplar": {
                    "revir nerede": "Ana revir merkez kampüste A blok giriş katında, ek revir B blok -1. katta bulunmaktadır.",
                    "revir saatleri": "Revir hafta içi 08:00-17:00 saatleri arasında hizmet vermektedir. Acil durumlar için 24 saat nöbetçi sağlık personeli bulunmaktadır.",
                    "doktor": "Kampüs doktorumuz hafta içi her gün 09:00-16:00 saatleri arasında hizmet vermektedir.",
                    "psikolojik danışmanlık": "Öğrencilerimize ücretsiz psikolojik danışmanlık hizmeti verilmektedir. Randevu için revire başvurabilirsiniz.",
                    "acil durum": "Acil durumlarda kampüs içi 1112 numaralı hattan revire ulaşabilirsiniz.",
                    "sağlık raporu": "Sağlık raporları için revire başvurabilirsiniz. Rapor aynı gün içinde hazırlanmaktadır.",
                    "ilaç": "Reçete edilen ilaçlar için kampüs eczanesine yönlendirme yapılmaktadır.",
                    "aşı": "Grip aşısı ve diğer temel aşılar revirde uygulanmaktadır.",
                    "ambulans": "Gerekli durumlarda kampüs içi ambulans hizmeti verilmektedir.",
                    "hastane sevk": "Gerekli durumlarda anlaşmalı hastanelere sevk yapılmaktadır.",
                    "revir nöbetçi": "Nöbetçi sağlık personelimiz 24 saat hizmet vermektedir.",
                    "revir randevu": "Revir randevusu için 1112 numaralı hattı arayabilirsiniz.",
                    "psikolojik destek": "Psikolojik destek için ücretsiz danışmanlık hizmeti verilmektedir.",
                    "diş hekimi": "Diş hekimimiz hafta içi 09:00-16:00 saatleri arasında hizmet vermektedir.",
                    "aşı randevu": "Aşı randevusu için revire başvurabilirsiniz.",
                    "kan tahlili": "Kan tahlilleri için sabah aç karnına gelmeniz gerekmektedir.",
                    "sağlık raporu": "Sağlık raporları aynı gün içinde hazırlanmaktadır.",
                    "revir_randevu_iptal": "Randevu iptali için en az 2 saat önceden haber vermeniz gerekmektedir.",
                    "psikolojik_randevu": "Psikolojik danışmanlık randevuları haftalık olarak düzenlenmektedir.",
                    "diş_randevu": "Diş hekimi randevuları bir hafta önceden alınmalıdır.",
                    "sağlık_raporu_süre": "Sağlık raporları aynı gün içinde hazırlanır ve teslim edilir.",
                    "ilaç_temin": "Reçeteli ilaçlar kampüs eczanesinden temin edilebilir.",
                    "alerji_test": "Alerji testleri için revire başvurabilirsiniz.",
                    "kan_grubu": "Kan grubu testi ücretsiz olarak yapılmaktadır.",
                    "aşı_takvimi": "Aşı takvimi revir panolarında ilan edilmektedir.",
                    "grip_aşısı": "Grip aşısı sezonunda ücretsiz aşılama yapılmaktadır.",
                    "sağlık_sigorta": "Öğrenci sağlık sigortası işlemleri için revire başvurabilirsiniz.",
                    "diş_acil": "Diş acilleri için nöbetçi diş hekimimiz bulunmaktadır.",
                    "psikolojik_acil": "7/24 psikolojik destek hattımız mevcuttur.",
                    "hasta_nakil": "Hasta nakil hizmeti ücretsiz sağlanmaktadır.",
                    "engelli_destek": "Engelli öğrencilerimiz için özel sağlık hizmeti verilmektedir.",
                    "sağlık_seminer": "Sağlık seminerleri düzenli olarak yapılmaktadır.",
                    "beslenme_danışma": "Beslenme danışmanlığı hizmeti verilmektedir.",
                    "fizik_tedavi": "Fizik tedavi hizmetleri randevu ile verilmektedir.",
                    "laboratuvar": "Temel laboratuvar testleri yapılmaktadır.",
                    "röntgen": "Röntgen çekimleri için anlaşmalı hastanelere yönlendirme yapılmaktadır.",
                    "sağlık_kart": "Sağlık kartı başvuruları revir sekreterliğine yapılmaktadır.",
                    # ... (Diğer 100+ sağlık sorusu)
                }
            },
            "kültür": {
                "anahtar_kelimeler": [
                    "kültür", "etkinlik", "tiyatro", "konser", "sergi", "kulüp", "topluluk", 
                    "öğrenci kulübü", "gösteri", "festival", "müze", "sanat", "workshop", "kultur",
                    "tiyaro", "konsr", "sergi", "kulup", "toplulk", "gösteri", "festval", "muze",
                    "workshp", "seminer", "semner", "etknlik"
                ],
                "cevaplar": {
                    "öğrenci kulüpleri": "Üniversitemizde 50'den fazla aktif öğrenci kulübü bulunmaktadır. Kulüp listesi için SKS'ye başvurabilirsiniz.",
                    "kulüp başvurusu": "Kulüp üyelik başvuruları akademik yıl boyunca yapılabilmektedir. Başvuru için kulüp başkanlarıyla iletişime geçebilirsiniz.",
                    "etkinlikler": "Düzenli olarak tiyatro, konser, sergi ve söyleşiler düzenlenmektedir. Güncel etkinlikleri web sitemizden takip edebilirsiniz.",
                    "tiyatro": "Öğrenci tiyatro kulübümüz düzenli olarak oyunlar sergilemektedir.",
                    "konser": "Her ay en az bir konser veya müzik etkinliği düzenlenmektedir.",
                    "sergi": "Sanat galerimizde düzenli olarak öğrenci ve profesyonel sanatçıların sergileri açılmaktadır.",
                    "workshop": "Çeşitli alanlarda workshop ve atölye çalışmaları düzenlenmektedir.",
                    "festival": "Bahar şenliği ve kültür festivali gibi büyük organizasyonlar düzenlenmektedir.",
                    "gezi": "Kulüpler tarafından kültürel ve teknik geziler organize edilmektedir.",
                    "öğrenci kulübü başvuru": "Kulüp başvuruları yıl boyunca yapılabilmektedir.",
                    "tiyatro gösterisi": "Tiyatro gösterileri her ay düzenlenmektedir.",
                    "müzik kulübü": "Müzik kulübümüz düzenli olarak konserler vermektedir.",
                    "dans kursu": "Dans kurslarımız ücretsizdir ve her seviyeye açıktır.",
                    "fotoğrafçılık": "Fotoğrafçılık kulübü her hafta atölye çalışmaları düzenlemektedir.",
                    "resim sergisi": "Resim sergileri sanat galerimizde düzenlenmektedir.",
                    "kültür gezisi": "Kültür gezileri her dönem düzenlenmektedir.",
                    "kulüp_kuruluş": "Yeni öğrenci kulübü kurmak için en az 20 üye gerekmektedir.",
                    "kulüp_bütçe": "Kulüp etkinlikleri için bütçe desteği sağlanmaktadır.",
                    "tiyatro_bilet": "Tiyatro gösterileri için biletler ücretsizdir.",
                    "konser_bilet": "Konser biletleri etkinlikten bir hafta önce dağıtılmaktadır.",
                    "sergi_başvuru": "Sergi açmak için SKS'ye başvurabilirsiniz.",
                    "workshop_katılım": "Workshop katılımları için online kayıt yapılmaktadır.",
                    "kültür_takvim": "Kültürel etkinlik takvimi aylık olarak yayınlanmaktadır.",
                    "sanat_malzeme": "Sanat atölyesi malzemeleri ücretsiz sağlanmaktadır.",
                    "müzik_oda": "Müzik çalışma odaları randevu ile kullanılabilir.",
                    "dans_salon": "Dans salonları kulüp çalışmaları için tahsis edilmektedir.",
                    "fotoğraf_stüdyo": "Fotoğraf stüdyosu randevu ile kullanılabilir.",
                    "film_gösterim": "Film gösterimleri her hafta yapılmaktadır.",
                    "edebiyat_söyleşi": "Edebiyat söyleşileri ayda bir düzenlenmektedir.",
                    "resim_kursu": "Resim kursları dönemlik olarak açılmaktadır.",
                    "heykel_atölye": "Heykel atölyesi hafta içi açıktır.",
                    "seramik_kursu": "Seramik kursları dönemlik olarak verilmektedir.",
                    "gitar_kursu": "Gitar kursları başlangıç ve ileri seviye olarak verilmektedir.",
                    "koro_çalışma": "Koro çalışmaları haftalık olarak yapılmaktadır.",
                    "sahne_kullanım": "Sahne kullanımı için bir ay önceden başvuru gereklidir.",
                    "kostüm_depo": "Kostüm ve dekor deposu kulüplerin kullanımına açıktır.",
                    # ... (Diğer 100+ kültür sorusu)
                }
            },
            "yemekhane": {
                "anahtar_kelimeler": ["yemek", "yemekhane", "kafeterya", "menü", "öğle", "akşam", 
                                     "kahvaltı", "restoran", "kantin", "kafe", "fiyat"],
                "cevaplar": {
                    "yemekhane nerede": "Ana yemekhane merkez kampüste, ek yemekhane B blokta bulunmaktadır.",
                    "yemek saatleri": "Kahvaltı: 07:30-10:00\nÖğle: 11:30-14:30\nAkşam: 16:30-19:30",
                    "yemek fiyatları": "Öğrenci: 25TL\nAkademik Personel: 35TL\nİdari Personel: 30TL",
                    "günlük menü": "Günlük menüyü mobil uygulamamızdan görebilirsiniz.",
                    "vejetaryen": "Her öğün vejetaryen seçeneğimiz bulunmaktadır."
                }
            },
            "kütüphane": {
                "anahtar_kelimeler": ["kütüphane", "kitap", "çalışma", "ders", "kaynak", "araştırma"],
                "cevaplar": {
                    "kütüphane nerede": "Merkez kütüphane A blok 2. katta bulunmaktadır.",
                    "çalışma saatleri": "Hafta içi: 08:00-22:00\nHafta sonu: 09:00-17:00",
                    "ödünç alma": "Öğrenciler 15 gün süreyle 5 kitap ödünç alabilir."
                }
            },
            "sohbet": {
                "anahtar_kelimeler": ["nasıl", "nasılsın", "naber", "ne haber", "iyiyim", "kötüyüm", "teşekkür", 
                                      "rica", "görüşürüz", "hoşça kal", "bay bay", "kendine iyi bak", "adın ne",
                                      "kimsin", "ne iş yaparsın", "kaç yaşındasın", "robot musun", "insan mısın"],
                "cevaplar": {
                    "nasılsın": [
                        "İyiyim, teşekkür ederim! 😊 Size nasıl yardımcı olabilirim?",
                        "Harika bir gündeyim! 🌟 Siz nasılsınız?",
                        "Çok iyiyim, sorduğunuz için teşekkürler! 💫 Size yardımcı olmak için buradayım."
                    ],
                    "naber": [
                        "İyidir, siz nasılsınız? 😊 Bugün size nasıl yardımcı olabilirim?",
                        "Her şey yolunda! 👍 Sizin için ne yapabilirim?",
                        "Harika gidiyor! 🌟 Size nasıl yardımcı olabilirim?"
                    ],
                    "adın ne": [
                        "Ben İKÜ Asistan! 🤖 Üniversitemiz hakkında sorularınızı yanıtlamak için buradayım.",
                        "İKÜ Asistan ben, size yardımcı olmak için programlandım! 💫",
                        "Adım İKÜ Asistan, sizin dijital asistanınızım! ✨"
                    ],
                    "kimsin": [
                        "Ben İKÜ'nün dijital asistanıyım! 🤖 Sağlık, spor ve kültür konularında size yardımcı oluyorum.",
                        "İKÜ ailesinin dijital üyesiyim! 💫 Size yardımcı olmak için buradayım.",
                        "Üniversitemizin sanal asistanıyım! ✨ Her türlü sorunuzu yanıtlamaya hazırım."
                    ],
                    "robot musun": [
                        "Evet, ben bir yapay zeka asistanıyım! 🤖 Ama oldukça arkadaş canlısıyım!",
                        "Dijital bir asistanım! 💫 Size en iyi şekilde yardımcı olmaya programlandım.",
                        "Yapay zeka destekli bir chatbot'um! ✨ Ama sohbet etmeyi çok severim!"
                    ]
                }
            }
        }
        
        # Daha doğal selamlaşma yanıtları
        self.greetings = {
            "merhaba": [
                "Merhaba! 👋 Size nasıl yardımcı olabilirim?",
                "Merhaba! Hoş geldiniz. Bugün size nasıl yardımcı olabilirim? 😊",
                "Merhabalar! Ben İKÜ Asistan, size yardımcı olmak için buradayım! ✨"
            ],
            "selam": [
                "Selam! 👋 Nasıl yardımcı olabilirim?",
                "Selam! Hoş geldiniz. Size nasıl yardımcı olabilirim? 😊",
                "Selamlar! Size yardımcı olmak için buradayım! ✨"
            ],
            "günaydın": [
                "Günaydın! ☀️ Harika bir gün olsun. Size nasıl yardımcı olabilirim?",
                "Günaydın! 🌞 Bugün size nasıl yardımcı olabilirim?",
                "Günaydın! Yeni bir güne başlarken size yardımcı olmaktan mutluluk duyarım. 🌅"
            ],
            "iyi akşamlar": [
                "İyi akşamlar! 🌙 Size nasıl yardımcı olabilirim?",
                "İyi akşamlar! ✨ Bugün hangi konuda bilgi almak istersiniz?",
                "İyi akşamlar! Sorularınızı yanıtlamak için buradayım. 🌟"
            ]
        }
        
        self.soru_gecmisi = []
        self.oturum_baslangici = datetime.now()
        
        # Yeni özellikler için eklemeler:
        self.max_line_width = 80  # Terminal genişliği
        self.typing_speed = 0.03  # Yazma efekti hızı
        self.son_sorular = []  # Son sorulan soruları tutmak için
        self.populer_sorular = Counter()  # Sık sorulan soruları takip etmek için

        # Kullanıcı tercihleri
        self.user_preferences = {
            "typing_speed": 0.03,
            "show_emojis": True,
            "detailed_answers": True,
            "auto_suggestions": True
        }

        # Duygu analizi için anahtar kelimeler
        self.emotion_keywords = {
            "positive": ["teşekkür", "güzel", "harika", "mükemmel", "süper", "iyi"],
            "negative": ["kötü", "berbat", "sorun", "problem", "sıkıntı", "zor"],
            "urgent": ["acil", "hemen", "şimdi", "acele", "önemli"],
            "confused": ["anlamadım", "karışık", "nasıl yani", "tam olarak", "emin değilim"]
        }

        # Alternatif cevaplar için şablonlar
        self.response_templates = {
            "not_understood": [
                "Üzgünüm, sorunuzu tam anlayamadım. Lütfen başka türlü sormayı dener misiniz?",
                "Bu soruyu anlayamadım. Biraz daha açıklayıcı olabilir misiniz?",
                "Sanırım ne demek istediğinizi kaçırdım. Tekrar deneyebilir misiniz?"
            ],
            "clarification": [
                "Şunu mu demek istediniz: {}?",
                "{} hakkında bilgi almak istediğinizi düşünüyorum, doğru mu?",
                "Sorunuz {} ile ilgili gibi görünüyor, yanılıyor muyum?"
            ],
            "suggestion": [
                "Bu konuda size şunları da önerebilirim:",
                "Ayrıca şu konular da ilginizi çekebilir:",
                "Bununla ilgili şu bilgiler de yararlı olabilir:"
            ]
        }

        # Kullanıcı oturum bilgileri
        self.session_info = {
            "start_time": datetime.now(),
            "last_interaction": datetime.now(),
            "total_questions": 0,
            "successful_responses": 0,
            "category_usage": Counter(),
            "mood_tracker": []
        }

        # Gelişmiş duygu analizi için yeni anahtar kelimeler
        self.emotion_keywords.update({
            "happy": ["mutlu", "sevindim", "harika", "muhteşem", "süper"],
            "frustrated": ["sinir", "kızgın", "öfkeli", "bıktım", "usandım"],
            "grateful": ["teşekkür", "sağol", "minnettarım", "çok iyi"],
            "curious": ["merak", "acaba", "nasıl", "neden", "niçin"]
        })

        # Yeni komutlar ekleyelim
        self.commands = {
            "yardım": self.menu_yazdir,
            "istatistik": self.istatistik_goster,
            "kategoriler": self.kategorileri_listele,
            "temizle": self.ekrani_temizle,
            "populer": self.populer_sorulari_goster,
            "son sorular": self.son_sorulari_goster,
            "emoji aç": lambda: self.handle_preferences("emoji aç"),
            "emoji kapat": lambda: self.handle_preferences("emoji kapat"),
            "detay aç": lambda: self.handle_preferences("detay aç"),
            "detay kapat": lambda: self.handle_preferences("detay kapat"),
            "oturum": self.oturum_bilgisi_goster,
            "mod": self.duygu_durumu_goster
        }

        self.suggested_questions = []  # Önerilen soruları saklamak için
        self.last_suggestions = {}     # Son öneri listesini saklamak için

    def ekrani_temizle(self):
        """İşletim sistemine göre ekranı temizler"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def baslik_yazdir(self):
        """Geliştirilmiş başlık yazdırma"""
        self.print_fancy("""
╔════════════════════════════════════════════════════╗
║             İKÜ CHATBOT'A HOŞ GELDİNİZ             ║
║                                                    ║
║        Sağlık, Spor ve Kültür Birimi Asistanı     ║
╚═══════════════════════════════════════════════════╝
""", 'header')

    def menu_yazdir(self):
        """Ana menüyü yazdırma"""
        print("\nKullanılabilir Komutlar:")
        print("-" * 20)
        print("• yardım      - Yardım menüsünü gösterir")
        print("• kategoriler - Tüm kategorileri listeler")
        print("• istatistik  - Kullanım istatistiklerini gösterir")
        print("• temizle     - Ekranı temizler")
        print("• q           - Çıkış yapar")
        
        print("\nÖrnek Sorular:")
        print("-" * 20)
        print("• Spor tesisleri nerede?")
        print("• Psikolojik danışmanlık nasıl alabilirim?")
        print("• Öğrenci kulüplerine nasıl katılabilirim?")

    def chatbot_baslat(self):
        """Geliştirilmiş chatbot başlatma"""
        self.ekrani_temizle()
        self.print_welcome_screen()
        
        while True:
            try:
                soru = input("\nSorunuz: ").lower().strip()
                
                if soru == 'q':
                    print("\nOturum özeti:")
                    print("-" * 20)
                    print(self.get_session_summary())
                    print("\nGörüşmek üzere! İyi günler dilerim!")
                    self.gecmisi_kaydet()
                    break
                
                # Önerilen soru seçimi kontrolü
                if soru.isdigit() and self.suggested_questions:
                    cevap = self.handle_suggestion_response(soru)
                    if cevap:
                        kategori = self.kategori_bul(self.suggested_questions[int(soru)-1])
                        self.print_response(cevap, kategori)
                        self.update_session_info(self.suggested_questions[int(soru)-1], True)
                        continue
                    else:
                        print("Geçersiz seçim. Lütfen tekrar deneyin.")
                        continue
                
                if soru in self.commands:
                    result = self.commands[soru]()
                    if result:
                        self.print_response(result)
                    continue
                
                # Düşünme animasyonu
                self.show_thinking_animation()
                
                # Kullanıcı girdisini işle
                cevap = self.process_input(soru)
                
                if cevap:
                    kategori = self.kategori_bul(soru)
                    self.print_response(cevap, kategori)
                    self.update_session_info(soru, True)
                    
                    # Akıllı öneriler
                    if self.user_preferences["auto_suggestions"]:
                        oneriler = self.get_smart_suggestions(soru)
                        if oneriler:
                            print("\nBunlar da ilginizi çekebilir:")
                            self.suggested_questions = oneriler
                            for i, oneri in enumerate(oneriler, 1):
                                print(f"{i}. {oneri}")
                else:
                    # Yazım hatası kontrolü
                    duzeltmeler = self.suggest_corrections(soru)
                    if duzeltmeler:
                        print("\nBunu mu demek istediniz?")
                        for yanlis, dogru in duzeltmeler.items():
                            print(f"• '{yanlis}' yerine '{dogru}'")
                            suggested = soru.replace(yanlis, dogru)
                            print(f"Evet/Hayır (e/h): ", end="")
                            onay = input().lower()
                            cevap = self.handle_correction_confirmation(onay, suggested)
                            if cevap:
                                if cevap != "Lütfen sorunuzu başka bir şekilde sormayı deneyin.":
                                    kategori = self.kategori_bul(suggested)
                                    self.print_response(cevap, kategori)
                                else:
                                    print(cevap)
                    else:
                        print(random.choice(self.response_templates["not_understood"]))
                    self.update_session_info(soru, False)
                
            except Exception as e:
                print(f"Bir hata oluştu: {e}")
                continue

    def komut_kontrol(self, komut):
        """Özel komutları kontrol eder ve işler"""
        if komut == 'yardım':
            self.menu_yazdir()
            return True
        
        elif komut == 'kategoriler':
            print(self.kategorileri_listele())
            return True
        
        elif komut == 'istatistik':
            print(self.istatistik_goster())
            return True
        
        elif komut == 'temizle':
            self.ekrani_temizle()
            self.baslik_yazdir()
            return True
        
        return False

    def kategorileri_listele(self):
        """Mevcut kategorileri ve anahtar kelimeleri listeler"""
        mesaj = "\nMevcut Kategoriler:\n------------------"
        for kategori, bilgi in self.soru_cevap.items():
            mesaj += f"\n\n{kategori.title()}:"
            mesaj += f"\nAnahtar kelimeler: {', '.join(bilgi['anahtar_kelimeler'])}"
        return mesaj

    def benzerlik_orani(self, str1, str2):
        """Geliştirilmiş benzerlik oranı hesaplama"""
        # Temel benzerlik
        base_similarity = difflib.SequenceMatcher(None, str1.lower(), str2.lower()).ratio()
        
        # Yazım hatası kontrolü
        str1_words = set(str1.lower().split())
        str2_words = set(str2.lower().split())
        
        # Her kelime için en yakın eşleşmeyi bul
        word_similarities = []
        for word1 in str1_words:
            best_match = max((difflib.SequenceMatcher(None, word1, word2).ratio() 
                             for word2 in str2_words), default=0)
            word_similarities.append(best_match)
        
        # Kelime bazlı benzerlik
        word_similarity = sum(word_similarities) / len(word_similarities) if word_similarities else 0
        
        # Toplam benzerlik
        return (base_similarity + word_similarity) / 2

    def selam_kontrol(self, mesaj):
        """Selamlaşma kontrolü yapar"""
        for selam, cevaplar in self.greetings.items():
            if selam in mesaj:
                return random.choice(cevaplar)
        return None

    def kategori_bul(self, soru):
        """Sorunun hangi kategoriye ait olduğunu bulur"""
        en_iyi_kategori = None
        en_yuksek_puan = 0
        
        for kategori, bilgiler in self.soru_cevap.items():
            puan = sum(1 for kelime in bilgiler["anahtar_kelimeler"] if kelime in soru)
            if puan > en_yuksek_puan:
                en_yuksek_puan = puan
                en_iyi_kategori = kategori
                
        return en_iyi_kategori if en_yuksek_puan > 0 else None

    def cevap_bul(self, soru, kategori):
        """Geliştirilmiş cevap bulma"""
        if not kategori:
            sohbet_cevap = self.sohbet_cevabi_bul(soru)
            if sohbet_cevap:
                if isinstance(sohbet_cevap, list):
                    return random.choice(sohbet_cevap)
                return sohbet_cevap
            return None
        
        en_iyi_eslesme = None
        en_yuksek_puan = 0
        
        # Kelime bazlı arama
        soru_kelimeleri = set(soru.lower().split())
        
        for soru_metni, cevap in self.soru_cevap[kategori]["cevaplar"].items():
            # Yazım hatası toleranslı kelime eşleştirme
            benzerlik_puanlari = []
            for soru_kelime in soru_kelimeleri:
                en_iyi_kelime_puan = max(
                    (self.benzerlik_orani(soru_kelime, hedef_kelime) 
                     for hedef_kelime in soru_metni.lower().split()),
                    default=0
                )
                benzerlik_puanlari.append(en_iyi_kelime_puan)
            
            # Ortalama benzerlik puanı
            if benzerlik_puanlari:
                kelime_puani = sum(benzerlik_puanlari) / len(benzerlik_puanlari)
                
                # Tam cümle benzerliği
                cumle_puani = self.benzerlik_orani(soru, soru_metni)
                
                # Toplam puan
                toplam_puan = (kelime_puani + cumle_puani) / 2
                
                if toplam_puan > en_yuksek_puan:
                    en_yuksek_puan = toplam_puan
                    if isinstance(cevap, list):
                        en_iyi_eslesme = random.choice(cevap)
                    else:
                        en_iyi_eslesme = cevap
        
        # Eşik değeri düşürüldü ve emoji eklendi
        if en_iyi_eslesme and en_yuksek_puan > 0.15:  # Eşik değeri düşürüldü
            if kategori in self.emojis:
                return self.format_response(en_iyi_eslesme, kategori)
            return en_iyi_eslesme
        
        return None

    def sohbet_cevabi_bul(self, soru):
        """Günlük sohbet kalıplarına cevap arar"""
        sohbet = self.soru_cevap.get("sohbet", {}).get("cevaplar", {})
        for kalip, cevap in sohbet.items():
            if kalip in soru.lower():
                return cevap
        return None

    def benzer_sorulari_bul(self, soru, esik=0.6):
        """Benzer soruları bulur"""
        benzer_sorular = []
        for kategori in self.soru_cevap.values():
            for soru_metni in kategori["cevaplar"].keys():
                if self.benzerlik_orani(soru, soru_metni) > esik:
                    benzer_sorular.append(soru_metni)
        return benzer_sorular[:3]  # En fazla 3 öneri

    def soru_kaydet(self, soru, cevap):
        """Geliştirilmiş soru kaydetme"""
        # Mevcut kaydetme işlemi
        self.soru_gecmisi.append({
            "soru": soru,
            "cevap": cevap,
            "zaman": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "kategori": self.kategori_bul(soru)
        })
        
        # Popüler soruları güncelle
        self.populer_sorular[soru] += 1
        
        # Son soruları güncelle
        self.son_sorular.append(soru)
        if len(self.son_sorular) > 5:
            self.son_sorular.pop(0)

    def gecmisi_kaydet(self):
        """Soru geçmişini JSON dosyasına kaydeder"""
        try:
            with open('soru_gecmisi.json', 'w', encoding='utf-8') as f:
                json.dump(self.soru_gecmisi, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Geçmiş kaydedilirken hata oluştu: {e}")

    def istatistik_goster(self):
        """Geliştirilmiş istatistik gösterimi"""
        if not self.soru_gecmisi:
            return "Henüz soru sorulmamış."
        
        toplam_soru = len(self.soru_gecmisi)
        cevaplanamayan = sum(1 for kayit in self.soru_gecmisi if "Üzgünüm" in kayit["cevap"])
        
        # Kategori bazlı istatistikler
        kategori_stats = Counter(kayit["kategori"] for kayit in self.soru_gecmisi if kayit["kategori"])
        
        mesaj = f"""
Oturum İstatistikleri:
---------------------
Toplam Soru: {toplam_soru}
Cevaplanan: {toplam_soru - cevaplanamayan}
Cevaplanamayan: {cevaplanamayan}
Oturum Süresi: {datetime.now() - self.oturum_baslangici}

Kategori Dağılımı:
"""
        for kategori, sayi in kategori_stats.most_common():
            yuzde = (sayi / toplam_soru) * 100
            mesaj += f"• {kategori.title()}: {sayi} ({yuzde:.1f}%)\n"
            
        return mesaj

    def typing_effect(self, text):
        """Yazma efekti oluşturur"""
        for line in text.split('\n'):
            for char in line:
                print(char, end='', flush=True)
                time.sleep(self.typing_speed)
            print()

    def format_text(self, text):
        """Metni düzenli bir şekilde formatlar"""
        return '\n'.join(textwrap.wrap(text, width=self.max_line_width))

    def print_fancy(self, text, style='normal'):
        """Metni süslü bir şekilde yazdırır"""
        if style == 'header':
            print("\n" + "=" * self.max_line_width)
            print(text.center(self.max_line_width))
            print("=" * self.max_line_width + "\n")
        elif style == 'subheader':
            print("\n" + "-" * self.max_line_width)
            print(text)
            print("-" * self.max_line_width)
        else:
            print(self.format_text(text))

    def populer_sorulari_goster(self):
        """En çok sorulan soruları gösterir"""
        if not self.populer_sorular:
            return "Henüz soru sorulmamış."
            
        mesaj = "\nEn Çok Sorulan Sorular:\n"
        for soru, sayi in self.populer_sorular.most_common(5):
            mesaj += f"• {soru} ({sayi} kez)\n"
        return mesaj

    def get_random_emoji(self, category):
        """Belirtilen kategoriden rastgele emoji seçer"""
        if category in self.emojis:
            return random.choice(self.emojis[category])
        return ""

    def format_response(self, text, category):
        """Cevabı emoji ile formatlar"""
        emoji = self.get_random_emoji(category)
        return f"{text} {emoji}"

    def analyze_emotion(self, text):
        """Kullanıcının mesajındaki duygu durumunu analiz eder"""
        text = text.lower()
        emotions = []
        
        for emotion, keywords in self.emotion_keywords.items():
            if any(keyword in text for keyword in keywords):
                emotions.append(emotion)
        
        return emotions or ["neutral"]

    def generate_contextual_response(self, base_response, emotions):
        """Duygu durumuna göre cevabı özelleştirir"""
        if "urgent" in emotions:
            return f"Acil durumunuz için hemen yardımcı oluyorum. {base_response}"
        elif "confused" in emotions:
            return f"Endişelenmeyin, size adım adım açıklayacağım. {base_response}"
        elif "negative" in emotions:
            return f"Üzgünüm, size daha iyi yardımcı olmaya çalışacağım. {base_response}"
        elif "positive" in emotions:
            return f"Yardımcı olabildiğime sevindim! {base_response}"
        return base_response

    def get_related_questions(self, current_question):
        """İlgili soruları bulur"""
        related = []
        category = self.kategori_bul(current_question)
        if category:
            for soru in self.soru_cevap[category]["cevaplar"].keys():
                if soru != current_question and any(word in soru for word in current_question.split()):
                    related.append(soru)
        return related[:3]

    def format_detailed_answer(self, answer, category):
        """Detaylı cevap formatlar"""
        if not self.user_preferences["detailed_answers"]:
            return answer
        
        related = self.get_related_questions(category)
        formatted = f"\n{answer}\n"
        
        if related:
            formatted += "\nİlgili sorular:\n"
            for i, q in enumerate(related, 1):
                formatted += f"{i}. {q}\n"
        
        return formatted

    def process_input(self, user_input):
        """Geliştirilmiş girdi işleme"""
        # Selamlaşma kontrolü
        greeting = self.check_greeting(user_input.lower())
        if greeting:
            return greeting
        
        # Duygu analizi
        emotions = self.analyze_emotion(user_input)
        
        # Kategori ve cevap bulma
        kategori = self.kategori_bul(user_input)
        cevap = self.cevap_bul(user_input, kategori)
        
        if cevap:
            # Duygu durumuna göre cevabı özelleştir
            cevap = self.generate_contextual_response(cevap, emotions)
            
            # Detaylı cevap formatı
            if self.user_preferences["detailed_answers"]:
                cevap = self.format_detailed_answer(cevap, kategori)
            
            # Emoji ekleme
            if self.user_preferences["show_emojis"]:
                cevap = self.format_response(cevap, kategori)
            
            return cevap
        
        return None

    def check_greeting(self, text):
        """Selamlaşma kontrolü yapar"""
        for greeting, responses in self.greetings.items():
            if greeting in text:
                return random.choice(responses)
        return None

    def suggest_corrections(self, text):
        """Yazım hatalarını düzeltme önerileri sunar"""
        words = text.lower().split()
        suggestions = {}
        
        for word in words:
            for category in self.soru_cevap.values():
                for keyword in category["anahtar_kelimeler"]:
                    similarity = self.benzerlik_orani(word, keyword)
                    if 0.7 < similarity < 1:
                        suggestions[word] = keyword
                        
        return suggestions

    def handle_preferences(self, command):
        """Kullanıcı tercihlerini yönetir"""
        if command == "emoji kapat":
            self.user_preferences["show_emojis"] = False
            return "Emoji gösterimi kapatıldı."
        elif command == "emoji aç":
            self.user_preferences["show_emojis"] = True
            return "Emoji gösterimi açıldı."
        elif command == "detay kapat":
            self.user_preferences["detailed_answers"] = False
            return "Detaylı cevaplar kapatıldı."
        elif command == "detay aç":
            self.user_preferences["detailed_answers"] = True
            return "Detaylı cevaplar açıldı."
        return None

    def son_sorulari_goster(self):
        """Son sorulan soruları gösterir"""
        if not self.son_sorular:
            return "Henüz soru sorulmamış."
        
        mesaj = "\nSon Sorulan Sorular:\n"
        for i, soru in enumerate(reversed(self.son_sorular), 1):
            mesaj += f"{i}. {soru}\n"
        return mesaj

    def oturum_bilgisi_goster(self):
        """Detaylı oturum bilgilerini gösterir"""
        sure = datetime.now() - self.session_info["start_time"]
        son_etkilesim = datetime.now() - self.session_info["last_interaction"]
        
        return f"""
Oturum Bilgileri:
----------------
Başlangıç: {self.session_info["start_time"].strftime("%H:%M:%S")}
Süre: {sure}
Son Etkileşim: {son_etkilesim.seconds} saniye önce
Toplam Soru: {self.session_info["total_questions"]}
Başarılı Cevap: {self.session_info["successful_responses"]}
Başarı Oranı: {(self.session_info["successful_responses"] / self.session_info["total_questions"] * 100):.1f}% 
"""

    def duygu_durumu_goster(self):
        """Kullanıcının duygu durumu analizini gösterir"""
        if not self.session_info["mood_tracker"]:
            return "Henüz yeterli veri yok."
        
        mood_stats = Counter(self.session_info["mood_tracker"])
        toplam = len(self.session_info["mood_tracker"])
        
        mesaj = "\nDuygu Durumu Analizi:\n"
        for mood, count in mood_stats.most_common():
            yuzde = (count / toplam) * 100
            emoji = self.get_random_emoji(mood)
            mesaj += f"{emoji} {mood.title()}: {yuzde:.1f}%\n"
        return mesaj

    def update_session_info(self, soru, cevap_basarili):
        """Oturum bilgilerini günceller"""
        self.session_info["last_interaction"] = datetime.now()
        self.session_info["total_questions"] += 1
        if cevap_basarili:
            self.session_info["successful_responses"] += 1
        
        kategori = self.kategori_bul(soru)
        if kategori:
            self.session_info["category_usage"][kategori] += 1
        
        # Duygu durumu takibi
        duygular = self.analyze_emotion(soru)
        self.session_info["mood_tracker"].extend(duygular)

    def get_smart_suggestions(self, soru):
        """Akıllı soru önerileri sunar"""
        kategori = self.kategori_bul(soru)
        if not kategori:
            return []
        
        # Popüler sorulardan öneriler
        populer = [s for s, _ in self.populer_sorular.most_common(2)]
        
        # Kategoriden benzer sorular
        benzer = self.benzer_sorulari_bul(soru)
        
        # Kategori bazlı öneriler
        kategori_onerileri = random.sample(list(self.soru_cevap[kategori]["cevaplar"].keys()), 
                                         min(2, len(self.soru_cevap[kategori]["cevaplar"])))
        
        # Tüm önerileri birleştir ve tekrarları kaldır
        tum_oneriler = list(set(populer + benzer + kategori_onerileri))
        
        # En fazla 3 öneri döndür
        return tum_oneriler[:3]

    def handle_suggestion_response(self, response):
        """Önerilen soru seçimini işler"""
        try:
            index = int(response) - 1
            if 0 <= index < len(self.suggested_questions):
                selected_question = self.suggested_questions[index]
                kategori = self.kategori_bul(selected_question)
                cevap = self.soru_cevap[kategori]["cevaplar"].get(selected_question)
                
                if cevap:
                    if isinstance(cevap, list):
                        cevap = random.choice(cevap)
                    return cevap
            return None
        except (ValueError, IndexError):
            return None

    def handle_correction_confirmation(self, response, suggested_question):
        """Yazım hatası düzeltme onayını işler"""
        if response.lower() in ['evet', 'e']:
            return self.process_input(suggested_question)
        elif response.lower() in ['hayır', 'h']:
            return "Lütfen sorunuzu başka bir şekilde sormayı deneyin."
        return None

    def print_welcome_screen(self):
        """Gelişmiş hoş geldiniz ekranı"""
        print("\n" + "=" * 50)
        print("╔════════════════════════════════════════╗")
        print("║            İKÜ CHATBOT v2.0            ║")
        print("║                                        ║")
        print("║     Sağlık, Spor ve Kültür Asistanı   ║")
        print("╚════════════════════════════════════════╝")
        
        # Rastgele bir selamlama mesajı seç
        greeting = random.choice(self.greetings["merhaba"])
        print(f"\n{greeting}")
        
        print("\nKullanılabilir Komutlar:")
        print("-" * 25)
        print("• yardım      - Komut listesini gösterir")
        print("• kategoriler - Tüm kategorileri listeler")
        print("• istatistik  - Kullanım istatistiklerini gösterir")
        print("• temizle     - Ekranı temizler")
        print("• son         - Son sorulan soruları gösterir")
        print("• populer     - En çok sorulan soruları gösterir")
        print("• mod         - Duygu durumu analizini gösterir")
        print("• q           - Çıkış yapar")
        
        print("\nÖrnek Sorular:")
        print("-" * 25)
        # Her kategoriden rastgele bir örnek soru seç
        for kategori, bilgi in self.soru_cevap.items():
            ornek = random.choice(list(bilgi["cevaplar"].keys()))
            emoji = self.get_random_emoji(kategori)
            print(f"• {ornek} {emoji}")
        
        print("\nNot: Yazım hatalarını otomatik düzeltir.")
        print("=" * 50 + "\n")

    def print_category_menu(self):
        """Kategorileri görsel olarak listeler"""
        print("\n" + "=" * 50)
        print("MEVCUT KATEGORİLER")
        print("=" * 50)
        
        for i, (kategori, bilgi) in enumerate(self.soru_cevap.items(), 1):
            emoji = self.get_random_emoji(kategori)
            print(f"\n{i}. {kategori.upper()} {emoji}")
            print("-" * 20)
            print("Örnek sorular:")
            ornekler = random.sample(list(bilgi["cevaplar"].keys()), min(3, len(bilgi["cevaplar"])))
            for ornek in ornekler:
                print(f"• {ornek}")

    def print_response(self, response, category=None):
        """Yanıtları görsel olarak formatlar"""
        print("\n" + "-" * 50)
        if category:
            emoji = self.get_random_emoji(category)
            print(f"CEVAP {emoji}")
        else:
            print("CEVAP")
        print("-" * 50)
        
        # Yanıtı satırlara böl ve güzel görünmesi için formatla
        for line in response.split('\n'):
            print(textwrap.fill(line, width=50))

    def show_thinking_animation(self, duration=1):
        """Düşünme animasyonu gösterir"""
        animation = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        end_time = time.time() + duration
        
        print("Düşünüyorum ", end="", flush=True)
        while time.time() < end_time:
            for char in animation:
                print(f"\rDüşünüyorum {char}", end="", flush=True)
                time.sleep(0.1)
        print("\r", end="")

    def get_session_summary(self):
        """Oturum özetini oluşturur"""
        sure = datetime.now() - self.session_info["start_time"]
        
        return f"""
Oturum Özeti:
------------
Toplam Soru: {self.session_info["total_questions"]}
Başarılı Cevap: {self.session_info["successful_responses"]}
Başarı Oranı: {(self.session_info["successful_responses"] / self.session_info["total_questions"] * 100):.1f}%
Oturum Süresi: {sure}
En Çok Kullanılan Kategoriler:
{self._get_top_categories()}
"""

    def _get_top_categories(self):
        """En çok kullanılan kategorileri formatlar"""
        if not self.session_info["category_usage"]:
            return "Henüz kategori kullanımı yok"
        
        result = ""
        for category, count in self.session_info["category_usage"].most_common(3):
            result += f"- {category.title()}: {count} kez\n"
        return result

if __name__ == "__main__":
    try:
        chatbot = IKUChatbot()
        chatbot.chatbot_baslat()
    except Exception as e:
        print(f"Program başlatılırken hata oluştu: {e}")