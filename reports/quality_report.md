# Vietnamese News Diversity — Phase 1 Data-Quality Report

*Supply-side snapshot. Descriptive completeness check on the published cross-section; no exposure or substantive-coverage claims.*

- **Generated:** 2026-06-24T22:14:22.216652+07:00
- **Window:** 2026-06-03 → 2026-06-24 (Asia/Ho_Chi_Minh)
- **Articles:** 2832  |  **Outlets:** 16  |  **Sections observed:** 723
- **Segmentation:** {'underthesea': 2816} (token counts)


## 1. Articles per outlet

| outlet | outlet_type | articles |
| --- | --- | --- |
| nhandan | party_official | 303 |
| tuoitre | union_mass_daily | 277 |
| vnexpress | semi_commercial | 259 |
| tienphong | union_mass_daily | 200 |
| dantri | semi_commercial | 193 |
| 24h | popular_lifestyle | 191 |
| vietnamnet | semi_commercial | 184 |
| vietnamplus | party_official | 182 |
| qdnd | party_official | 176 |
| saostar | popular_lifestyle | 165 |
| vneconomy | sector_business | 128 |
| cafef | sector_business | 124 |
| kenh14 | popular_lifestyle | 124 |
| thanhnien | union_mass_daily | 121 |
| soha | popular_lifestyle | 120 |
| baochinhphu | party_official | 85 |

![Articles per outlet](figures/articles_per_outlet.png)


## 2. Articles per outlet × section

_Section provenance differs by outlet, which is itself a measurement-validity observation (not a data error). VnExpress and Tuổi Trẻ supply clean per-section RSS, so their `section` values are controlled slugs (`thoi-su`, `phap-luat`, …). Nhân Dân (party_official) exposes no reliable per-section feed and uses flat article URLs; its `section` is recovered from page categories where present — natural-language labels mixing topical and geographic taxonomies (`Thể thao`, `Môi trường`, `Duyên hải Nam Trung Bộ và Tây Nguyên`) — and `(none)` otherwise. The section vocabulary is therefore not directly comparable across outlet types and will need harmonisation before any section-based diversity metric._


| outlet | section | articles |
| --- | --- | --- |
| 24h | Ronaldo | 5 |
| 24h | Hà Nội | 3 |
| 24h | giá vàng | 3 |
| 24h | lich thi dau bong da | 3 |
| 24h | (none) | 2 |
| 24h | Bóng đá 24h | 2 |
| 24h | Giá vàng hôm nay | 2 |
| 24h | Iran | 2 |
| 24h | Lisa | 2 |
| 24h | Messi | 2 |
| 24h | Putin | 2 |
| 24h | Quỳnh Anh Shyn | 2 |
| 24h | Scotland | 2 |
| 24h | dự báo thời tiết | 2 |
| 24h | mỹ | 2 |
| 24h | nga | 2 |
| 24h | ĐT Anh | 2 |
| 24h | 4 suối thác tự nhiên gần Hà Nội | 1 |
| 24h | ADN | 1 |
| 24h | Andy Burnham | 1 |
| 24h | Apple | 1 |
| 24h | BHXH | 1 |
| 24h | Biệt thự 525 m2 | 1 |
| 24h | Brooklyn Beckham | 1 |
| 24h | Bảo Ngọc | 1 |
| 24h | Bồ Đào Nha | 1 |
| 24h | CHDC Congo Colombia | 1 |
| 24h | Chồng ghen tuông | 1 |
| 24h | Declan Rice | 1 |
| 24h | Elma | 1 |
| 24h | Elon Musk | 1 |
| 24h | FBI | 1 |
| 24h | Giá bạc | 1 |
| 24h | Giẫm đạp | 1 |
| 24h | Gu mặc | 1 |
| 24h | HLV Deschamps | 1 |
| 24h | Honda Prelude Limited Edition | 1 |
| 24h | Honda Vario 125 | 1 |
| 24h | Hồng Đăng du lịch | 1 |
| 24h | Keito Nakamura | 1 |
| 24h | Kiểm sát viên | 1 |
| 24h | Lê Phương | 1 |
| 24h | Lý Kim Minh | 1 |
| 24h | Lý lịch tư pháp | 1 |
| 24h | Mai Phương Thuý | 1 |
| 24h | Mercedes | 1 |
| 24h | Mức phí 13 tuyến cao tốc Bắc - Nam | 1 |
| 24h | Mỹ | 1 |
| 24h | Mỹ Tâm | 1 |
| 24h | Neymar Junior | 1 |
| 24h | Nga | 1 |
| 24h | Ngoại trưởng Mỹ | 1 |
| 24h | Ngọc Quỳnh | 1 |
| 24h | Nhận định bóng đá | 1 |
| 24h | Nàng hậu Thái Lan | 1 |
| 24h | Núi Cấm | 1 |
| 24h | Omoda C5 | 1 |
| 24h | OnePlus 13 | 1 |
| 24h | Panama | 1 |
| 24h | Pháp | 1 |
| 24h | Quang Hải | 1 |
| 24h | Realme p4x 4g | 1 |
| 24h | Ronaldo Bồ Đào Nha | 1 |
| 24h | Ronaldo Ibrahimovic | 1 |
| 24h | Tai nghe | 1 |
| 24h | Thành nhà Hồ | 1 |
| 24h | Thượng viện Mỹ | 1 |
| 24h | Thủ khoa | 1 |
| 24h | Timothée Chalamet | 1 |
| 24h | Tiểu Long Nữ | 1 |
| 24h | Toyota Camry | 1 |
| 24h | Triều Tiên | 1 |
| 24h | Trái Đất | 1 |
| 24h | Tây Ninh | 1 |
| 24h | Tướng Donahue | 1 |
| 24h | Tập đoàn Sơn Hải | 1 |
| 24h | Tụ điện | 1 |
| 24h | Viện KSND TP.HCM | 1 |
| 24h | Việt Nam | 1 |
| 24h | Vĩnh Long | 1 |
| 24h | Vương Sở Nhiên | 1 |
| 24h | World Cup 2026 | 1 |
| 24h | Xe MPV | 1 |
| 24h | Xioban | 1 |
| 24h | Yamal | 1 |
| 24h | biển số giả | 1 |
| 24h | bong chuyen nu | 1 |
| 24h | bác tin bão số 3 | 1 |
| 24h | bóng đá 24h | 1 |
| 24h | clip 1 phút | 1 |
| 24h | clip phút 90+ | 1 |
| 24h | con ac ac wimbledon | 1 |
| 24h | da mụn | 1 |
| 24h | du lịch hội an | 1 |
| 24h | dứa | 1 |
| 24h | giá mắc cọp | 1 |
| 24h | giá vàng hôm nay | 1 |
| 24h | giá xăng | 1 |
| 24h | giá xăng dầu | 1 |
| 24h | giảm cân | 1 |
| 24h | giấy chứng nhận quyền sử dụng đất | 1 |
| 24h | honda click 125 | 1 |
| 24h | hà nội | 1 |
| 24h | học phí khối Y Dược | 1 |
| 24h | học thuyết quân sự iran | 1 |
| 24h | hố đen ngủ đông | 1 |
| 24h | iPhone | 1 |
| 24h | iPhone 18 Pro | 1 |
| 24h | iphone | 1 |
| 24h | lich thi dau bong da hom nay va ngay mai | 1 |
| 24h | lich thi dau world cup 2026 | 1 |
| 24h | loại rau | 1 |
| 24h | lương hưu | 1 |
| 24h | lừa tình | 1 |
| 24h | mang hung khí điều khiển xe mô tô | 1 |
| 24h | mâm cơm gia đình | 1 |
| 24h | mây ngũ sắc | 1 |
| 24h | mã độc WhatsApp | 1 |
| 24h | nang wags | 1 |
| 24h | ngộ độc thực phẩm | 1 |
| 24h | ngủ đủ giấc | 1 |
| 24h | nong ruc khan dai world cup | 1 |
| 24h | nắng nóng | 1 |
| 24h | nợ lương | 1 |
| 24h | phong cách mùa hè 2026 | 1 |
| 24h | phường Thanh Xuân | 1 |
| 24h | phẫu thuật | 1 |
| 24h | quyền riêng tư | 1 |
| 24h | quầng mặt trời | 1 |
| 24h | rút BHXH một lần | 1 |
| 24h | sát hạch lái xe | 1 |
| 24h | sử dụng điện thoại | 1 |
| 24h | tai nạn giao thông | 1 |
| 24h | tennis dinh cao | 1 |
| 24h | thành phố Bắc Ninh | 1 |
| 24h | thác Bản Giốc | 1 |
| 24h | thời tiết Hà Nội | 1 |
| 24h | thủ tục hành chính | 1 |
| 24h | tim mạch | 1 |
| 24h | tinh hà say hi | 1 |
| 24h | trái cây nhập khẩu | 1 |
| 24h | trực tiếp bóng đá | 1 |
| 24h | tuyển sinh đại học | 1 |
| 24h | tên lửa | 1 |
| 24h | tôm khô | 1 |
| 24h | tăng nặng mức phạt | 1 |
| 24h | tổ dân phố | 1 |
| 24h | tỷ giá usd | 1 |
| 24h | tỷ phú | 1 |
| 24h | ung thư dạ dày | 1 |
| 24h | ung thư gan | 1 |
| 24h | viêm cơ tim | 1 |
| 24h | vo gạo trước khi nấu cơm | 1 |
| 24h | vo tien minh | 1 |
| 24h | vé điện tử liên thông | 1 |
| 24h | vợ Duy Mạnh | 1 |
| 24h | xe máy | 1 |
| 24h | xét tuyển đại học | 1 |
| 24h | xăng E10 | 1 |
| 24h | Ông Nawat lo ngại về Miss Universe Vietnam | 1 |
| 24h | Điểm chuẩn | 1 |
| 24h | Điện lực TPHCM | 1 |
| 24h | Đề thi môn Văn | 1 |
| 24h | Đỗ Mỹ Linh sau sinh | 1 |
| 24h | Đội tuyển bóng đá Iran | 1 |
| 24h | điều hòa | 1 |
| 24h | điểm chuẩn vào lớp 10 | 1 |
| 24h | đêm tân hôn | 1 |
| baochinhphu | (none) | 22 |
| baochinhphu | Chủ tịch Quốc hội | 3 |
| baochinhphu | Phó Thủ tướng | 3 |
| baochinhphu | Tổng Bí thư | 3 |
| baochinhphu | Vĩnh Long | 3 |
| baochinhphu | Cần Thơ | 2 |
| baochinhphu | Nghị quyết 57-NQ/TW | 2 |
| baochinhphu | Phạm Gia Túc | 2 |
| baochinhphu | ACB | 1 |
| baochinhphu | Agribank | 1 |
| baochinhphu | Chiến lược tài chính | 1 |
| baochinhphu | Cơ quan điều tra | 1 |
| baochinhphu | Hộ kinh doanh | 1 |
| baochinhphu | Nestlé MILO | 1 |
| baochinhphu | Người cao tuổi | 1 |
| baochinhphu | PetroVietnam | 1 |
| baochinhphu | Sếu đầu đỏ | 1 |
| baochinhphu | Sở hữu trí tuệ | 1 |
| baochinhphu | Thanh Tra | 1 |
| baochinhphu | Vinachem | 1 |
| baochinhphu | Y tế | 1 |
| baochinhphu | an ninh phi truyền thống | 1 |
| baochinhphu | bác sĩ | 1 |
| baochinhphu | bảo hiểm bắt buộc trong xây dựng\ | 1 |
| baochinhphu | bảo tàng mỹ thuật việt nam | 1 |
| baochinhphu | công nghệ hiện đại | 1 |
| baochinhphu | giao thông | 1 |
| baochinhphu | giấy phép xây dựng | 1 |
| baochinhphu | hoạt động bay | 1 |
| baochinhphu | hài cốt liệt sĩ | 1 |
| baochinhphu | khoa học | 1 |
| baochinhphu | liên bang nga | 1 |
| baochinhphu | miễn thuế | 1 |
| baochinhphu | nghỉ việc | 1 |
| baochinhphu | nhà giáo ưu tú | 1 |
| baochinhphu | phó thủ tướng thường trực | 1 |
| baochinhphu | phường | 1 |
| baochinhphu | thu ngân sách | 1 |
| baochinhphu | thủ tướng | 1 |
| baochinhphu | trường học biên giới | 1 |
| baochinhphu | tín dụng xanh | 1 |
| baochinhphu | tăng trưởng hai con số | 1 |
| baochinhphu | tỉnh Điện Biên | 1 |
| baochinhphu | vi phạm | 1 |
| baochinhphu | văn hóa | 1 |
| baochinhphu | vận tải | 1 |
| baochinhphu | vốn tín dụng chính sách | 1 |
| baochinhphu | xăng E10 | 1 |
| baochinhphu | Đoàn Thanh niên Chính phủ | 1 |
| baochinhphu | Đà Nẵng | 1 |
| baochinhphu | Đại học Nam Cần Thơ | 1 |
| baochinhphu | đo lường | 1 |
| baochinhphu | đăng ký doanh nghiệp | 1 |
| cafef | trung quốc | 7 |
| cafef | việt nam | 4 |
| cafef | Bắc Ninh | 3 |
| cafef | bất động sản | 3 |
| cafef | cổ phiếu | 3 |
| cafef | nga | 3 |
| cafef | (none) | 2 |
| cafef | Google | 2 |
| cafef | dự án | 2 |
| cafef | ngân hàng | 2 |
| cafef | vàng | 2 |
| cafef | 2 loại nước | 1 |
| cafef | 5 loại cá | 1 |
| cafef | Apple | 1 |
| cafef | Bắt tạm giam Giám đốc | 1 |
| cafef | Bộ Tài chính | 1 |
| cafef | Công an TP Đà Nẵng | 1 |
| cafef | Công an điều tra về số tiền | 1 |
| cafef | DIC Corp | 1 |
| cafef | Dự án quan trọng của Nga | 1 |
| cafef | Galaxy Cruiser 700 | 1 |
| cafef | Khởi tố | 1 |
| cafef | Messi | 1 |
| cafef | Móng tay | 1 |
| cafef | Mẹ đảm miền Tây | 1 |
| cafef | Nam MC giàu nhất nhì Việt Nam | 1 |
| cafef | Nam sinh | 1 |
| cafef | Nam sinh mê Toán | 1 |
| cafef | Neymar | 1 |
| cafef | Ngành ngoại ngữ | 1 |
| cafef | Nhà hát kịch Việt Nam | 1 |
| cafef | Nắng nóng cực đoan | 1 |
| cafef | Phát hiện 30 kg vàng | 1 |
| cafef | Phương Thanh | 1 |
| cafef | Phạm Nhật Vượng | 1 |
| cafef | Sun PhuQuoc Airways | 1 |
| cafef | Tin vui: Từ 1/7 | 1 |
| cafef | Trường THPT | 1 |
| cafef | Trường Đại học Y Dược Hải Phòng | 1 |
| cafef | Trợ lý cảnh sát | 1 |
| cafef | Tài khoản không sử dụng | 1 |
| cafef | VietJet | 1 |
| cafef | Vietnam Airlines | 1 |
| cafef | Vinspeed | 1 |
| cafef | WinCommerce | 1 |
| cafef | anker | 1 |
| cafef | bizfly | 1 |
| cafef | bãi biển | 1 |
| cafef | bảo hiểm nhân thọ | 1 |
| cafef | chuyển khoản | 1 |
| cafef | châu âu | 1 |
| cafef | công an | 1 |
| cafef | công nghệ | 1 |
| cafef | cơ quan thuế | 1 |
| cafef | cửa trượt nhà bếp | 1 |
| cafef | doanh nghiệp Việt | 1 |
| cafef | donald trump | 1 |
| cafef | evn | 1 |
| cafef | gia vị | 1 |
| cafef | giá điện | 1 |
| cafef | giấy tờ | 1 |
| cafef | giới siêu giàu | 1 |
| cafef | hoa hậu | 1 |
| cafef | huyền thoại | 1 |
| cafef | hải sản | 1 |
| cafef | iran | 1 |
| cafef | khách hàng | 1 |
| cafef | lừa đảo | 1 |
| cafef | malaysia | 1 |
| cafef | miền Tây | 1 |
| cafef | mệnh Kim | 1 |
| cafef | ngân hàng nhà nước | 1 |
| cafef | ngọc trinh | 1 |
| cafef | nhnn | 1 |
| cafef | nhà đầu tư | 1 |
| cafef | nhà ở xã hội | 1 |
| cafef | nhập viện | 1 |
| cafef | nắng nóng | 1 |
| cafef | pin | 1 |
| cafef | quy định mới | 1 |
| cafef | quốc lộ 13 | 1 |
| cafef | ra mắt | 1 |
| cafef | samsung | 1 |
| cafef | sống lâu | 1 |
| cafef | thi hành lệnh bắt tạm giam | 1 |
| cafef | thương mại điện tử | 1 |
| cafef | thị trường | 1 |
| cafef | trồng lúa | 1 |
| cafef | tập đoàn Sơn Hải | 1 |
| cafef | vietinbank | 1 |
| cafef | vinasoy | 1 |
| cafef | vải thiều | 1 |
| cafef | vận tải biển | 1 |
| cafef | wimbledon | 1 |
| cafef | xe máy | 1 |
| cafef | xem TV | 1 |
| cafef | xăng dầu | 1 |
| cafef | xới cơm | 1 |
| cafef | Đóng BHXH | 1 |
| cafef | đen vâu | 1 |
| cafef | điện thoại đang bị theo dõi | 1 |
| cafef | đại học | 1 |
| dantri | Thời sự | 27 |
| dantri | Pháp luật | 21 |
| dantri | Kinh doanh | 20 |
| dantri | Thế giới | 19 |
| dantri | Sức khỏe | 18 |
| dantri | Thể thao | 14 |
| dantri | Nội vụ | 12 |
| dantri | Đời sống | 12 |
| dantri | (none) | 10 |
| dantri | Giáo dục | 10 |
| dantri | Bất động sản | 9 |
| dantri | Giải trí | 9 |
| dantri | Công nghệ | 6 |
| dantri | Du lịch | 2 |
| dantri | Khoa học | 1 |
| dantri | Lao động - Việc làm | 1 |
| dantri | Tâm điểm | 1 |
| dantri | Tấm lòng nhân ái | 1 |
| kenh14 | (none) | 11 |
| kenh14 | World Cup 2026 | 5 |
| kenh14 | thể thao | 5 |
| kenh14 | nắng nóng | 4 |
| kenh14 | ronaldo | 4 |
| kenh14 | đời sống | 4 |
| kenh14 | World Cup | 3 |
| kenh14 | giải trí | 3 |
| kenh14 | Kpop | 2 |
| kenh14 | Z-School Tour | 2 |
| kenh14 | bạo hành | 2 |
| kenh14 | dân văn phòng | 2 |
| kenh14 | giá vàng hôm nay | 2 |
| kenh14 | messi | 2 |
| kenh14 | phạt nguội | 2 |
| kenh14 | 14 triệu người dân ở TP.HCM nhận tin vui | 1 |
| kenh14 | Bác sĩ Bạch Mai cảnh báo | 1 |
| kenh14 | Bắc Ninh | 1 |
| kenh14 | Ca sĩ Việt | 1 |
| kenh14 | Dương tử | 1 |
| kenh14 | Facebook | 1 |
| kenh14 | Gan tổn thương | 1 |
| kenh14 | Google | 1 |
| kenh14 | Hà Nội | 1 |
| kenh14 | Long Châu | 1 |
| kenh14 | Luộc thịt | 1 |
| kenh14 | Lý Kim Minh | 1 |
| kenh14 | MC Đại Nghĩa | 1 |
| kenh14 | Mua nhà | 1 |
| kenh14 | Máy bay | 1 |
| kenh14 | Mặt trời | 1 |
| kenh14 | NSƯT Ngọc Quỳnh | 1 |
| kenh14 | Phạm Quỳnh Anh | 1 |
| kenh14 | Phế cầu khuẩn | 1 |
| kenh14 | Psi Scott | 1 |
| kenh14 | Pun | 1 |
| kenh14 | Rosé | 1 |
| kenh14 | Starbucks | 1 |
| kenh14 | Sỏi bàng quang | 1 |
| kenh14 | TP.HCM | 1 |
| kenh14 | Thi vào lớp 10 | 1 |
| kenh14 | Vinamilk | 1 |
| kenh14 | Võ Hà Linh | 1 |
| kenh14 | Xét xử | 1 |
| kenh14 | Yeah1 | 1 |
| kenh14 | bellingham | 1 |
| kenh14 | chuyển khoản | 1 |
| kenh14 | chuyển khoản nhầm | 1 |
| kenh14 | chất gây ung thư | 1 |
| kenh14 | croatia | 1 |
| kenh14 | cắt điện | 1 |
| kenh14 | giấy tờ | 1 |
| kenh14 | graff | 1 |
| kenh14 | hạ cánh | 1 |
| kenh14 | iPhone 18 Pro Max | 1 |
| kenh14 | lyly | 1 |
| kenh14 | lãi suất ngân hàng | 1 |
| kenh14 | lịch sử | 1 |
| kenh14 | lớp 10 | 1 |
| kenh14 | miền bắc nắng nóng | 1 |
| kenh14 | mua xe máy | 1 |
| kenh14 | mỹ nhân | 1 |
| kenh14 | ngư dân | 1 |
| kenh14 | ngọc trinh | 1 |
| kenh14 | nhiễm HIV | 1 |
| kenh14 | nhà cháy | 1 |
| kenh14 | nạp tiền | 1 |
| kenh14 | phim ngôn tình | 1 |
| kenh14 | phim trung quốc | 1 |
| kenh14 | phạm băng băng | 1 |
| kenh14 | thiếu nữ bỏ nhà đi | 1 |
| kenh14 | thành công | 1 |
| kenh14 | thịt lợn | 1 |
| kenh14 | tranh cãi | 1 |
| kenh14 | tránh nắng | 1 |
| kenh14 | trần triết viễn | 1 |
| kenh14 | tuyển anh | 1 |
| kenh14 | tôm khô | 1 |
| kenh14 | ung thư | 1 |
| kenh14 | vỡ hoàng thể | 1 |
| kenh14 | ông Phạm Nhật Vượng | 1 |
| kenh14 | Đường sắt mở Đoàn tàu Bạch Mai | 1 |
| kenh14 | Đặng Triệu Tôn | 1 |
| kenh14 | điều hòa | 1 |
| kenh14 | điện thoại | 1 |
| kenh14 | đập gương | 1 |
| nhandan | Kinh tế | 33 |
| nhandan | Xã hội | 32 |
| nhandan | Chính trị | 31 |
| nhandan | Tin chung | 26 |
| nhandan | Thể thao | 22 |
| nhandan | Đồng bằng sông Hồng | 22 |
| nhandan | Văn hóa | 16 |
| nhandan | Châu Âu | 14 |
| nhandan | Y tế | 14 |
| nhandan | Môi trường | 13 |
| nhandan | Thế giới | 10 |
| nhandan | (none) | 7 |
| nhandan | Duyên hải Nam Trung Bộ và Tây Nguyên | 7 |
| nhandan | Khoa học - Công nghệ | 6 |
| nhandan | Ảnh | 6 |
| nhandan | Giáo dục | 5 |
| nhandan | Pháp luật | 5 |
| nhandan | Văn hóa - Văn nghệ | 5 |
| nhandan | Bạn cần biết | 3 |
| nhandan | Châu Á-TBD | 3 |
| nhandan | Thời Nay | 3 |
| nhandan | Trung Đông | 3 |
| nhandan | Bình luận quốc tế | 2 |
| nhandan | Bạn đọc | 2 |
| nhandan | Chuyên trang Hà Nội | 2 |
| nhandan | Châu Phi | 2 |
| nhandan | Chuyển đổi số | 1 |
| nhandan | Châu Mỹ | 1 |
| nhandan | Hành động và thách thức | 1 |
| nhandan | Infographic | 1 |
| nhandan | NHÂN DÂN HẰNG THÁNG | 1 |
| nhandan | Văn hóa làng quê | 1 |
| nhandan | Xây dựng nông thôn mới | 1 |
| nhandan | Xây dựng Đảng | 1 |
| nhandan | Đồng bằng sông Cửu Long | 1 |
| qdnd | World Cup | 9 |
| qdnd | World Cup 2026 | 6 |
| qdnd | Ronaldo | 4 |
| qdnd | Cảnh sát biển | 3 |
| qdnd | Quân khu 4 | 3 |
| qdnd | Tổng Bí thư | 3 |
| qdnd | Đoàn TNCS Hồ Chí Minh | 3 |
| qdnd | An Giang | 2 |
| qdnd | Campuchia | 2 |
| qdnd | Iran | 2 |
| qdnd | Messi | 2 |
| qdnd | Mỹ | 2 |
| qdnd | Nga | 2 |
| qdnd | Quân khu 2 | 2 |
| qdnd | Quân khu 5 | 2 |
| qdnd | Quân đoàn 34 | 2 |
| qdnd | eo biển Hormuz | 2 |
| qdnd | nhà ở | 2 |
| qdnd | Đắk Lắk | 2 |
| qdnd | (none) | 1 |
| qdnd | AIDS | 1 |
| qdnd | ASEAN | 1 |
| qdnd | Binh đoàn 16 | 1 |
| qdnd | Biên phòng Cửa khẩu Săm Pun | 1 |
| qdnd | Bosnia và Qatar | 1 |
| qdnd | Bác Hồ | 1 |
| qdnd | Bảng xếp hạng World Cup 2026 hôm nay | 1 |
| qdnd | Bảo hiểm | 1 |
| qdnd | Bảo tàng Phụ nữ Việt Nam | 1 |
| qdnd | Bắc Ninh | 1 |
| qdnd | Bệnh viện đa khoa Hòe Nhai | 1 |
| qdnd | Bộ Tổng tham mưu | 1 |
| qdnd | Bộ tư lệnh 86 | 1 |
| qdnd | Cao Bằng | 1 |
| qdnd | Chuẩn úy Palina Dalasin | 1 |
| qdnd | Chính phủ | 1 |
| qdnd | Chính trường Anh | 1 |
| qdnd | Chứng khoán | 1 |
| qdnd | Công an TP Hà Nội | 1 |
| qdnd | Cần Thơ | 1 |
| qdnd | Cục Quân khí | 1 |
| qdnd | Donald Trump | 1 |
| qdnd | Giá hồ tiêu | 1 |
| qdnd | Giá vàng | 1 |
| qdnd | Hà Tĩnh | 1 |
| qdnd | Hải đội 202 | 1 |
| qdnd | Học viện Quân y | 1 |
| qdnd | Học viện Quốc phòng | 1 |
| qdnd | IAEA | 1 |
| qdnd | Israel | 1 |
| qdnd | Khánh Hòa | 1 |
| qdnd | LLVT tỉnh Quảng Ninh | 1 |
| qdnd | Laura | 1 |
| qdnd | Link xem trực tiếp Bồ Đào Nha | 1 |
| qdnd | Link xem trực tiếp Colombia và Cộng hòa dân chủ Congo | 1 |
| qdnd | Link xem trực tiếp Panama và Croatia | 1 |
| qdnd | Lào Cai | 1 |
| qdnd | Lịch thi đấu World Cup 2026 hôm nay | 1 |
| qdnd | Lữ đoàn 162 | 1 |
| qdnd | Lữ đoàn 596 | 1 |
| qdnd | Mexico City | 1 |
| qdnd | Mộc bản triều Nguyễn | 1 |
| qdnd | New Zealand | 1 |
| qdnd | Nghệ An | 1 |
| qdnd | Nhà máy Z115 | 1 |
| qdnd | Nhận định Scotland và Brazil | 1 |
| qdnd | Phó chủ tịch nước Võ Thị Ánh Xuân | 1 |
| qdnd | Quân khu 3 | 1 |
| qdnd | Quân đoàn 12 | 1 |
| qdnd | Quân ủy Trung ương | 1 |
| qdnd | Quảng Ninh | 1 |
| qdnd | TP Hồ Chí Minh | 1 |
| qdnd | Thanh Hóa | 1 |
| qdnd | Thủ tướng | 1 |
| qdnd | Thủ tướng Anh | 1 |
| qdnd | Thủy thủ | 1 |
| qdnd | Tin thể thao | 1 |
| qdnd | Trung Quốc | 1 |
| qdnd | Trung tá QNCN Đinh Thị Hà | 1 |
| qdnd | Trung đoàn 102 | 1 |
| qdnd | Trung đoàn 754 | 1 |
| qdnd | Trung đoàn 88 | 1 |
| qdnd | Trường Sa | 1 |
| qdnd | Trường Sĩ quan Chính trị | 1 |
| qdnd | Trần Phi Hổ | 1 |
| qdnd | Tân cảng | 1 |
| qdnd | Tô Văn Đực | 1 |
| qdnd | Tự chủ đại học | 1 |
| qdnd | UN Women | 1 |
| qdnd | UNICEF | 1 |
| qdnd | VPBank | 1 |
| qdnd | Video bàn thắng Colombia và CHDC Congo | 1 |
| qdnd | Video bàn thắng Croatia và Panama | 1 |
| qdnd | Video trận đấu Anh và Ghana | 1 |
| qdnd | Viện Khoa học và Công nghệ quân sự | 1 |
| qdnd | Vòm Vàng | 1 |
| qdnd | Vùng 3 Hải quân | 1 |
| qdnd | Vùng Cảnh sát biển 4 | 1 |
| qdnd | Vị Xuyên | 1 |
| qdnd | Xe máy | 1 |
| qdnd | bóng đá | 1 |
| qdnd | chiến dịch 500 ngày đêm | 1 |
| qdnd | chiến tranh | 1 |
| qdnd | chính quyền địa phương hai cấp | 1 |
| qdnd | diễn biến hòa bình | 1 |
| qdnd | diễn tập | 1 |
| qdnd | giá dầu | 1 |
| qdnd | giá vàng hôm nay | 1 |
| qdnd | gìn giữ hòa bình | 1 |
| qdnd | hài cốt liệt sĩ | 1 |
| qdnd | hàng không Mỹ | 1 |
| qdnd | kinh tế tập thể | 1 |
| qdnd | lịch sử | 1 |
| qdnd | mẫu sinh phẩm ADN | 1 |
| qdnd | mẹ Việt Nam Anh hùng | 1 |
| qdnd | nghiệp vụ công tác văn phòng | 1 |
| qdnd | ngành xuất bản | 1 |
| qdnd | ngư dân | 1 |
| qdnd | người cao tuổi | 1 |
| qdnd | nhiếp ảnh | 1 |
| qdnd | nhà giàn | 1 |
| qdnd | nông sản | 1 |
| qdnd | phường Tây Hồ | 1 |
| qdnd | quân sự | 1 |
| qdnd | thời tiết hôm nay | 1 |
| qdnd | trường Đại học Thủ Dầu Một | 1 |
| qdnd | tài xế công nghệ | 1 |
| qdnd | tỉnh Gia Lai | 1 |
| qdnd | tỉnh Điện Biên | 1 |
| qdnd | tỷ giá USD | 1 |
| qdnd | video bàn thắng Bồ Đào Nha | 1 |
| qdnd | xác nhận nhập học | 1 |
| qdnd | Điện Biên | 1 |
| qdnd | Đoàn Kinh tế | 1 |
| qdnd | Đoàn Văn công Quân đội nhân dân Lào | 1 |
| qdnd | Đại tá VĂN MẠNH SOÁI | 1 |
| qdnd | Đất đai | 1 |
| qdnd | Đồng Nai | 1 |
| qdnd | đại học | 1 |
| qdnd | đội tuyển Việt Nam | 1 |
| saostar | Phim ảnh | 49 |
| saostar | Sao | 28 |
| saostar | Âm nhạc | 18 |
| saostar | Sao Sport | 16 |
| saostar | Vòng quanh thế giới | 11 |
| saostar | Cận cảnh cuộc sống | 10 |
| saostar | Người mẫu - Hoa hậu | 10 |
| saostar | Du lịch - Khám phá | 9 |
| saostar | Fashion - Beauty | 4 |
| saostar | BĐS - Tài chính | 3 |
| saostar | Công nghệ | 2 |
| saostar | Học đường | 2 |
| saostar | Ăn - Chơi | 2 |
| saostar | Sức khỏe | 1 |
| soha | (none) | 35 |
| soha | World Cup | 6 |
| soha | Trung Quốc | 3 |
| soha | sao Việt | 3 |
| soha | báo công an | 2 |
| soha | công an TP Hà Nội | 2 |
| soha | quảng ninh | 2 |
| soha | 5g | 1 |
| soha | BHXH | 1 |
| soha | Brazil | 1 |
| soha | Canada | 1 |
| soha | Claude Mythos | 1 |
| soha | Công an tỉnh Cà Mau | 1 |
| soha | EVN | 1 |
| soha | Facebook nghe lén | 1 |
| soha | HIV | 1 |
| soha | Hành chính công | 1 |
| soha | IAEA | 1 |
| soha | Israel tự sản xuất vũ khí | 1 |
| soha | Kim Jong-un | 1 |
| soha | Lê Thị Hồng Nhung | 1 |
| soha | Mùa nào bệnh nấy | 1 |
| soha | Mỹ | 1 |
| soha | Nguyễn Đình Lâm | 1 |
| soha | Ronaldo | 1 |
| soha | Soha Special | 1 |
| soha | Su-57 | 1 |
| soha | Suzuki | 1 |
| soha | UAV đánh chặn | 1 |
| soha | biệt thự thông minh | 1 |
| soha | bán dâm tại Quảng Đông | 1 |
| soha | bánh ram ít | 1 |
| soha | bỏng nặng | 1 |
| soha | bộ công an | 1 |
| soha | cháy rừng | 1 |
| soha | cách luộc thịt | 1 |
| soha | cây | 1 |
| soha | cảnh báo lừa đảo EVN | 1 |
| soha | cờ bạc trực tuyến | 1 |
| soha | giá vàng giảm | 1 |
| soha | hang động Bắc Na Uy | 1 |
| soha | huỳnh thánh y | 1 |
| soha | hà nội | 1 |
| soha | làm sạch dép Crocs | 1 |
| soha | lương hưu 2026 | 1 |
| soha | lớp 10 | 1 |
| soha | máy bay | 1 |
| soha | mệnh Kim tháng 7 | 1 |
| soha | mừng cưới | 1 |
| soha | nhà máy địa nhiệt | 1 |
| soha | nắng nóng ở Paris | 1 |
| soha | phun thuốc diệt cỏ | 1 |
| soha | quy định kiểm tra thuế | 1 |
| soha | quốc gia | 1 |
| soha | shipper | 1 |
| soha | thu nhập chịu thuế | 1 |
| soha | thẻ vé giao thông | 1 |
| soha | tiêm kích F-35 | 1 |
| soha | tiếng Việt | 1 |
| soha | tiết kiệm | 1 |
| soha | trẻ em tử vong vì nóng | 1 |
| soha | trồng cây | 1 |
| soha | tuyển dụng giả gấu | 1 |
| soha | tài khoản ngân hàng | 1 |
| soha | tỉnh thái nguyên | 1 |
| soha | world cup 2026 | 1 |
| soha | xe cảnh sát | 1 |
| soha | xử lý hành chính | 1 |
| soha | âm thanh lạ từ quan tài | 1 |
| soha | ô tô bị chém kính | 1 |
| soha | điện thoại đang bị theo dõi | 1 |
| soha | đuối nước | 1 |
| soha | đường dây ma túy | 1 |
| soha | ủy quyền nhận lương hưu | 1 |
| thanhnien | Thời sự | 21 |
| thanhnien | Thế giới | 12 |
| thanhnien | Giới trẻ | 10 |
| thanhnien | World Cup 2026 | 9 |
| thanhnien | Kinh tế | 6 |
| thanhnien | Cộng đồng | 5 |
| thanhnien | Đời nghệ sĩ | 5 |
| thanhnien | Giáo dục | 4 |
| thanhnien | Sức khỏe | 4 |
| thanhnien | Tin tức công nghệ | 4 |
| thanhnien | Bóng đá Việt Nam | 3 |
| thanhnien | Bạn cần biết | 3 |
| thanhnien | Dân sinh | 3 |
| thanhnien | Pháp luật | 3 |
| thanhnien | Thị trường | 3 |
| thanhnien | Đời sống | 3 |
| thanhnien | Khỏe đẹp mỗi ngày | 2 |
| thanhnien | Văn hóa | 2 |
| thanhnien | Ẩm thực | 2 |
| thanhnien | Chuyện lạ | 1 |
| thanhnien | Chính sách - Phát triển | 1 |
| thanhnien | Chống tin giả | 1 |
| thanhnien | Các môn khác | 1 |
| thanhnien | Câu chuyện văn hóa | 1 |
| thanhnien | Game | 1 |
| thanhnien | Giải trí | 1 |
| thanhnien | Kinh tế xanh | 1 |
| thanhnien | Làm đẹp | 1 |
| thanhnien | Ngân hàng | 1 |
| thanhnien | Phim | 1 |
| thanhnien | Quân sự | 1 |
| thanhnien | Thời trang 24/7 | 1 |
| thanhnien | Thủ thuật | 1 |
| thanhnien | Tin tức - Sự kiện | 1 |
| thanhnien | Tin tức thời sự nhanh 24h | 1 |
| thanhnien | Địa ốc | 1 |
| tienphong | Xã hội | 40 |
| tienphong | Pháp luật | 16 |
| tienphong | Bóng đá | 14 |
| tienphong | Sinh viên Việt Nam | 13 |
| tienphong | Kinh tế | 12 |
| tienphong | Thế giới | 12 |
| tienphong | Hoa học trò | 11 |
| tienphong | Hậu trường sao | 6 |
| tienphong | Nhịp sống | 6 |
| tienphong | Tin tức | 6 |
| tienphong | Âm nhạc | 6 |
| tienphong | Giới trẻ | 5 |
| tienphong | Hậu trường SHOWBIZ | 5 |
| tienphong | Xe | 5 |
| tienphong | Hành trình | 4 |
| tienphong | Khoa học | 4 |
| tienphong | Video | 4 |
| tienphong | Giải trí | 3 |
| tienphong | Sức khỏe | 3 |
| tienphong | Thị trường | 3 |
| tienphong | Tài chính - Chứng khoán | 3 |
| tienphong | Đẹp hơn mỗi ngày | 3 |
| tienphong | Giáo dục | 2 |
| tienphong | Địa ốc | 2 |
| tienphong | (none) | 1 |
| tienphong | Hàng không - Du lịch | 1 |
| tienphong | Học đường | 1 |
| tienphong | Kết nối Hoa Học Trò | 1 |
| tienphong | Media Địa ốc | 1 |
| tienphong | Nhịp sống phương Nam | 1 |
| tienphong | Phim ảnh | 1 |
| tienphong | Sóng xanh | 1 |
| tienphong | Thể thao | 1 |
| tienphong | Tuyển sinh | 1 |
| tienphong | Yêu | 1 |
| tienphong | Ảnh | 1 |
| tuoitre | thoi-su | 95 |
| tuoitre | the-gioi | 69 |
| tuoitre | kinh-doanh | 47 |
| tuoitre | phap-luat | 27 |
| tuoitre | suc-khoe | 21 |
| tuoitre | giao-duc | 18 |
| vietnamnet | World Cup | 33 |
| vietnamnet | Tin tức | 15 |
| vietnamnet | Tuyển sinh | 13 |
| vietnamnet | Thế giới | 11 |
| vietnamnet | Thị trường | 11 |
| vietnamnet | Dân sinh | 9 |
| vietnamnet | Pháp luật | 8 |
| vietnamnet | Thể thao | 8 |
| vietnamnet | Tài chính | 8 |
| vietnamnet | Tin nóng | 7 |
| vietnamnet | Thế giới sao | 5 |
| vietnamnet | Ô tô - Xe máy | 5 |
| vietnamnet | Công nghệ | 4 |
| vietnamnet | Chính trị | 3 |
| vietnamnet | Tư vấn sức khỏe | 3 |
| vietnamnet | Văn hóa - Giải trí | 3 |
| vietnamnet | Bản tin thời sự | 2 |
| vietnamnet | Chân dung | 2 |
| vietnamnet | Dân tộc và Tôn giáo | 2 |
| vietnamnet | Dự án | 2 |
| vietnamnet | Giao thông | 2 |
| vietnamnet | Quân sự | 2 |
| vietnamnet | Quốc phòng | 2 |
| vietnamnet | Đi đâu chơi đi | 2 |
| vietnamnet | (none) | 1 |
| vietnamnet | AI CONTEST | 1 |
| vietnamnet | Bàn luận | 1 |
| vietnamnet | Bóng đá Việt Nam | 1 |
| vietnamnet | Chuyển đổi số | 1 |
| vietnamnet | Chuyện lạ | 1 |
| vietnamnet | Gia đình | 1 |
| vietnamnet | Giới trẻ | 1 |
| vietnamnet | Hạ tầng số | 1 |
| vietnamnet | Kinh doanh | 1 |
| vietnamnet | Mỹ thuật - Sân khấu | 1 |
| vietnamnet | Ngày mai tươi sáng | 1 |
| vietnamnet | Nội dung chuyên đề | 1 |
| vietnamnet | Phim - Truyền hình | 1 |
| vietnamnet | Trắc nghiệm | 1 |
| vietnamnet | Tâm sự | 1 |
| vietnamnet | Tư vấn | 1 |
| vietnamnet | Video | 1 |
| vietnamnet | Xây dựng Đảng | 1 |
| vietnamnet | Ăn Ăn Uống Uống | 1 |
| vietnamnet | Đối ngoại | 1 |
| vietnamnet | Đời sống tôn giáo | 1 |
| vietnamplus | Xã hội | 49 |
| vietnamplus | Thế giới | 29 |
| vietnamplus | Bóng đá | 16 |
| vietnamplus | Đời sống | 15 |
| vietnamplus | Kinh doanh | 14 |
| vietnamplus | Multimedia | 10 |
| vietnamplus | Chính trị | 8 |
| vietnamplus | Công nghệ | 6 |
| vietnamplus | Kinh tế | 6 |
| vietnamplus | Thị trường | 6 |
| vietnamplus | Châu Á-TBD | 5 |
| vietnamplus | Văn hóa | 5 |
| vietnamplus | Bất động sản | 3 |
| vietnamplus | Du lịch | 3 |
| vietnamplus | Chứng khoán | 1 |
| vietnamplus | Doanh nghiệp | 1 |
| vietnamplus | Khoa học ứng dụng | 1 |
| vietnamplus | Pháp luật | 1 |
| vietnamplus | Sản phẩm mới | 1 |
| vietnamplus | Điểm đến | 1 |
| vietnamplus | Điện ảnh | 1 |
| vneconomy | Thế giới | 22 |
| vneconomy | Chứng khoán | 16 |
| vneconomy | Thị trường | 12 |
| vneconomy | Bất động sản | 10 |
| vneconomy | Kinh tế số | 10 |
| vneconomy | Dân sinh | 8 |
| vneconomy | Tiêu điểm | 7 |
| vneconomy | Tài chính | 6 |
| vneconomy | Đầu tư | 6 |
| vneconomy | Kinh tế xanh | 5 |
| vneconomy | Doanh nghiệp | 4 |
| vneconomy | Du lịch | 4 |
| vneconomy | Sức khỏe | 4 |
| vneconomy | Doanh nghiệp niêm yết | 3 |
| vneconomy | Giải trí | 2 |
| vneconomy | Hạ tầng | 2 |
| vneconomy | Đẹp + | 2 |
| vneconomy | Địa phương | 2 |
| vneconomy | Thế | 1 |
| vneconomy | Tiêu & Dùng | 1 |
| vneconomy | Video | 1 |
| vnexpress | suc-khoe | 73 |
| vnexpress | the-gioi | 51 |
| vnexpress | kinh-doanh | 47 |
| vnexpress | thoi-su | 42 |
| vnexpress | phap-luat | 32 |
| vnexpress | giao-duc | 14 |

![Articles per section](figures/articles_per_section.png)


## 3. Articles per publish day

| d | articles |
| --- | --- |
| 2026-06-22 | 178 |
| 2026-06-23 | 443 |
| 2026-06-24 | 2166 |

![Articles per day](figures/articles_per_day.png)


## 4. Missingness by field (% null)

| outlet | n | %miss_body | %miss_section | %miss_publish_datetime | %miss_author |
| --- | --- | --- | --- | --- | --- |
| 24h | 191 | 0.0 | 1.0 | 0.0 | 0.0 |
| baochinhphu | 85 | 0.0 | 25.9 | 0.0 | 0.0 |
| cafef | 124 | 0.0 | 1.6 | 0.0 | 0.0 |
| dantri | 193 | 5.2 | 5.2 | 0.0 | 0.0 |
| kenh14 | 124 | 0.0 | 8.9 | 0.0 | 0.0 |
| nhandan | 303 | 1.3 | 2.3 | 0.0 | 2.3 |
| qdnd | 176 | 0.6 | 0.6 | 0.0 | 0.6 |
| saostar | 165 | 0.0 | 0.0 | 0.0 | 0.0 |
| soha | 120 | 0.0 | 29.2 | 0.0 | 0.0 |
| thanhnien | 121 | 0.0 | 0.0 | 0.0 | 0.0 |
| tienphong | 200 | 0.0 | 0.5 | 0.0 | 0.5 |
| tuoitre | 277 | 0.0 | 0.0 | 0.0 | 0.0 |
| vietnamnet | 184 | 0.5 | 0.5 | 0.0 | 0.5 |
| vietnamplus | 182 | 0.0 | 0.0 | 0.0 | 16.5 |
| vneconomy | 128 | 0.0 | 0.0 | 0.0 | 0.0 |
| vnexpress | 259 | 0.0 | 0.0 | 0.0 | 98.5 |
| ALL | 2832 | 0.6 | 3.2 | 0.0 | 10.4 |

## 5. Article length (Vietnamese word tokens)

| outlet | n_with_body | mean | median |
| --- | --- | --- | --- |
| 24h | 191 | 567.3 | 539.0 |
| baochinhphu | 85 | 871.0 | 727.0 |
| cafef | 124 | 684.3 | 668.5 |
| dantri | 183 | 627.2 | 609.0 |
| kenh14 | 124 | 701.5 | 649.5 |
| nhandan | 299 | 669.8 | 566.0 |
| qdnd | 175 | 533.5 | 436.0 |
| saostar | 165 | 532.5 | 503.0 |
| soha | 120 | 601.0 | 543.5 |
| thanhnien | 121 | 484.5 | 428.0 |
| tienphong | 200 | 514.5 | 441.5 |
| tuoitre | 277 | 490.4 | 425.0 |
| vietnamnet | 183 | 509.7 | 424.0 |
| vietnamplus | 182 | 620.0 | 533.0 |
| vneconomy | 128 | 1146.0 | 1101.5 |
| vnexpress | 259 | 556.9 | 477.0 |

![Mean length per outlet](figures/mean_length_per_outlet.png)


## 6. Language

| lang | articles |
| --- | --- |
| vi | 2816 |
|  | 16 |

_Non-`vi` (flagged): 0._


## 7. Duplication

- Articles with extractable body: **2816**
- Exact-duplicate copies (verbatim body, after first): **20**
- Exact-duplicate rate: **0.7%**
- Distinct content clusters: **2796**
- Cross-outlet verbatim clusters (syndication signal): **14** (28 articles)

- Near-duplicate (same-story) copies: **52** (3.6%), in **41** multi-article clusters
- **Cross-outlet** same-story clusters: **36** (74 articles) — the syndication/overlap signal that exact-hash misses

