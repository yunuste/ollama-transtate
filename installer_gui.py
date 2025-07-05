import tkinter as tk
from tkinter import ttk, messagebox
import requests
import os
import threading
import subprocess

class SetupWizard:
    def __init__(self, master):
        self.master = master
        master.title("Ollama-Translate Kurulum Sihirbazı")
        master.geometry("600x400")
        master.resizable(False, False)

        self.current_page = 0
        self.pages = []

        # Kurulum dizinini kullanıcının ana dizini altına ayarla
        # Bu, her işletim sisteminde ve her kullanıcı için doğru yolu bulacaktır.
        self.install_dir = os.path.join(os.path.expanduser("~"), "ollama-translate")

        # Dizin yoksa oluştur
        if not os.path.exists(self.install_dir):
            try:
                os.makedirs(self.install_dir)
            except OSError as e:
                messagebox.showerror("Dizin Oluşturma Hatası", f"Kurulum dizini oluşturulamadı: {self.install_dir}\nHata: {e}\nLütfen gerekli izinlere sahip olduğunuzdan emin olun.")
                self.master.destroy()
                return

        # İndirilecek dosyaların listesi ve hedef isimleri
        self.download_files = [
            ("https://download943.mediafire.com/w318uvrkv6rgwc4ntVhUSUfrpb1UrAiWeVlvW3bjdS7K_1jDIpLGxaVVu8XpTmuvr_JEUs7SRzTJ-TWcqCG33aHbl7Dxf2SdaqDWCWFzj7K5ERZvmjnxbTuguNt7OmhyUFoVcbxGFNbiPlfFEUaMJ9fNJTL6lziMg9Eu8tCLNF5S/qvjbdcl8lqcw59g/readme.txt", "readme.txt"),
            ("https://download1526.mediafire.com/eugs6u9yfujgIAxdJivLgdOVIkNoiivZeOw2WsEMEqf_pAWCbOwslel0GSI-GY7xmZwlWBAMSDYNekUIi2sIzD3mQh5AuCSD4MvA-VeO8ZLeKsWIy7-nyFIAYGrXfl0svkQ_zAnN5YJu1arVCmujSrPsjI5ZWboVAicqjq56v7/bhk3kqlz6ze988j/ollama.py", "ollama.py"),
            ("https://download1586.mediafire.com/1nosq6p1c6agMZ_sNa09YnOohDcPSiB0ShepwjbB1CWctoqt1ZpF055N7pko3fh78okk3KOzUkApsPWSSmeplp-Mqnr8zTvjt28uJIoOxbdL2QksAmq1HSaR8HukyPCJil1OKsLeYXnsgsyZmp2FZ_n8ni_-u0ol9_BqxxdQXMLP/a12zwy3sumw5nyy/ollama-x86_64.AppImage", "ollama-x86_64.AppImage")
        ]
        self.current_download_index = 0

        # Her bir sayfa için bir Frame oluştur
        self.welcome_page = tk.Frame(master)
        self.license_page = tk.Frame(master)
        self.installation_page = tk.Frame(master)
        self.thank_you_page = tk.Frame(master)

        self.pages.append(self.welcome_page)
        self.pages.append(self.license_page)
        self.pages.append(self.installation_page)
        self.pages.append(self.thank_you_page)

        # Butonlar için alt çerçeve
        self.button_frame = tk.Frame(master, bd=1, relief="raised")
        self.button_frame.pack(side="bottom", fill="x", pady=5, padx=5)

        self.back_button = ttk.Button(self.button_frame, text="< Geri", command=self.go_back)
        self.back_button.pack(side="left", padx=5)

        self.next_button = ttk.Button(self.button_frame, text="İleri >", command=self.go_next)
        self.next_button.pack(side="right", padx=5)

        self.finish_button = ttk.Button(self.button_frame, text="Bitir", command=self.finish_setup)
        self.finish_button.pack(side="right", padx=5)
        self.finish_button.pack_forget() # Başlangıçta gizle

        self.cancel_button = ttk.Button(self.button_frame, text="İptal", command=self.cancel_setup)
        self.cancel_button.pack(side="right", padx=5)

        self.setup_pages()
        self.show_page(self.current_page)

    def setup_pages(self):
        # --- Sayfa 1: Karşılama Sayfası ---
        tk.Label(self.welcome_page, text="Ollama-Translate Kurulum Sihirbazına Hoş Geldiniz", font=("Arial", 16, "bold")).pack(pady=20)
        tk.Label(self.welcome_page, text="Bu sihirbaz, Ollama-Translate uygulamasını bilgisayarınıza kuracaktır.").pack(pady=5)
        tk.Label(self.welcome_page, text="Devam etmek için 'İleri' butonuna tıklayın.").pack(pady=5)

        # --- Sayfa 2: Lisans Anlaşması ---
        tk.Label(self.license_page, text="Lisans Anlaşması", font=("Arial", 14, "bold")).pack(pady=10)
        license_text = """
Ollama-Translate LİSANS SÖZLEŞMESİ (version 0.0.1)

Bu yazılım ("Yazılım"), Ollama-Translate Geliştirme Ekibi tarafından özgür bir yazılım olarak geliştirilmiştir.
Bu Yazılımı kullanmadan önce lütfen aşağıdaki şartları ve koşulları dikkatlice okuyunuz.
Yazılımı kurarak veya kullanarak, bu Lisans Sözleşmesinin tüm hüküm ve koşullarına bağlı kalmayı kabul etmiş olursunuz.

1. Yazılımın Lisansı: Ekip, bu Yazılımı kullanmanız için size münhasır olmayan, devredilemez bir lisans vermektedir.
Yazılımı kişisel veya ticari amaçlarla kullanabilirsiniz. Özgür yazılım felsefesi gereği, bu yazılımı inceleyebilir, değiştirebilir ve dağıtabilirsiniz.

2. Kısıtlamalar: Yazılımı, bu lisans sözleşmesinin izin verdiği sınırlar dışında, tersine mühendislik yapamaz, kaynak kodunu çözemez, değiştiremez, kopyalayamaz, kiralayamaz, ödünç veremez, satamaz veya dağıtamazsınız.

3. Garanti Reddi: Yazılım "olduğu gibi" sağlanmaktadır ve Ekip, Yazılımla ilgili olarak açık veya zımni hiçbir garanti vermez.
Yazılımın kalitesi, performansı veya belirli bir amaca uygunluğu konusunda herhangi bir garanti verilmez.

4. Sorumluluğun Sınırlandırılması: Ekip, Yazılımın kullanımından kaynaklanan herhangi bir doğrudan, dolaylı, arızi, özel veya sonuç olarak ortaya çıkan zararlardan sorumlu değildir.

5. Fesih: Bu lisans sözleşmesi, sizin tarafınızdan veya Ekip tarafından herhangi bir zamanda feshedilebilir.
Sözleşmenin herhangi bir hükmüne uymazsanız, Ekip bu lisansı bildirimde bulunmaksızın feshedebilir.

Bu lisans sözleşmesini kabul ettiğiniz için teşekkür ederiz.
        """
        self.license_text_widget = tk.Text(self.license_page, wrap="word", height=15, width=60)
        self.license_text_widget.insert(tk.END, license_text)
        self.license_text_widget.config(state="disabled") # Metnin düzenlenmesini engelle
        self.license_text_widget.pack(pady=10, padx=20)

        self.agree_var = tk.BooleanVar()
        self.agree_checkbox = tk.Checkbutton(self.license_page, text="Lisans anlaşmasını okudum ve kabul ediyorum.", variable=self.agree_var, command=self.check_next_button_state)
        self.agree_checkbox.pack(pady=5)
        self.check_next_button_state() # Başlangıçta ileri butonunun durumunu ayarla

        # --- Sayfa 3: Kurulum ve İndirme Sayfası ---
        tk.Label(self.installation_page, text="Program Kuruluyor ve Dosyalar İndiriliyor...", font=("Arial", 14, "bold")).pack(pady=20)
        self.current_file_label = tk.Label(self.installation_page, text="Dosyalar hazırlanıyor...")
        self.current_file_label.pack(pady=5)
        self.progress_bar = ttk.Progressbar(self.installation_page, orient="horizontal", length=300, mode="determinate")
        self.progress_bar.pack(pady=10)
        self.overall_progress_label = tk.Label(self.installation_page, text="Genel İlerleme: 0%")
        self.overall_progress_label.pack(pady=5)

        # --- Sayfa 4: Teşekkür Mesajı ---
        tk.Label(self.thank_you_page, text="Kurulum Tamamlandı!", font=("Arial", 16, "bold")).pack(pady=20)
        tk.Label(self.thank_you_page, text="Ollama-Translate başarıyla bilgisayarınıza kuruldu.").pack(pady=10)
        # Teşekkür mesajında dinamik olarak doğru yolu göster
        tk.Label(self.thank_you_page, text=f"Dosyalar şu dizine indirildi: {self.install_dir}").pack(pady=5)
        tk.Label(self.thank_you_page, text="Sihirbazdan çıkmak için 'Bitir' butonuna tıklayın.").pack(pady=10)

    def show_page(self, index):
        for i, page in enumerate(self.pages):
            if i == index:
                page.pack(fill="both", expand=True)
            else:
                page.pack_forget()

        self.update_buttons()

    def update_buttons(self):
        # Geri butonu
        if self.current_page == 0:
            self.back_button.config(state="disabled")
        else:
            self.back_button.config(state="normal")

        # İleri ve Bitir butonları
        if self.current_page == len(self.pages) - 1: # Son sayfa
            self.next_button.pack_forget()
            self.finish_button.pack(side="right", padx=5)
            self.cancel_button.pack_forget() # Son sayfada iptal butonunu gizle
        else:
            self.next_button.pack(side="right", padx=5)
            self.finish_button.pack_forget()
            self.cancel_button.pack(side="right", padx=5)
            self.check_next_button_state() # İleri butonunun durumunu güncelle

        # Kurulum sayfasına gelindiğinde indirme işlemini başlat
        if self.current_page == 2:
            self.next_button.config(state="disabled") # İndirme bitene kadar ileri butonunu devre dışı bırak
            # İndirme işlemini ayrı bir thread'de başlat
            download_thread = threading.Thread(target=self.start_downloading_files)
            download_thread.start()

    def check_next_button_state(self):
        # Lisans sayfasındaysa ve onay kutusu işaretli değilse ileri butonunu devre dışı bırak
        if self.current_page == 1:
            if not self.agree_var.get():
                self.next_button.config(state="disabled")
            else:
                self.next_button.config(state="normal")
        elif self.current_page == 2: # Kurulum sayfasındaysa, indirme bitene kadar ileri kapalı kalır
             self.next_button.config(state="disabled")
        else:
            self.next_button.config(state="normal")

    def go_next(self):
        if self.current_page < len(self.pages) - 1:
            self.current_page += 1
            self.show_page(self.current_page)

    def go_back(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.show_page(self.current_page)

    def open_file(self, filepath):
        """İşletim sistemine göre dosyayı açar."""
        if os.path.exists(filepath):
            try:
                if os.name == 'nt':  # Windows
                    os.startfile(filepath)
                elif os.uname().sysname == 'Darwin':  # macOS
                    subprocess.run(['open', filepath])
                else:  # Linux/Unix
                    subprocess.run(['xdg-open', filepath])
            except Exception as e:
                messagebox.showerror("Dosya Açma Hatası", f"Dosya açılamadı: {filepath}\nHata: {e}")
        else:
            messagebox.showerror("Dosya Bulunamadı", f"Belirtilen dosya bulunamadı: {filepath}")

    def start_downloading_files(self):
        total_files = len(self.download_files)
        overall_progress_per_file = 100 / total_files
        readme_path = "" # readme.txt'nin yolunu tutmak için

        for i, (url, filename) in enumerate(self.download_files):
            full_path = os.path.join(self.install_dir, filename)
            self.current_file_label.config(text=f"İndiriliyor: {filename} ({i+1}/{total_files})")
            self.master.update_idletasks() # Ekranı güncelle

            if filename == "readme.txt":
                readme_path = full_path

            try:
                response = requests.get(url, stream=True)
                response.raise_for_status() # HTTP hataları için hata fırlat

                total_size = int(response.headers.get('content-length', 0))
                downloaded_size = 0

                with open(full_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk: # chunk filtrelenmiş keep-alive paketleri için
                            f.write(chunk)
                            downloaded_size += len(chunk)
                            # Dosya bazında ilerleme
                            if total_size > 0:
                                file_progress = (downloaded_size / total_size) * 100
                                self.progress_bar["value"] = file_progress
                                # Genel ilerleme
                                overall_progress = (i * overall_progress_per_file) + (file_progress / 100 * overall_progress_per_file)
                                self.overall_progress_label.config(text=f"Genel İlerleme: {int(overall_progress)}%")
                                self.master.update_idletasks()
                self.current_download_index = i + 1 # Bir sonraki dosya için indeksi güncelle
            except requests.exceptions.RequestException as e:
                messagebox.showerror("İndirme Hatası", f"Dosya indirilirken bir hata oluştu: {filename}\nHata: {e}")
                self.overall_progress_label.config(text="İndirme Başarısız Oldu!")
                self.next_button.config(state="normal") # Hata olsa bile ilerlemeye izin ver (devam etme seçeneği)
                return # Hata durumunda indirme işlemini durdur
            except Exception as e:
                messagebox.showerror("Dosya Yazma Hatası", f"Dosya yazılırken bir hata oluştu: {filename}\nHata: {e}")
                self.overall_progress_label.config(text="İndirme Başarısız Oldu!")
                self.next_button.config(state="normal")
                return

        self.current_file_label.config(text="Tüm dosyalar başarıyla indirildi!")
        self.progress_bar["value"] = 100
        self.overall_progress_label.config(text="Genel İlerleme: 100%")
        self.next_button.config(state="normal") # İndirme bitince ileri butonunu etkinleştir

        # readme.txt'yi aç
        if readme_path:
            self.open_file(readme_path)

    def finish_setup(self):
        messagebox.showinfo("Kurulum Tamamlandı", "Ollama-Translate başarıyla kuruldu!")
        self.master.destroy()

    def cancel_setup(self):
        if messagebox.askyesno("Kurulumu İptal Et", "Kurulumu iptal etmek istediğinizden emin misiniz?"):
            self.master.destroy()

if __name__ == "__main__":
    # requests kütüphanesinin kurulu olduğundan emin olun
    # Eğer kurulu değilse, terminalde 'pip install requests' komutunu çalıştırın.
    try:
        import requests
    except ImportError:
        messagebox.showerror("Eksik Kütüphane", "requests kütüphanesi bulunamadı. Lütfen 'pip install requests' komutunu çalıştırın.")
        exit()

    root = tk.Tk()
    app = SetupWizard(root)
    root.mainloop()
