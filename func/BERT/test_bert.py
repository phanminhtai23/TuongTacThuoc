from transformers import pipeline

# Load mô hình BERT cho nhiệm vụ Question Answering
qa_pipeline = pipeline("question-answering",
                       model="deepset/bert-base-cased-squad2")

# Văn bản về thuốc

text = r"""
4
Shree
CONG TYCé PHA ƯỢC PHẨM DBC: Viên nang-vỉ bấmPHAN DUC x ~ ã cất 7CỬU LONG MAU NHAN Vi AECYSMUX® Mã số: Q4. ĐKM.GY-LI.: Số: 07. 27 - 07 - 2013
T——eRlar—~ VỈ 10 VIÊN NANG CỨNG(nang số 1)
BỘ Y TẾ
CUC QUAN LÝ DƯỢC
DA PHE DUYET

Nhãn trực tiếp trên đơn vị đóng gói nhỏ nhất
Lan dau: 2.2).A % ./.204 % 0 mo
    vo edtah sar hà
    want PECKco
    Cơ sở xin đăng ký
    ổng Giám Đốc

    yến Hữu Trung
    CỔ PHẦN DƯỢC PHẨM
    CÔNG TY
    MAU NHAN HỘP AECYSMUXÊHỘP 10 VỈ x 10 VIÊN NANG CỨNG(nang số 1)
    CỬU LONG~—— seGfĐar———~
    Nhãn trung gian
    GMP-WHO
    AECYSMUX"Acetylcystein 200 mg
    GMP-WHO
    AECYSMUX°

    Acetylcyslein200mụ



    THÀNH PHẨN: Acetylcystein
    Ta duge vira du .

    và thuốc làm giảm độ quánh của đồm ở phổi có mũ, trị
    rối loạn về chất tiết phế quản trong viêm phế quản cấp
    và cơn cấp của viêm phế quản mẫn tinh, Acetylcystein
    dùng giải độc trong quá liều paracstamai.
    8 SK: Ngày 5X: Han deg:

    Bw 002 0(215Á2 | A182y
eXNWSAIAVOHM-dWO Jk. LH ef _
CHONG CHI BINH, CÁCH DUNG VA LIEU DUNG, THAN TRONG c...TAC DUNG KHONG MONG MUON, TUONG TAC THI
Xin đọc trang td hung din sv dyng thude.
SDK:
Tiêu chuẩn áp dụng: TCCS
BẢO QUẦN: Để thuốc nơi khô ráo, thoáng mát, nhiệttránh ánh sáng.
Để thude xa 14m tay trẻ em.
Đọc kỹ hướng dẫn sử dụng trước khi dũng
CÔNG TY CỔ PHẦN DƯỢC PHẨM CỬU LONGnuaana - 150 điểng 14/9 - Phường 5 - Tp Vĩhh Lạng - Tĩnh Vĩnh Long
fiz(CCF

    4 ee




    DBC: Viên nang-vÌ bấm
    Mã số: Q4. ĐKM.GY-LI
    Số: 07. 27 - 07 - 2013

    BuiQ02U6\SÁ2)/402v
sX\NSAĐäY.
OHAYdNS

Cơ sở xin đăng ký
KT. Tổng Giám Đốc  feJ LÔNG: sri
gốm Trung
Ẻ
NATh.
CONG TY DBC: Vién nang-vi bamCO PHAN DUGC PHAM z - aCUU LONG MẪU NHẪN CHAI AECYSMUX® = M40: Q4. PKM.GY-L15 - Số: 07. 27 - 07 - 2013—mo CHAI 100 VIÊN NANG CỨNG(nang số 1)
Nhãn trực tiếp trên đơn vị đóng gói nhỏ nhất
- THÀNH PHẨN: | Cah ent AcetylcySt@in ....cc.cccccescscstseereeen200 mg | Tá dược vừa đủ .................... se...1 VIÊN
CHỈ ĐỊNH: Acetylcystein dùng làm thuốc tiêu chất nhẩy 'và thuốc làm gl m độ ánh của đờm ở phổi có mủ, trịrối loạn về chất tiết phê quản trong viêm phế quản cấpvà cơn cấp của viêm phếquản mãn tính. Acetylcystein
Acetylcystein 200 mg dùng giải độctrongquá liéu paracetamol.- CHONG CHỈ ĐỊNH, THẬNTRÙNGCÁCH DING & yeu DUNGCHAI 100 VIEN NANG CUNG TAC DUNG KHONG MONG MUON; TUONG TAC THUOC, Xindoc trongtờhướngdẫn sử dụng thuốc.5Ð


nụ hôráo, thoáng mát, S
ánh sáng.
tay trẻ em.
Cơ sở xin đăng ký
ổng Giám Đốc

` guyễn Hữu Trung
: CÔNG TY
CỔ PHẦN DƯỢC PHẨM5 ề 4 Ẫ a _ Mã số: Q4.ĐKM.GY-LICỬU LONG TO HUONG DAN SUDUNG THUOC Số-07 27.07.2013
DBC: Viên nang-vỉ bấm
«cite+
AECYSMUX® GMP-WHOViên nang cứng
THÀNH PHẨN:
AcetylcySÍ6ÏI................... các ng y2 200 mg
Tá dược vừa đủ ...... ..1 Viên
(Tá dược gồm: Tinh bội tiên hồ hóa, đường trắng, ‘natri chat, “acid citric monohydrat, silicon dioxyd)
DANG BAO GHẾ: Viên nang cứng.
QUY CACH BONG GOI: Chai 100 viên. Hộp 10 vỉ x 10 viên.
CHỈ ĐỊNH: Acetylcystein dùng làm thuốc tiêu chất nhdy và thuốc làm giảm độ quánh của đờm ở phổi có mủ, trị rối loạn về chất tiết
phế quản trong viêm phế quản cấp và cơn cấp của viêm phế quản mãn tính. Acetylcystein dùng giải độc trong qué ligu paracetamol.
CÁCH DÙNG VÀ LIỀU DUNG: AECYSMUX®200 mg được dùng bằng đường
Tiêu chất nhầy: Người lớn: 200 mg(1 viên) x 3 lần/ngày. Trả em từ 2 đến 6 tuổi: 200 mg(1 viên) x 2 lân/ngày. Giải độc quá liều
paracetamol: Liéu khdi d4u 140 mg/kg, tiếp theo cách 4 giờ uống một lần với liều 70 mg/kg và uống tổng cộng thêm 17 lần.
- Hoặc theo sự hướng dẫn của thầy thuốc.
CHỐNG CHỈ ĐỊNH: Quá mẫn với acetylcystein hay bất cứ thành phần nào của thuốc. Bệnh nhân hen hay có tiền sử co thắt phế quản. Trẻ
em dưới 2 tuổi.
THAN TRONG KHI DUNG THUỐC: Phải giám sát chặt chế người bệnh có nguy cơ phát hen, nếu dùng acetylcystein cho người có tiền sử dị
ứng, nếu có co that phế quản, phải dùng thuốc phun mù giãn phế quản như salbutamol(thuốc beta - 2 adrenergic chọn lọc, tác dụng ngắn)
hoặc ipratropium(thuốc kháng muscarin) và phải ngừng acetylcystein ngay. Khi điều trị với acetylcystein, có thể xuất hiện nhiều đờm
loãng ở phế quản, cần phải hút để lấy ra nếu người bệnh giảm khả năng ho.
TƯƠNG TAC THUOC: Acetylcystein la mot chất khử nên không phù hợp với các chất oxy - hóa. Không được dùng đồng thời các thuốc ho
khác hoặc bất cứ thuốc nào làm giâm bài tiết phế quản trong thời gian điềutrị bằng acetylcystein. Acetylcystein phản ứng với 1 số kim loại,
đặc biệt sắt, niken, đồng và với cao su. Cẩn tránh thuốc tiếp xúc với các chất đó. Dung dịch natri acetylcystein tương ky về lý và/hoặc hóa
hoc véi cac dung dich chia penicilin, oxacilin, oleandomycin, amphotericin B, tetracyclin, erythromycin, lactobionat, hodc natri ampicilin.
Khi định dùng một trong các kháng sinh đó ở dạng khí dung, thuốc đó phải được phun mù riêng. Dung dịch acetylcystein cũng tương ky về
lý học với dầu iod, trypsin và hydrogen peroxyd.
TAC DUNG KHONG MONG MUỐN: Thường gặp: ADR > 1/100. Buồn nôn, nôn. gặp: 1/1000 < ADR < 1/100. Buồn ngủ, nhức đầu, ùtai.
Viêm miệng, chảy nước mũi nhiều. Phát ban, mày đay. Hiếm gặp: ADR < 1/1000 0o thắt phế quản kèm phản ứng dạng phản vệ toàn than.
Sốt, rét run. Cách xử trí: Dùng dung dịch acetylcystein pha loãng có thể giảm khả năng gây nôn nhiều do thuốc. Phải điều trị ngay phản
ứng phản vệ bằng tiêm dudi da adrenalin (0, 3 - 0, 5 ml dung dich 1/1000) thở oxy 100 %, đặt nội khí quản nếu cẩn, truyền dịch tĩnh mạch
dé tăng thể tích huyết tương, hít thuốc chủ vận befa - adrenergic nếu co thắt phế quản, tiêm tĩnh mạch 500mg hydrocortison hoặc 125 mg
methylprednisolon. Co thé ức chế phản ứng quá mẫn với acetylcystein bao gồm phát hồng ban toàn thân, ngứa, buồn nôn, nôn, chóng mặt,
bằng dùng kháng histamin trước. Cóý kiến cho rằng quá mẫn là do cơ chếgiả dị ứng trên cơ sở giải phóng histamin hơn là do+7

miễn dịch. Vì phản ứng quá mẫn đã xảy ra tới 3 % \số người tiềm tĩnh mạch
acetylcystein dé điều trị quá liều paracetamol, nên các thầy thuốc cần chúý dùng kháng histamin để phòng phản ứng đó.
Thông báo cho bác sỹ những tác dụng không mong muốn gặp phải khi sử dụng thuốc
DƯỢC LỰC HỌC: Acetylcystein(N - acetylcystein) là dẫn chất N - acetyl của L - cys†ein, một amino - acid tự nhiên. Acetylcystein được dùng
làm thuốc tiêu chất nhẩy và thuốc giải độc khi quá liều paracetamol. Thuốc làm giảm độ quánh của đờm ở phổi có mủ hoặc không bằng cá
tách đôi cầu nối disulfua trongmucoprotein và tạo thuận lợi để tống đờm ra ngoài bằng ho, dẫn lưu tư thế hoặc bằng phương pháp cơ học.
Acetylcystein cũng được dùng tại chỗ để điều trị không có nước mắt. Acetylcystain dùng để bảo vệ chống gây độc cho gan do quá liểu
paracetamol, bang cách duy trì hoặc khôi phục nồng độ gluthation của gan là chất cẩn thiết để làm bất hoạt chất chuyển hóa trung gian cia. *
paracetamol gây độc cho gan. Trong quá liều paracetamol, một lượng lớn chất chuyển hóa này được tạo ra vì đường chuyển hóa chính(liền
                                                                                                                                 - glucuronid va sulfat) trở thành bão hòa. Acetylcystein chuyển hóa thành cystein kích thích gan tổng hợp gluthation và dọ đó, =
a | _avetyteystein có thể bảo vệ được gan nếu bắt đầuđiều trị trong vòng 12 giờ sau khi quá liều paracetamol. Bắt đầuđiều trị càng sớm càng tối:
ni > E 'bUgb.BONG HỌC: Sau khí uống acetylcystein được hấp thu nhanh ở đường tiêu hóa và bị gan khử acetyl thanh cystein va sau đó
> PH “chiyén Hóa, Đạt nồng độ đỉnh huyết tương trong khoảng 0, 5 đến 1 giờ sau khi uống liều 200-600 mg. Khả dung sinh học khi uống
un pH eothé đốc uyển hóa trong thành ruột và chuyển hóa bước đầutrong gan. độ thanh thải thận có thể chiếm 30 % độ thanh thải toàn thân.
x: | QUA ue) À XỬ TRÍ: Quá liều có triệu chứng tương tựnhư triệu chứng củaphảmệ;; qh)ưng nặng hơn nhiều đặc biệt là giảm huyếtáp. Các
    _Ƒˆ triềuchữ ¡ khác bao gồm suy hô hấp, tan máu, đông máu rải rác gr] the





    pva
    BAO QUAN: Dé thuốc nơi khô mát, thoáng mát, nhiệt độ dưới ve
    Để thuốc xa tẩm tay trẻ em.
    AN DUNG: 36 tháng kể từ ngày sản xuất.
    TIÊU CHUẨN ÁP DỤNG: Tiêu chuẩn cơ sở
    'CÍ BOC KY HUONG DẪN SỬ DỤNG TRƯỚC KHI DÙNG
    e +\ NEU CAN THEM THÔNG TIN, XIN HỒI Ý KIẾN CỦA BÁC SỸ .
    , \ THONG BAO CHO BAC SY NHUNG TAC DUNG KHONG MONG MUON GAP PHAN KKHI SỬ DỤNG THUỐC

    LenHl VPC CÔNG TY CỔ PHAN DƯỢC PHẨM CỬU LONG7E Jj Pharmaxeo 150 đường 14/9 - Phường 5 - Tp Vĩnh Long“Bins goa TRƯỞNG
    rung Nouyin Vin Ghand
    """

# Câu hỏi cần tìm kiếm trong văn bản
question = "Đây là thông tin của một loại thuốc, tôi cần trích cặp hoạt chất tương tác thuốc với nhau và hậu quả của nó ?"

# Dự đoán câu trả lời
result = qa_pipeline(question=question, context=text)
print(result["answer"])
