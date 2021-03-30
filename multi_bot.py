import telebot, requests, json, os, sys, time, urllib
from datetime import datetime

TOKEN = "token_bot"
bot = telebot.TeleBot(TOKEN)
waktu = datetime.today().strftime('%Y-%m-%d')

@bot.message_handler(commands=["start"])
def index(pesan):
    bot.send_message(pesan.chat.id, "*BOT SUDAH BERJALAN🛠*", parse_mode="Markdown")
    
@bot.message_handler(commands=["help"])
def tolong(sos):
    bot.send_message(sos.chat.id, "*Selamat datang difitur bantuan⚙\n\nPertanyaan:\nApa yang bisa dilakukan bot ini?\n\nJawaban:\nBot ini bisa mengerjakan beberapa tugas seperti menulis dibuku,mencari jadwal sholat suatu kota,dll\n\nPenjelasan fitur\n\n- /help -> Menampilkan menu bantuan\n- /source -> Source code bot\n- /berita -> Menampilkan berita-berita terbaru\n- /tulis -> Menggunakan bot tulis\n- /jadsho -> Mencari jadwal sholat suatu kota\n- /quran -> Al-Qur'an Online\n\nSEMOGA MENU BANTUAN INI MEMBANTU ANDA UNTUK MENGGUNAKAN BOT :)*", parse_mode="Markdown")
    
@bot.message_handler(commands=["source"])
def sc(minta):
    bot.send_message(minta.chat.id, "*Source code bot🔓\n\n{github}*", parse_mode="Markdown")
    
@bot.message_handler(commands=["tulis"])
def index(pesan):
    pesan_index = bot.send_message(pesan.chat.id, "*Selamat datang difitur bot tulis*📑\n\n*Silakan ketik tugas anda!!*", parse_mode="Markdown")
    bot.register_next_step_handler(pesan_index, scanner)
    
def scanner(tulisan):
    tugas = tulisan.text
    req = requests.get("http://salism3.pythonanywhere.com/write?text="+tugas)
    response = json.loads(req.text)

    jumlah = 0
    bot.send_message(tulisan.chat.id, "Mohon tunggu sebentar...\nBot sedang menulis📝")
    for gambar in response["images"]:
        jumlah += 1
        jumlah_tot = str(jumlah)
        url = gambar
        f = open(f"gambar{jumlah_tot}.png", "wb")
        f.write(urllib.request.urlopen(url).read())
        f.close()
        
        img = open(f"gambar{jumlah_tot}.png", "rb")
        bot.send_photo(tulisan.chat.id, img)
        img.close()
        
    bot.send_message(tulisan.chat.id, "Tugas selesai dikerjakan :)\n\nTerimakasih sudah menggunakan bot kami\nSpesial thank from Vit ID")
        
@bot.message_handler(commands=["jadsho"])
def index(pesan):
        pesan_index = bot.send_message(pesan.chat.id, "*Selamat datang difitur jadwal sholat🕌*\n\n*Silakan masukan nama kota anda(Ex. Medan)!!*", parse_mode="Markdown")
        bot.register_next_step_handler(pesan_index, nama_kota)
        
def nama_kota(kota):
        tempat = kota.text
        url = f"https://api.pray.zone/v2/times/day.json?city={tempat}&date={waktu}"
        req = requests.get(url)
        if req.status_code == 200:
            jeson = json.loads(req.text)
            
            for hasil in jeson["results"]["datetime"]:
                tanggal = hasil["date"]["gregorian"]
                subuh = hasil["times"]["Imsak"]
                dzuhur = hasil["times"]["Dhuhr"]
                ashar = hasil["times"]["Asr"]
                maghrib = hasil["times"]["Maghrib"]
                isya = hasil["times"]["Isha"]
                
            bot.send_message(kota.chat.id, f"Jadwal Sholat kota *{tempat.upper()}*🏠\nHari ini tanggal *{tanggal}*\n\n*Subuh: {subuh}*\n*Dzuhur: {dzuhur}*\n*Ashar: {ashar}*\n*Maghrib: {maghrib}*\n*Isya: {isya}*\n\nSemoga bisa membantu anda :)", parse_mode="Markdown")
        else:
            bot.send_message(kota.chat.id, "*Maaf kota yang anda cari tidak dapat ditemukan didalam data kami :(\n\nSilakan ketik /jadsho untuk melihat jadwal kota lain*", parse_mode="Markdown")
            
@bot.message_handler(commands=["quran"])
def index(pesan):
    pesan_index = bot.send_message(pesan.chat.id, "*Selamat datang difitur quran online🕌*\n\n*Silakan masukan nomor surah(Contoh: Al-Fatihah -> 1)*", parse_mode="Markdown")
    bot.register_next_step_handler(pesan_index, sumber)
    
def sumber(surah):
    surah_cari = surah.text
    
    url = f"https://api.quran.sutanlab.id/surah/{surah_cari}"
    req = requests.get(url)
    jeson = json.loads(req.text)
    
    try:
      ayat = 0
      for hasil in jeson["data"]["verses"]:
          ayat += 1
          ayat_jadi = str(ayat)
          arab = hasil["text"]["arab"]
          latin = hasil["text"]["transliteration"]["en"]
          arti = hasil["translation"]["id"]
          bot.send_message(surah.chat.id, f"*Ayat ke: {ayat_jadi}*\n\n{arab}\n\n*Latin:*\n{latin}\n\n*Arti:*\n{arti}", parse_mode="Markdown")
          time.sleep(2)
          
    except Exception as e:
        bot.send_message(surah.chat.id, f"*Maaf surah '{surah_cari}' tidak ditemukan\n\nSilakan ketik /quran untuk mencari surah lain :')*", parse_mode="Markdown")
    
@bot.message_handler(commands=["berita"])
def index(pesan):
    key = "key -> create from url"
    bot.send_message(pesan.chat.id, "*Selamat datang difitur berita📺*\n\n*Berikut ini adalah berita terbaru dari beberapa situs berita terpercaya*", parse_mode="Markdown")
    url = f"https://newsapi.org/v2/top-headlines?country=id&apiKey={key}"
    req = requests.get(url)
    jeson = json.loads(req.text)
    
    jum = 0
    for hasil in jeson["articles"]:
        jum += 1
        jum_tot = str(jum)
        url = hasil["url"]
        judul = hasil["title"]
        
        
        bot.send_message(pesan.chat.id, f"*Judul: {judul}*\n\n*Url berita: {url}*", parse_mode="Markdown")
        
#Handle command not found
@bot.message_handler(content_types=["text"])
def error(er):
    ers = er.text
    bot.send_message(er.chat.id, f"*Maaf perintah '{ers}' tidak ditemukan\n\nSilakan ketik /help untuk bantuan*", parse_mode="Markdown")
    
if __name__ == "__main__":
    kata = """
    \033[1;37m----------\033[1;32m=\033[1;36m[ \033[1;33mPesan \033[1;36m]\033[1;32m=\033[1;37m----------
        \033[1;34mBOT TELE SUDAH BERJALAN
        
            \033[1;31mAuthor\033[1;33m: \033[1;37mVit ID
   \033[1;31mGithub\033[1;33m: \033[1;37mhttps://github.com/DavitID
   """
   
    def tulis(kata):
     for ketik in kata:
         sys.stdout.write(ketik)
         sys.stdout.flush()
         time.sleep(0.01)
        
    tulis(kata)
    bot.polling(none_stop = True)