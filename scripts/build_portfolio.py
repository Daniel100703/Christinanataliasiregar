"""Generate the separate, print-ready A4 portfolio. Run: python3 scripts/build_portfolio.py.
Requires reportlab and Pillow. Uses only existing portfolio text and images.
"""
from pathlib import Path
from xml.sax.saxutils import escape
import re
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'Portofolio-Christina-Natalia-Siregar.pdf'
W, H = 595.2756, 841.8898
M = 43
WINE, INK, MUTED, LINE = '#672c3f', '#292827', '#6f6965', '#ded8d1'
FONT_DIR = Path('/usr/share/fonts/truetype/dejavu')
# DejaVu can be replaced by installed fonts; standard PDF fonts are a fallback.
if (FONT_DIR / 'DejaVuSans.ttf').exists():
    for name, file in [('Body','DejaVuSans.ttf'),('Bold','DejaVuSans-Bold.ttf'),('Title','DejaVuSerif.ttf'),('Italic','DejaVuSerif-Italic.ttf')]:
        if (FONT_DIR / file).exists():
            pdfmetrics.registerFont(TTFont(name, str(FONT_DIR / file)))
        else:
            pdfmetrics.registerFont(pdfmetrics.Font(name, 'Times-Italic', 'WinAnsiEncoding'))
else:
    for name, base in [('Body','Helvetica'),('Bold','Helvetica-Bold'),('Title','Times-Roman'),('Italic','Times-Italic')]:
        pdfmetrics.registerFont(pdfmetrics.Font(name, base, 'WinAnsiEncoding'))

c = canvas.Canvas(str(OUT), pagesize=(W,H), pageCompression=1)
c.setTitle('Portofolio Profesional - Christina Natalia Siregar')
c.setAuthor('Christina Natalia Siregar')
c.setSubject('Administrasi, operasional, koordinasi acara, dan layanan pelanggan')

def text(s, x, y, font='Body', size=10, color=INK):
    c.setFillColor(HexColor(color)); c.setFont(font,size); c.drawString(x,H-y,s)

def rule(y, x=M, width=W-2*M):
    c.setStrokeColor(HexColor(LINE)); c.setLineWidth(.6); c.line(x,H-y,x+width,H-y)

def para(s, x, y, width, size=9.3, leading=15, color=MUTED, font='Body'):
    style=ParagraphStyle('p',fontName=font,fontSize=size,leading=leading,textColor=HexColor(color),alignment=TA_LEFT)
    p=Paragraph(s,style); _,h=p.wrap(width,H);p.drawOn(c,x,H-y-h);return y+h

def image(name,x,y,w,h):
    # Letterbox screenshots to keep all information visible without cropping.
    from PIL import Image
    im=Image.open(ROOT/'assets'/name)
    iw,ih=im.size; scale=min(w/iw,h/ih); nw,nh=iw*scale,ih*scale
    c.drawImage(str(ROOT/'assets'/name),x+(w-nw)/2,H-y-(h+nh)/2,width=nw,height=nh)

def page(no, label):
    text('CHRISTINA NATALIA SIREGAR',M,30,'Bold',7.3,WINE)
    text(label.upper(),W-230,30,'Body',6.7,MUTED)
    rule(43)
    rule(794)
    text('PORTOFOLIO PROFESIONAL  /  2026',M,813,'Body',6.7,MUTED)
    text(f'{no:02d} / 05',W-M-37,813,'Body',7,WINE)

def title(kicker, heading):
    text(kicker,M,78,'Bold',7.3,WINE)
    text(heading,M,116,'Title',27,INK)

def bullet(s,y,x=M+14,width=W-2*M-14):
    text('•',x-12,y+10,'Body',9,WINE)
    return para(escape(s),x,y,width,9,14)+5

# 1. A useful introduction, not a mostly empty cover.
page(1,'Profil & kompetensi')
text('ADMINISTRASI & OPERASIONAL',M,84,'Bold',8,WINE)
text('Christina',M,134,'Title',34)
text('Natalia Siregar.',M,177,'Italic',31,WINE)
text('Rapi mengurus detail.',M,216,'Body',12)
text('Tenang mengoordinasikan banyak hal.',M,237,'Body',11)
image('portrait.jpg',413,72,136,176)
rule(268)
y=para('Lulusan D3 Kesekretariatan Universitas Sumatera Utara dengan pengalaman di edukasi tenaga kesehatan, biro perjalanan, dan ritel daring. Terbiasa menangani registrasi dan database peserta, anggaran serta invoice, dokumen, dan koordinasi acara dari perencanaan hingga pasca-kegiatan.',M,286,W-2*M,10,17)
y=para('Cepat menyesuaikan sistem baru dan nyaman menjadi penghubung antara peserta, klien, mitra, dan tim internal.',M,y+13,W-2*M,10,17)
for x,num,label in [(M,'494','Pendaftar dalam satu program'),(225,'159','Peserta daring dalam satu sesi'),(407,'C1','EF SET English Advanced')]:
    text(num,x,437,'Title',29,WINE)
    para(label,x,450,145,7.4,12)
rule(487)
text('KOMPETENSI UTAMA',M,513,'Bold',8,WINE)
para('Administrasi perkantoran & arsip<br/>Microsoft Office & Google Workspace<br/>Pengolahan data & database peserta<br/>Tour costing, quotation & invoicing',M,530,249,9,17)
para('Registrasi & sertifikat melalui Canva<br/>Koordinasi acara & layanan pelanggan<br/>Administrasi SKP, LMS & platform terkait<br/>Komunikasi & copywriting promosi',311,530,243,9,17)
rule(618)
text('PENDIDIKAN',M,645,'Bold',8,WINE)
text('D3 Kesekretariatan',M,670,'Bold',10)
text('Universitas Sumatera Utara  |  2019 - 2022',M,690,'Body',9,MUTED)
text('Medan, Sumatera Utara',M,735,'Body',9,WINE)
text('christinanataliasiregar19@gmail.com  |  +62 821-6738-5790',M,755,'Body',8,MUTED)
c.showPage()

# 2. All roles and responsibilities from the existing site.
page(2,'Pengalaman profesional');title('01 / PERJALANAN KARIER','Pengalaman profesional')
html=(ROOT/'index.html').read_text()
articles=re.findall(r'<article class="xp">.*?</article>',html,re.S)
def clean(s):
    from html import unescape
    return unescape(re.sub('<[^>]+>','',s)).strip().replace('–','-').replace('—','-')
y=145
for a in articles:
    role=clean(re.search(r'<h3 class="xp-role">(.*?)</h3>',a,re.S).group(1))
    date=clean(re.search(r'<span class="xp-date">(.*?)</span>',a,re.S).group(1))
    org=clean(re.search(r'<div class="xp-org">(.*?)</div>',a,re.S).group(1))
    text(role,M,y+14,'Bold',12)
    c.setFillColor(HexColor(MUTED));c.setFont('Body',7.7);c.drawRightString(W-M,H-y-13,date)
    text(org,M,y+33,'Body',9,WINE)
    y+=46
    for s in re.findall(r'<li>(.*?)</li>',a,re.S):y=bullet(clean(s),y)
    y+=8;rule(y);y+=15
assert y<780, f'Experience overflow: {y}'
c.showPage()

# 3-4. Evidence, displayed whole, with captions that explain the work.
def evidence_block(number, heading, category, file, desc, y):
    text(number+' / '+category,M,y,'Bold',7.2,WINE)
    text(heading,M,y+27,'Title',18)
    # Thin border gives screenshot edges definition on white printer paper.
    c.setFillColor(HexColor('#f7f5f2'));c.rect(M,H-y-231,W-2*M,187,fill=1,stroke=0)
    image(file,M+10,y+52,W-2*M-20,169)
    return para(desc,M,y+246,W-2*M,9,14)
page(3,'Bukti kerja - Medsense');title('02 / DOKUMENTASI KARYA','Administrasi & koordinasi')
evidence_block('01','Registrasi & verifikasi peserta','MEDSENSE','registration.jpg','Mengelola formulir pendaftaran webinar nasional dan memverifikasi data peserta satu per satu. Salah satu program tercatat hingga 494 pendaftar.',151)
evidence_block('02','Operasional webinar kesehatan','MEDSENSE','webinar.jpg','Menjalankan operasional webinar edukasi tenaga kesehatan, dari monitoring kuota dan akses pembelajaran hingga status SKP. Satu sesi diikuti 159 peserta daring.',463)
c.showPage()
page(4,'Bukti kerja - Dokumen & anggaran');title('03 / DOKUMENTASI KARYA','Dokumen & perencanaan')
evidence_block('03','Pembuatan sertifikat massal','MEDSENSE','certificates.jpg','Memproduksi sertifikat peserta secara bulk sesuai database dan ketentuan program, siap didistribusikan pada tahap pasca-kegiatan.',151)
evidence_block('04','Tour costing & anggaran','ERNI TOUR & TRAVEL','tour-budget.jpg','Menyusun rincian biaya transportasi, akomodasi, dan operasional perjalanan sebagai dasar quotation kepada pelanggan.',463)
c.showPage()

# 5. Activities, credentials, and actionable contact links.
page(5,'Pengembangan & kontak');title('04 / PENGEMBANGAN DIRI','Belajar & bertumbuh')
items=[('tour.jpg','Group Leader tour budaya','Indonesia-Xiamen'),('training.jpg','Pelatihan Tour Berbasis','Kompetensi (BBPV)'),('internship.jpg','Magang Kesbangpol','Sumatera Utara'),('organization.jpg','Pengurus organisasi','GMKI FEDITA USU')]
colw=(W-2*M-24)/2
for i,(file,a,b) in enumerate(items):
    x=M+(i%2)*(colw+24);y=146+(i//2)*174
    image(file,x,y,colw,121)
    text(a,x,y+139,'Bold',8)
    text(b,x,y+153,'Body',8,MUTED)
rule(495)
text('SERTIFIKASI & PELATIHAN',M,522,'Bold',8,WINE)
for y,a,b in [(545,'EF SET English Certificate','C1 Advanced - 2025'),(570,'TOEFL ITP','Language Center of UNJ - 2023'),(595,'Pelatihan Tour Berbasis Kompetensi','BBPV'),(620,'Career Class Preparation for Better Future','PT Jago Karir Indonesia - 2024')]:
    text(a,M,y,'Bold',8.3)
    text(b,355,y,'Body',7.5,MUTED)
rule(642)
text('MARI TERHUBUNG',M,667,'Bold',8,WINE)
para('Terbuka untuk peran administrasi, manajemen, operasional, sekretaris, atau layanan pelanggan.',M,681,W-2*M,9,14)
text('christinanataliasiregar19@gmail.com',M,728,'Body',9,WINE)
c.linkURL('mailto:christinanataliasiregar19@gmail.com',(M,H-732,320,H-716),relative=0)
text('+62 821-6738-5790',M,750,'Body',9,WINE)
c.linkURL('tel:+6282167385790',(M,H-754,200,H-739),relative=0)
text('linkedin.com/in/christinanataliasiregar',M,772,'Body',8,WINE)
c.linkURL('https://www.linkedin.com/in/christinanataliasiregar/',(M,H-776,320,H-761),relative=0)
c.showPage();c.save()
print(OUT)
