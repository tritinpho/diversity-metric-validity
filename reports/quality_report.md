# Vietnamese News Diversity — Phase 1 Data-Quality Report

*Supply-side snapshot. Descriptive completeness check on the published cross-section; no exposure or substantive-coverage claims.*

- **Generated:** 2026-06-27T15:37:57.220338+07:00
- **Window:** 2026-06-06 → 2026-06-27 (Asia/Ho_Chi_Minh)
- **Articles:** 6074  |  **Outlets:** 16  |  **Sections observed:** 1395
- **Segmentation:** {'underthesea': 6049} (token counts)


## 1. Articles per outlet

| outlet | outlet_type | articles |
| --- | --- | --- |
| nhandan | party_official | 525 |
| tuoitre | union_mass_daily | 522 |
| vnexpress | semi_commercial | 482 |
| tienphong | union_mass_daily | 441 |
| dantri | semi_commercial | 427 |
| 24h | popular_lifestyle | 417 |
| vietnamnet | semi_commercial | 404 |
| vietnamplus | party_official | 404 |
| saostar | popular_lifestyle | 402 |
| qdnd | party_official | 390 |
| cafef | sector_business | 305 |
| soha | popular_lifestyle | 300 |
| kenh14 | popular_lifestyle | 299 |
| thanhnien | union_mass_daily | 285 |
| vneconomy | sector_business | 277 |
| baochinhphu | party_official | 194 |

![Articles per outlet](figures/articles_per_outlet.png)


## 2. Articles per outlet × section

_Section provenance differs by outlet, which is itself a measurement-validity observation (not a data error). VnExpress and Tuổi Trẻ supply clean per-section RSS, so their `section` values are controlled slugs (`thoi-su`, `phap-luat`, …). Nhân Dân (party_official) exposes no reliable per-section feed and uses flat article URLs; its `section` is recovered from page categories where present — natural-language labels mixing topical and geographic taxonomies (`Thể thao`, `Môi trường`, `Duyên hải Nam Trung Bộ và Tây Nguyên`) — and `(none)` otherwise. The section vocabulary is therefore not directly comparable across outlet types and will need harmonisation before any section-based diversity metric._


| outlet | section | articles |
| --- | --- | --- |
| 24h | World Cup | 10 |
| 24h | lich thi dau bong da | 10 |
| 24h | Hà Nội | 9 |
| 24h | Ronaldo | 6 |
| 24h | giá vàng | 6 |
| 24h | (none) | 3 |
| 24h | Giá vàng hôm nay | 3 |
| 24h | Iran | 3 |
| 24h | Lisa | 3 |
| 24h | Mỹ | 3 |
| 24h | Putin | 3 |
| 24h | Tây Ninh | 3 |
| 24h | Venezuela | 3 |
| 24h | World Cup 2026 | 3 |
| 24h | giá xăng | 3 |
| 24h | iPhone 18 Pro | 3 |
| 24h | mỹ | 3 |
| 24h | xe máy | 3 |
| 24h | Apple | 2 |
| 24h | Brooklyn Beckham | 2 |
| 24h | Bóng đá 24h | 2 |
| 24h | Cape Verde | 2 |
| 24h | Dương Mịch | 2 |
| 24h | Messi | 2 |
| 24h | Na Uy | 2 |
| 24h | Panama | 2 |
| 24h | Quỳnh Anh Shyn | 2 |
| 24h | Scotland | 2 |
| 24h | Trái Đất | 2 |
| 24h | Tây Ban Nha | 2 |
| 24h | bóng đá 24h | 2 |
| 24h | dự báo thời tiết | 2 |
| 24h | giá bạc | 2 |
| 24h | giá xăng dầu | 2 |
| 24h | kết quả bóng đá | 2 |
| 24h | loại rau | 2 |
| 24h | mâm cơm gia đình | 2 |
| 24h | nga | 2 |
| 24h | tai nạn giao thông | 2 |
| 24h | tỷ giá usd | 2 |
| 24h | ĐT Anh | 2 |
| 24h | điều hòa | 2 |
| 24h | động đất Venezuela | 2 |
| 24h | 4 suối thác tự nhiên gần Hà Nội | 1 |
| 24h | ADN | 1 |
| 24h | Ai Cập - Iran | 1 |
| 24h | Andy Burnham | 1 |
| 24h | BHXH | 1 |
| 24h | Biệt thự 525 m2 | 1 |
| 24h | Bé trai người nhật | 1 |
| 24h | Bảo Anh | 1 |
| 24h | Bảo Ngọc | 1 |
| 24h | Bồ Đào Nha | 1 |
| 24h | CHDC Congo Colombia | 1 |
| 24h | Cape Verde - Saudi Arabia | 1 |
| 24h | Caracas | 1 |
| 24h | Châu Âu | 1 |
| 24h | Chồng ghen tuông | 1 |
| 24h | Cô gái | 1 |
| 24h | Công an phường Phú Thuỷ | 1 |
| 24h | Cận cảnh biệt thự gần 2.000 m2 | 1 |
| 24h | Declan Rice | 1 |
| 24h | Diễm Châu | 1 |
| 24h | Du lịch | 1 |
| 24h | Dương Tử | 1 |
| 24h | Ecuador | 1 |
| 24h | Elma | 1 |
| 24h | Elon Musk | 1 |
| 24h | F1 2026 | 1 |
| 24h | FBI | 1 |
| 24h | FIFA MU World Cup | 1 |
| 24h | Ford Ranger | 1 |
| 24h | Gia Bình | 1 |
| 24h | Giá bạc | 1 |
| 24h | Giúp việc Singapore | 1 |
| 24h | Giẫm đạp | 1 |
| 24h | Giọng ca vàng Bolero | 1 |
| 24h | Gu mặc | 1 |
| 24h | HLV Deschamps | 1 |
| 24h | Harvard | 1 |
| 24h | Honda Prelude Limited Edition | 1 |
| 24h | Honda Vario 125 | 1 |
| 24h | Hyundai | 1 |
| 24h | Hàng nghìn người đội nắng | 1 |
| 24h | Hạm đội 5 | 1 |
| 24h | Hẹ nước | 1 |
| 24h | Hồng Đăng du lịch | 1 |
| 24h | Keito Nakamura | 1 |
| 24h | Khách sạn lâu đài gần 100 tuổi | 1 |
| 24h | Kiểm sát viên | 1 |
| 24h | Kylian Mbappe | 1 |
| 24h | Lukashenko | 1 |
| 24h | Lái xe | 1 |
| 24h | Lãnh Thanh | 1 |
| 24h | Lê Phương | 1 |
| 24h | Lý Kim Minh | 1 |
| 24h | Lý lịch tư pháp | 1 |
| 24h | MC Phí Linh làm MC concert Thanh xuân | 1 |
| 24h | Mai Phương Thuý | 1 |
| 24h | Mazda CX-5 | 1 |
| 24h | Mercedes | 1 |
| 24h | Mercedes-Maybach GLS 480 | 1 |
| 24h | Midu | 1 |
| 24h | Myanmar | 1 |
| 24h | Mức phí 13 tuyến cao tốc Bắc - Nam | 1 |
| 24h | Mỹ Tâm | 1 |
| 24h | NSND Việt Anh | 1 |
| 24h | New Zealand - Bỉ | 1 |
| 24h | Neymar Junior | 1 |
| 24h | Nga | 1 |
| 24h | Ngoại trưởng Mỹ | 1 |
| 24h | Nguyễn Xuân Son | 1 |
| 24h | Ngọc Quỳnh | 1 |
| 24h | Nhiễm chấy rận | 1 |
| 24h | Nhận định bóng đá | 1 |
| 24h | Nhật Bản | 1 |
| 24h | Nhật Bản - Thụy Điển | 1 |
| 24h | Nàng hậu Thái Lan | 1 |
| 24h | Núi Cấm | 1 |
| 24h | Omoda C5 | 1 |
| 24h | One UI 9 | 1 |
| 24h | OnePlus 13 | 1 |
| 24h | Paraguay - Australia | 1 |
| 24h | Pháp | 1 |
| 24h | Phương Trinh Jolie | 1 |
| 24h | Quang Hải | 1 |
| 24h | Quảng Ninh | 1 |
| 24h | RAM | 1 |
| 24h | Realme p4x 4g | 1 |
| 24h | Ronaldo Bồ Đào Nha | 1 |
| 24h | Ronaldo Ibrahimovic | 1 |
| 24h | Son Ye Jin | 1 |
| 24h | Suzuki XL7 | 1 |
| 24h | Tai nghe | 1 |
| 24h | Taylor Swift | 1 |
| 24h | Thành nhà Hồ | 1 |
| 24h | Thượng viện Mỹ | 1 |
| 24h | Thổ Nhĩ Kỳ - Mỹ | 1 |
| 24h | Thủ khoa | 1 |
| 24h | Timothée Chalamet | 1 |
| 24h | Tiểu Long Nữ | 1 |
| 24h | Tiểu Vy | 1 |
| 24h | Toyota Camry | 1 |
| 24h | Toyota Land Cruiser Hybrid | 1 |
| 24h | Triều Tiên | 1 |
| 24h | Trường chuyên | 1 |
| 24h | Trường công lập | 1 |
| 24h | Trại hè | 1 |
| 24h | Tunisia - Hà Lan | 1 |
| 24h | Tô Hữu Bằng | 1 |
| 24h | Tướng Donahue | 1 |
| 24h | Tạ Đình Phong | 1 |
| 24h | Tập đoàn Sơn Hải | 1 |
| 24h | Tổng thống Trump | 1 |
| 24h | Tụ điện | 1 |
| 24h | Tỷ giá USD | 1 |
| 24h | Uruguay - Tây Ban Nha | 1 |
| 24h | VinFast VF 3 | 1 |
| 24h | Viện KSND TP.HCM | 1 |
| 24h | Việt Nam | 1 |
| 24h | Văn Thanh | 1 |
| 24h | Vĩnh Long | 1 |
| 24h | Vương Sở Nhiên | 1 |
| 24h | Vụ ‘bỏ bom’ hóa đơn 16 triệu đồng | 1 |
| 24h | Xe MPV | 1 |
| 24h | Xioban | 1 |
| 24h | Xuân Son | 1 |
| 24h | Yamal | 1 |
| 24h | Zelensky | 1 |
| 24h | bang xep hang bong da | 1 |
| 24h | bang xep hang bong da anh | 1 |
| 24h | biển số giả | 1 |
| 24h | bong chuyen nu | 1 |
| 24h | bong chuyen vo dich dong nam a | 1 |
| 24h | bác tin bão số 3 | 1 |
| 24h | bảng xếp hạng World Cup | 1 |
| 24h | bất tỉnh | 1 |
| 24h | ca sĩ | 1 |
| 24h | chinh phục Everest | 1 |
| 24h | chuyển tiền | 1 |
| 24h | cháy quán cà phê | 1 |
| 24h | chính sách | 1 |
| 24h | clip 1 phút | 1 |
| 24h | clip phút 90+ | 1 |
| 24h | con ac ac wimbledon | 1 |
| 24h | cua hoàng đế | 1 |
| 24h | cách chọn dưa lê | 1 |
| 24h | công viên | 1 |
| 24h | cảnh báo mưa dông | 1 |
| 24h | da mụn | 1 |
| 24h | dancer | 1 |
| 24h | djokovic | 1 |
| 24h | doanh nghiệp ma | 1 |
| 24h | du lịch hội an | 1 |
| 24h | dấu hiệu bệnh thận | 1 |
| 24h | dứa | 1 |
| 24h | em bé | 1 |
| 24h | ghế an toàn | 1 |
| 24h | ghế trẻ em | 1 |
| 24h | giá mắc cọp | 1 |
| 24h | giá vàng giảm | 1 |
| 24h | giá vàng hôm nay | 1 |
| 24h | giá điện | 1 |
| 24h | giáo dục | 1 |
| 24h | giảm cân | 1 |
| 24h | giấy chứng nhận quyền sử dụng đất | 1 |
| 24h | gỡ rối | 1 |
| 24h | hoa don 16 trieu | 1 |
| 24h | honda click 125 | 1 |
| 24h | honda click evo 160 | 1 |
| 24h | hot girl | 1 |
| 24h | hà nội | 1 |
| 24h | hành hung | 1 |
| 24h | học phí khối Y Dược | 1 |
| 24h | học thuyết quân sự iran | 1 |
| 24h | hố đen ngủ đông | 1 |
| 24h | iPhone | 1 |
| 24h | iPhone 18 | 1 |
| 24h | iPhone Ultra | 1 |
| 24h | iPhone cũ | 1 |
| 24h | infographic | 1 |
| 24h | iphone | 1 |
| 24h | lich phat song truc tiep | 1 |
| 24h | lich thi dau bong da hom nay va ngay mai | 1 |
| 24h | lich thi dau ngoai hang anh | 1 |
| 24h | lich thi dau world cup 2026 | 1 |
| 24h | lich truc tiep tennis hom nay | 1 |
| 24h | làn khẩn cấp | 1 |
| 24h | lương giáo viên | 1 |
| 24h | lương hưu | 1 |
| 24h | lớp 10 | 1 |
| 24h | lừa tình | 1 |
| 24h | lừa đảo | 1 |
| 24h | lừa đảo chiếm đoạt tài sản | 1 |
| 24h | mang hung khí điều khiển xe mô tô | 1 |
| 24h | mâm cơm | 1 |
| 24h | mây ngũ sắc | 1 |
| 24h | mã độc WhatsApp | 1 |
| 24h | mưa dông | 1 |
| 24h | mặt nạ | 1 |
| 24h | mặt trời | 1 |
| 24h | nang wags | 1 |
| 24h | người Việt ở nước ngoài | 1 |
| 24h | ngộ độc thực phẩm | 1 |
| 24h | ngủ đủ giấc | 1 |
| 24h | nhà tập thể | 1 |
| 24h | nong ruc khan dai world cup | 1 |
| 24h | nước luộc thịt | 1 |
| 24h | nắng nóng | 1 |
| 24h | nợ lương | 1 |
| 24h | phim kinh dị | 1 |
| 24h | phong cách mùa hè 2026 | 1 |
| 24h | phường Thanh Xuân | 1 |
| 24h | phạt tài xế | 1 |
| 24h | phẫu thuật | 1 |
| 24h | quyền riêng tư | 1 |
| 24h | quầng mặt trời | 1 |
| 24h | redmi k90 ultra | 1 |
| 24h | robot dáng người đá bóng | 1 |
| 24h | rút BHXH một lần | 1 |
| 24h | samsung | 1 |
| 24h | suy thận | 1 |
| 24h | suzuki | 1 |
| 24h | sát hạch lái xe | 1 |
| 24h | sân vận động Akron | 1 |
| 24h | sạc dự phòng | 1 |
| 24h | sổ BHXH | 1 |
| 24h | sử dụng điện thoại | 1 |
| 24h | tennis dinh cao | 1 |
| 24h | thi mô phỏng | 1 |
| 24h | thuế khoán | 1 |
| 24h | thành phố Bắc Ninh | 1 |
| 24h | thác Bản Giốc | 1 |
| 24h | thông minh | 1 |
| 24h | thịt vịt | 1 |
| 24h | thời tiết | 1 |
| 24h | thời tiết Hà Nội | 1 |
| 24h | thời tiết khắc nghiệt | 1 |
| 24h | thủ tục hành chính | 1 |
| 24h | thức đêm | 1 |
| 24h | tim mạch | 1 |
| 24h | tinh hà say hi | 1 |
| 24h | top ghi ban world cup | 1 |
| 24h | trái cây nhập khẩu | 1 |
| 24h | trực tiếp bóng đá | 1 |
| 24h | tuyển sinh đại học | 1 |
| 24h | tàu dầu nga | 1 |
| 24h | tên lửa | 1 |
| 24h | tìm kiếm cứu nạn | 1 |
| 24h | tôm khô | 1 |
| 24h | tăng nặng mức phạt | 1 |
| 24h | tổ dân phố | 1 |
| 24h | tỷ phú | 1 |
| 24h | ung thư dạ dày | 1 |
| 24h | ung thư gan | 1 |
| 24h | viêm cơ tim | 1 |
| 24h | vo gạo trước khi nấu cơm | 1 |
| 24h | vo tien minh | 1 |
| 24h | vé điện tử liên thông | 1 |
| 24h | vô sinh có phải do phụ nữ không | 1 |
| 24h | vật thể | 1 |
| 24h | vợ Duy Mạnh | 1 |
| 24h | xe may | 1 |
| 24h | xe máy kẹp 5 | 1 |
| 24h | xung đột | 1 |
| 24h | xét tuyển đại học | 1 |
| 24h | xăng E10 | 1 |
| 24h | xổ số | 1 |
| 24h | Á hậu Châu Anh đóng MV | 1 |
| 24h | Ông Nawat lo ngại về Miss Universe Vietnam | 1 |
| 24h | ăn trứng sai cách | 1 |
| 24h | ĐT Việt Nam | 1 |
| 24h | ĐT hàn quốc | 1 |
| 24h | Điểm chuẩn | 1 |
| 24h | Điện lực TPHCM | 1 |
| 24h | Đề thi môn Văn | 1 |
| 24h | Đỗ Mỹ Linh sau sinh | 1 |
| 24h | Đội tuyển bóng đá Iran | 1 |
| 24h | Động đất | 1 |
| 24h | Đức thua đau Ecuador | 1 |
| 24h | điều chỉnh giá điện | 1 |
| 24h | điểm chuẩn vào lớp 10 | 1 |
| 24h | đêm tân hôn | 1 |
| 24h | đạo diễn Victor Vũ | 1 |
| 24h | đấu giá | 1 |
| 24h | đầu tư | 1 |
| 24h | đồng tháp | 1 |
| 24h | động đất tại Venezuela | 1 |
| 24h | Ảnh sao | 1 |
| 24h | ốp lưng | 1 |
| baochinhphu | (none) | 46 |
| baochinhphu | Phó Thủ tướng | 7 |
| baochinhphu | Tổng Bí thư | 5 |
| baochinhphu | Vĩnh Long | 5 |
| baochinhphu | Phạm Gia Túc | 4 |
| baochinhphu | Chủ tịch Quốc hội | 3 |
| baochinhphu | hài cốt liệt sĩ | 3 |
| baochinhphu | Cần Thơ | 2 |
| baochinhphu | Hộ kinh doanh | 2 |
| baochinhphu | Nghị quyết 57-NQ/TW | 2 |
| baochinhphu | khoa học | 2 |
| baochinhphu | mộ liệt sĩ | 2 |
| baochinhphu | Đà Nẵng | 2 |
| baochinhphu | ACB | 1 |
| baochinhphu | Agribank | 1 |
| baochinhphu | Báo chí | 1 |
| baochinhphu | Bệnh viện Bạch Mai | 1 |
| baochinhphu | Bộ Khoa học và Công nghệ | 1 |
| baochinhphu | Bộ Nội vụ | 1 |
| baochinhphu | Bộ Tư Pháp | 1 |
| baochinhphu | Chiến lược tài chính | 1 |
| baochinhphu | Cháy rừng | 1 |
| baochinhphu | Chỉ đạo | 1 |
| baochinhphu | Cơ quan điều tra | 1 |
| baochinhphu | Cảnh sát kinh tế | 1 |
| baochinhphu | EVNNPT | 1 |
| baochinhphu | Huế | 1 |
| baochinhphu | Hòn Đá Bạc | 1 |
| baochinhphu | Hùng Nhơn | 1 |
| baochinhphu | Hội thi | 1 |
| baochinhphu | Hội thảo | 1 |
| baochinhphu | KPI trong xây dựng pháp luật | 1 |
| baochinhphu | Kế toán | 1 |
| baochinhphu | Long Châu | 1 |
| baochinhphu | MTTQ | 1 |
| baochinhphu | Nestlé MILO | 1 |
| baochinhphu | Người cao tuổi | 1 |
| baochinhphu | Nhà Quốc hội | 1 |
| baochinhphu | ODA | 1 |
| baochinhphu | One Mount | 1 |
| baochinhphu | PetroVietnam | 1 |
| baochinhphu | Quảng Trị | 1 |
| baochinhphu | Rừng phòng hộ | 1 |
| baochinhphu | Sếu đầu đỏ | 1 |
| baochinhphu | Sở hữu trí tuệ | 1 |
| baochinhphu | Thanh Tra | 1 |
| baochinhphu | Thủ tướng Lê Minh Hưng | 1 |
| baochinhphu | Thủ tục hành chính | 1 |
| baochinhphu | Tây Ninh | 1 |
| baochinhphu | Vinachem | 1 |
| baochinhphu | Vinamilk | 1 |
| baochinhphu | Việt Nam - Hàn Quốc | 1 |
| baochinhphu | Văn phòng Chính phủ | 1 |
| baochinhphu | Văn phòng đại diện | 1 |
| baochinhphu | Xăng dầu | 1 |
| baochinhphu | Xử phạt vi phạm | 1 |
| baochinhphu | Y tế | 1 |
| baochinhphu | an ninh phi truyền thống | 1 |
| baochinhphu | bác sĩ | 1 |
| baochinhphu | bảo hiểm bắt buộc trong xây dựng\ | 1 |
| baochinhphu | bảo tàng mỹ thuật việt nam | 1 |
| baochinhphu | bảo vệ trẻ em | 1 |
| baochinhphu | bệnh dại | 1 |
| baochinhphu | bổ nhiệm Phó Chủ nhiệm Văn phòng Chính phủ | 1 |
| baochinhphu | chip bán dẫn | 1 |
| baochinhphu | chuyển mục đích sử dụng đất | 1 |
| baochinhphu | chuyển đổi số | 1 |
| baochinhphu | cá độ bóng đá | 1 |
| baochinhphu | các bon | 1 |
| baochinhphu | công chức | 1 |
| baochinhphu | công nghệ hiện đại | 1 |
| baochinhphu | cơ sở giáo dục đại học | 1 |
| baochinhphu | dịch vụ công lưu động | 1 |
| baochinhphu | giao thông | 1 |
| baochinhphu | giá xăng | 1 |
| baochinhphu | giấy phép xây dựng | 1 |
| baochinhphu | hoạt động bay | 1 |
| baochinhphu | hưu trí | 1 |
| baochinhphu | hải quan | 1 |
| baochinhphu | khoa học công nghệ | 1 |
| baochinhphu | liên bang nga | 1 |
| baochinhphu | liên kết 4 nhà | 1 |
| baochinhphu | miễn thuế | 1 |
| baochinhphu | mua bán người | 1 |
| baochinhphu | nghỉ việc | 1 |
| baochinhphu | nguồn nhân lực | 1 |
| baochinhphu | người có công | 1 |
| baochinhphu | nhà giáo ưu tú | 1 |
| baochinhphu | nền tảng số dùng chung quốc gia | 1 |
| baochinhphu | nổi bật tuần | 1 |
| baochinhphu | phát triển ngoại thương | 1 |
| baochinhphu | phòng chống rửa tiền | 1 |
| baochinhphu | phó thủ tướng thường trực | 1 |
| baochinhphu | phường | 1 |
| baochinhphu | phụ cấp | 1 |
| baochinhphu | sàng lọc trước sinh và sơ sinh | 1 |
| baochinhphu | thu ngân sách | 1 |
| baochinhphu | thuế sử dụng đất | 1 |
| baochinhphu | thủ tướng | 1 |
| baochinhphu | trường học biên giới | 1 |
| baochinhphu | trạm dừng nghỉ | 1 |
| baochinhphu | tài sản | 1 |
| baochinhphu | tín dụng xanh | 1 |
| baochinhphu | tăng trưởng hai con số | 1 |
| baochinhphu | tỉnh Điện Biên | 1 |
| baochinhphu | vi phạm | 1 |
| baochinhphu | văn bản quy phạm pháp luật | 1 |
| baochinhphu | văn hóa | 1 |
| baochinhphu | văn hóa truyền thống | 1 |
| baochinhphu | vận tải | 1 |
| baochinhphu | vốn tín dụng chính sách | 1 |
| baochinhphu | xúc tiến thương mại | 1 |
| baochinhphu | xăng E10 | 1 |
| baochinhphu | Đoàn Thanh niên Chính phủ | 1 |
| baochinhphu | Đại học Nam Cần Thơ | 1 |
| baochinhphu | Đắk Lắk | 1 |
| baochinhphu | đo lường | 1 |
| baochinhphu | đàm phán | 1 |
| baochinhphu | đăng ký doanh nghiệp | 1 |
| baochinhphu | đường sắt | 1 |
| baochinhphu | đại tướng phan văn giang | 1 |
| baochinhphu | đất ruộng | 1 |
| cafef | trung quốc | 9 |
| cafef | bất động sản | 6 |
| cafef | dự án | 6 |
| cafef | việt nam | 6 |
| cafef | vàng | 6 |
| cafef | lừa đảo | 5 |
| cafef | nga | 5 |
| cafef | ngân hàng | 5 |
| cafef | cổ phiếu | 4 |
| cafef | trái phiếu | 4 |
| cafef | (none) | 3 |
| cafef | AI | 3 |
| cafef | Bắc Ninh | 3 |
| cafef | công an | 3 |
| cafef | giá điện | 3 |
| cafef | hà nội | 3 |
| cafef | BHXh | 2 |
| cafef | Google | 2 |
| cafef | Phạm Nhật Vượng | 2 |
| cafef | Venezuela | 2 |
| cafef | apple | 2 |
| cafef | châu âu | 2 |
| cafef | cơ quan thuế | 2 |
| cafef | gia vị | 2 |
| cafef | hoa hậu | 2 |
| cafef | iran | 2 |
| cafef | lãi suất | 2 |
| cafef | mỹ nhân | 2 |
| cafef | nhnn | 2 |
| cafef | nhà ở xã hội | 2 |
| cafef | nắng nóng | 2 |
| cafef | thi hành lệnh bắt tạm giam | 2 |
| cafef | thuế | 2 |
| cafef | thị trường | 2 |
| cafef | 2 loại nước | 1 |
| cafef | 5 loại cá | 1 |
| cafef | Airwallex | 1 |
| cafef | Apple | 1 |
| cafef | BV Bạch Mai | 1 |
| cafef | Ba Tư | 1 |
| cafef | Bác sĩ ở Bệnh viện Việt Đức | 1 |
| cafef | Bắt Lê Văn Chi SN 1991 | 1 |
| cafef | Bắt giữ Lê Nguyễn Bích Huyền | 1 |
| cafef | Bắt tạm giam Giám đốc | 1 |
| cafef | Bệnh viện | 1 |
| cafef | Bệnh viện Bạch Mai cơ sở 2 | 1 |
| cafef | Bộ Tài chính | 1 |
| cafef | Ca sĩ Mỹ Tâm | 1 |
| cafef | Cristiano Ronaldo | 1 |
| cafef | Cuối tuần này (26-28/6) | 1 |
| cafef | Công an TP Đà Nẵng | 1 |
| cafef | Công an điều tra về số tiền | 1 |
| cafef | DIC Corp | 1 |
| cafef | Dự án quan trọng của Nga | 1 |
| cafef | Galaxy Cruiser 700 | 1 |
| cafef | Gia đình Việt có 8 người con đều là Giáo sư | 1 |
| cafef | Gửi tiết kiệm | 1 |
| cafef | Honda | 1 |
| cafef | Hoài Linh | 1 |
| cafef | Hyundai | 1 |
| cafef | Hàng tồn kho | 1 |
| cafef | Học phí | 1 |
| cafef | Jungle Boss | 1 |
| cafef | Khởi tố | 1 |
| cafef | Liên minh châu Âu | 1 |
| cafef | Lương hưu | 1 |
| cafef | MIE | 1 |
| cafef | Mai Phương Thúy | 1 |
| cafef | Mang 9 | 1 |
| cafef | Messi | 1 |
| cafef | Mitsubishi | 1 |
| cafef | Móng tay | 1 |
| cafef | Mẹ đảm miền Tây | 1 |
| cafef | Mỹ Tâm | 1 |
| cafef | NSND Công Lý | 1 |
| cafef | Nam MC giàu nhất nhì Việt Nam | 1 |
| cafef | Nam sinh | 1 |
| cafef | Nam sinh mê Toán | 1 |
| cafef | Neymar | 1 |
| cafef | Nga | 1 |
| cafef | Ngành ngoại ngữ | 1 |
| cafef | Người đàn ông mua nhà | 1 |
| cafef | Nhà hát kịch Việt Nam | 1 |
| cafef | Nobita | 1 |
| cafef | Nắng nóng cực đoan | 1 |
| cafef | Paris | 1 |
| cafef | Phát hiện 1 chiếc xe | 1 |
| cafef | Phát hiện 30 kg vàng | 1 |
| cafef | Phương Thanh | 1 |
| cafef | Starlink | 1 |
| cafef | Sun PhuQuoc Airways | 1 |
| cafef | Thiếu 0 | 1 |
| cafef | Thuế thu nhập cá nhân | 1 |
| cafef | TikTok Shop | 1 |
| cafef | Tin vui: Từ 1/7 | 1 |
| cafef | Trường THPT | 1 |
| cafef | Trường Đại học Y Dược Hải Phòng | 1 |
| cafef | Trợ lý cảnh sát | 1 |
| cafef | Tài khoản không sử dụng | 1 |
| cafef | Tạm giữ khẩn cấp | 1 |
| cafef | Tổng thống Mỹ Trump | 1 |
| cafef | UBND TP Đà Nẵng | 1 |
| cafef | VietJet | 1 |
| cafef | Vietnam Airlines | 1 |
| cafef | Vietnamobile | 1 |
| cafef | Vinhomes phước vĩnh tây | 1 |
| cafef | Vinspeed | 1 |
| cafef | WinCommerce | 1 |
| cafef | World Cup | 1 |
| cafef | World Cup 2026 | 1 |
| cafef | Zhongji Innolight | 1 |
| cafef | anker | 1 |
| cafef | asus | 1 |
| cafef | bang New Jersey | 1 |
| cafef | bizfly | 1 |
| cafef | bãi biển | 1 |
| cafef | bđs | 1 |
| cafef | bạc | 1 |
| cafef | bảo hiểm nhân thọ | 1 |
| cafef | bệnh viện bạch mai | 1 |
| cafef | chiến binh ung thư | 1 |
| cafef | chuyển khoản | 1 |
| cafef | chứng khoán | 1 |
| cafef | concert | 1 |
| cafef | csgt | 1 |
| cafef | cài đặt phần mềm | 1 |
| cafef | công bố thông tin | 1 |
| cafef | công nghệ | 1 |
| cafef | cổ phiếu ngân hàng | 1 |
| cafef | cổ tức | 1 |
| cafef | cửa trượt nhà bếp | 1 |
| cafef | doanh nghiệp Việt | 1 |
| cafef | donald trump | 1 |
| cafef | dự phòng | 1 |
| cafef | evn | 1 |
| cafef | fpt | 1 |
| cafef | giá vàng | 1 |
| cafef | giá vàng miếng SJC | 1 |
| cafef | giấy tờ | 1 |
| cafef | giới siêu giàu | 1 |
| cafef | giữ vàng suốt 10 năm | 1 |
| cafef | gã khổng lồ thép 58 tấn | 1 |
| cafef | huyền thoại | 1 |
| cafef | hva | 1 |
| cafef | hàn quốc | 1 |
| cafef | hàng không | 1 |
| cafef | hóa đơn 16 triệu đồng | 1 |
| cafef | hưng yên | 1 |
| cafef | hải sản | 1 |
| cafef | hệ thống | 1 |
| cafef | italy | 1 |
| cafef | kbc | 1 |
| cafef | khách hàng | 1 |
| cafef | khám chữa bệnh | 1 |
| cafef | loại quả | 1 |
| cafef | loại rau | 1 |
| cafef | ly hôn | 1 |
| cafef | lương giáo viên | 1 |
| cafef | malaysia | 1 |
| cafef | meta | 1 |
| cafef | miền Tây | 1 |
| cafef | mua nhà | 1 |
| cafef | món bánh | 1 |
| cafef | môn thể thao | 1 |
| cafef | mưa đá | 1 |
| cafef | mệnh Kim | 1 |
| cafef | mỹ đình | 1 |
| cafef | ngành học | 1 |
| cafef | ngân hàng nhà nước | 1 |
| cafef | ngọc trinh | 1 |
| cafef | nhà đầu tư | 1 |
| cafef | nhập viện | 1 |
| cafef | nữ ca sĩ | 1 |
| cafef | phó chủ nhiệm Văn phòng Chính phủ | 1 |
| cafef | phạt | 1 |
| cafef | phạt đến 50 triệu đồng | 1 |
| cafef | pin | 1 |
| cafef | quy định mới | 1 |
| cafef | quốc lộ 13 | 1 |
| cafef | ra mắt | 1 |
| cafef | samsung | 1 |
| cafef | sát hạch lái xe | 1 |
| cafef | sóc trăng | 1 |
| cafef | sống lâu | 1 |
| cafef | sống thọ | 1 |
| cafef | thu hồi đất | 1 |
| cafef | thuê nhà | 1 |
| cafef | thương mại điện tử | 1 |
| cafef | thầy giáo | 1 |
| cafef | thủ khoa | 1 |
| cafef | tiktok | 1 |
| cafef | tiết kiệm điện | 1 |
| cafef | trạm sạc | 1 |
| cafef | trồng lúa | 1 |
| cafef | trợ cấp thai sản | 1 |
| cafef | tuổi 30 | 1 |
| cafef | tài khoản | 1 |
| cafef | tài khoản ngân hàng | 1 |
| cafef | tái định cư | 1 |
| cafef | tôm hùm | 1 |
| cafef | tất cả người dân | 1 |
| cafef | tập đoàn Sơn Hải | 1 |
| cafef | uống 13 lít nước | 1 |
| cafef | vietinbank | 1 |
| cafef | vinasoy | 1 |
| cafef | vingroup | 1 |
| cafef | vinhomes | 1 |
| cafef | vnsteel | 1 |
| cafef | vải thiều | 1 |
| cafef | vận tải biển | 1 |
| cafef | wimbledon | 1 |
| cafef | xe buýt | 1 |
| cafef | xe máy | 1 |
| cafef | xem TV | 1 |
| cafef | xăng dầu | 1 |
| cafef | xới cơm | 1 |
| cafef | ô nhiễm nguồn nước | 1 |
| cafef | Đóng BHXH | 1 |
| cafef | Đông Nam Á | 1 |
| cafef | Đại học Bách khoa Hà Nội | 1 |
| cafef | đen vâu | 1 |
| cafef | đhcđ | 1 |
| cafef | điện thoại đang bị theo dõi | 1 |
| cafef | đường Lê Lợi | 1 |
| cafef | đường dây lừa đảo xuyên quốc gia | 1 |
| cafef | đại học | 1 |
| cafef | đất nông nghiệp | 1 |
| cafef | đất đai | 1 |
| cafef | đổ xăng | 1 |
| dantri | Thời sự | 59 |
| dantri | Kinh doanh | 46 |
| dantri | Thế giới | 43 |
| dantri | Pháp luật | 39 |
| dantri | Thể thao | 37 |
| dantri | Nội vụ | 26 |
| dantri | Sức khỏe | 25 |
| dantri | Đời sống | 21 |
| dantri | Giáo dục | 20 |
| dantri | Bất động sản | 19 |
| dantri | Giải trí | 19 |
| dantri | (none) | 16 |
| dantri | Công nghệ | 14 |
| dantri | Ô tô - Xe máy | 11 |
| dantri | Du lịch | 8 |
| dantri | Khoa học | 6 |
| dantri | Lao động - Việc làm | 5 |
| dantri | Tấm lòng nhân ái | 5 |
| dantri | Bạn đọc | 3 |
| dantri | Tâm điểm | 3 |
| dantri | Thời tiết | 1 |
| dantri | Tình yêu - Giới tính | 1 |
| kenh14 | (none) | 21 |
| kenh14 | World Cup 2026 | 15 |
| kenh14 | đời sống | 10 |
| kenh14 | thể thao | 9 |
| kenh14 | giải trí | 7 |
| kenh14 | nắng nóng | 7 |
| kenh14 | ronaldo | 6 |
| kenh14 | Kpop | 4 |
| kenh14 | World Cup | 4 |
| kenh14 | giá vàng hôm nay | 4 |
| kenh14 | Z-School Tour | 3 |
| kenh14 | dân văn phòng | 3 |
| kenh14 | Ca sĩ Việt | 2 |
| kenh14 | Mỹ Tâm | 2 |
| kenh14 | bạo hành | 2 |
| kenh14 | bắt giữ | 2 |
| kenh14 | chuyển khoản | 2 |
| kenh14 | dạy con | 2 |
| kenh14 | giảm cân | 2 |
| kenh14 | hóa đơn | 2 |
| kenh14 | messi | 2 |
| kenh14 | phim trung quốc | 2 |
| kenh14 | phạt nguội | 2 |
| kenh14 | quy định | 2 |
| kenh14 | suy thận | 2 |
| kenh14 | tranh cãi | 2 |
| kenh14 | tuyển anh | 2 |
| kenh14 | điện thoại | 2 |
| kenh14 | 14 triệu người dân ở TP.HCM nhận tin vui | 1 |
| kenh14 | Agent Kim Reactivated | 1 |
| kenh14 | Angelababy | 1 |
| kenh14 | BHYT | 1 |
| kenh14 | Beckham | 1 |
| kenh14 | Bác sĩ Bạch Mai cảnh báo | 1 |
| kenh14 | Bảo Anh | 1 |
| kenh14 | Bắc Ninh | 1 |
| kenh14 | Cháy quán cà phê | 1 |
| kenh14 | City Guide | 1 |
| kenh14 | Công an | 1 |
| kenh14 | Dương tử | 1 |
| kenh14 | Elon Musk | 1 |
| kenh14 | Facebook | 1 |
| kenh14 | Gan tổn thương | 1 |
| kenh14 | Google | 1 |
| kenh14 | Hong Seok Jun | 1 |
| kenh14 | House n Home | 1 |
| kenh14 | Hà Nội | 1 |
| kenh14 | Hàn Quốc | 1 |
| kenh14 | Học phí | 1 |
| kenh14 | Hội An | 1 |
| kenh14 | Jayna Angelina Stevens | 1 |
| kenh14 | Khám xét | 1 |
| kenh14 | Lavie | 1 |
| kenh14 | Long Châu | 1 |
| kenh14 | Louis Vuitton | 1 |
| kenh14 | Luộc thịt | 1 |
| kenh14 | Lý Kim Minh | 1 |
| kenh14 | Lương Thế Thành | 1 |
| kenh14 | MC Đại Nghĩa | 1 |
| kenh14 | Michelin guide | 1 |
| kenh14 | Mua nhà | 1 |
| kenh14 | Máy bay | 1 |
| kenh14 | Mặt trời | 1 |
| kenh14 | NSƯT Ngọc Quỳnh | 1 |
| kenh14 | Nhật Bản | 1 |
| kenh14 | Nắng nóng | 1 |
| kenh14 | Pháo | 1 |
| kenh14 | Pháp | 1 |
| kenh14 | Phạm Quỳnh Anh | 1 |
| kenh14 | Phế cầu khuẩn | 1 |
| kenh14 | Psi Scott | 1 |
| kenh14 | Pun | 1 |
| kenh14 | Rosé | 1 |
| kenh14 | Song hye kyo | 1 |
| kenh14 | Starbucks | 1 |
| kenh14 | Sóng nhiệt | 1 |
| kenh14 | Sỏi bàng quang | 1 |
| kenh14 | TP.HCM | 1 |
| kenh14 | Thi thể thiếu nữ | 1 |
| kenh14 | Thi vào lớp 10 | 1 |
| kenh14 | Thu Trang | 1 |
| kenh14 | Thảo Cầm Viên Sài Gòn | 1 |
| kenh14 | Tlinh | 1 |
| kenh14 | Tóc Tiên | 1 |
| kenh14 | Ung thư | 1 |
| kenh14 | Vinamilk | 1 |
| kenh14 | Võ Hà Linh | 1 |
| kenh14 | Vĩnh Thuỵ | 1 |
| kenh14 | Vũ Thuý Quỳnh | 1 |
| kenh14 | Xét xử | 1 |
| kenh14 | Yeah1 | 1 |
| kenh14 | Yoon Doo Joon | 1 |
| kenh14 | Zalo | 1 |
| kenh14 | bellingham | 1 |
| kenh14 | bài học cuộc sống | 1 |
| kenh14 | bài học tài chính | 1 |
| kenh14 | bão | 1 |
| kenh14 | bảo hiểm | 1 |
| kenh14 | bảo ngọc | 1 |
| kenh14 | bằng lái xe | 1 |
| kenh14 | bộ xương người | 1 |
| kenh14 | chuyển khoản nhầm | 1 |
| kenh14 | chân gà đông lạnh | 1 |
| kenh14 | chạy bộ | 1 |
| kenh14 | chất gây ung thư | 1 |
| kenh14 | collagen | 1 |
| kenh14 | croatia | 1 |
| kenh14 | có như lời đồn | 1 |
| kenh14 | công an | 1 |
| kenh14 | căn nhà | 1 |
| kenh14 | cơ quan thuế | 1 |
| kenh14 | cảnh báo | 1 |
| kenh14 | cắt điện | 1 |
| kenh14 | cứu người | 1 |
| kenh14 | giá bạc | 1 |
| kenh14 | giá vàng | 1 |
| kenh14 | giấy tờ | 1 |
| kenh14 | graff | 1 |
| kenh14 | gửi tiết kiệm | 1 |
| kenh14 | han ga in | 1 |
| kenh14 | hoàng thùy linh | 1 |
| kenh14 | hành hung thai phụ | 1 |
| kenh14 | hạ cánh | 1 |
| kenh14 | hộ dân | 1 |
| kenh14 | iPhone 18 Pro Max | 1 |
| kenh14 | iPhone cũ | 1 |
| kenh14 | khách sạn | 1 |
| kenh14 | khói mù | 1 |
| kenh14 | kiếm tiền | 1 |
| kenh14 | lisa | 1 |
| kenh14 | lyly | 1 |
| kenh14 | lãi suất ngân hàng | 1 |
| kenh14 | lịch sử | 1 |
| kenh14 | lớp 10 | 1 |
| kenh14 | miền bắc nắng nóng | 1 |
| kenh14 | mua xe máy | 1 |
| kenh14 | mưa dông | 1 |
| kenh14 | mưa lũ ở cao bằng | 1 |
| kenh14 | mộ | 1 |
| kenh14 | mộc châu | 1 |
| kenh14 | mỹ nhân | 1 |
| kenh14 | ngân 98 | 1 |
| kenh14 | ngư dân | 1 |
| kenh14 | ngọc trinh | 1 |
| kenh14 | ngừng tim khi chơi thể thao | 1 |
| kenh14 | nhiễm HIV | 1 |
| kenh14 | nhà cháy | 1 |
| kenh14 | nhà mới | 1 |
| kenh14 | nạp tiền | 1 |
| kenh14 | nắng nóng gay gắt ở Pháp | 1 |
| kenh14 | nội tiết tố nữ | 1 |
| kenh14 | paris | 1 |
| kenh14 | phim chiếu rạp | 1 |
| kenh14 | phim ngôn tình | 1 |
| kenh14 | phát hiện bộ xương | 1 |
| kenh14 | phạm băng băng | 1 |
| kenh14 | song hye kyo | 1 |
| kenh14 | sông Bằng Giang | 1 |
| kenh14 | sạc dự phòng | 1 |
| kenh14 | sạc không dây | 1 |
| kenh14 | sống thọ | 1 |
| kenh14 | sử dụng ma tuý | 1 |
| kenh14 | teen viet nam | 1 |
| kenh14 | thai sản | 1 |
| kenh14 | thi thể chị em ruột | 1 |
| kenh14 | thiếu nữ bỏ nhà đi | 1 |
| kenh14 | thu trang | 1 |
| kenh14 | thành công | 1 |
| kenh14 | thái bình niên | 1 |
| kenh14 | thịt lợn | 1 |
| kenh14 | thời tiết | 1 |
| kenh14 | tin tức | 1 |
| kenh14 | tiếng Việt | 1 |
| kenh14 | trang trại | 1 |
| kenh14 | trái cây | 1 |
| kenh14 | tránh nắng | 1 |
| kenh14 | trần triết viễn | 1 |
| kenh14 | trợ cấp hưu trí | 1 |
| kenh14 | tôm khô | 1 |
| kenh14 | tôm khô Cà Mau | 1 |
| kenh14 | tăng lương cơ sở | 1 |
| kenh14 | tạm giam | 1 |
| kenh14 | tắm lâu | 1 |
| kenh14 | tắm đá lạnh | 1 |
| kenh14 | tử vong | 1 |
| kenh14 | tử vong ở hồ bơi | 1 |
| kenh14 | ung thư | 1 |
| kenh14 | va chạm | 1 |
| kenh14 | vàng | 1 |
| kenh14 | vỡ hoàng thể | 1 |
| kenh14 | ông Phạm Nhật Vượng | 1 |
| kenh14 | Đoàn tàu Bạch Mai | 1 |
| kenh14 | Đường sắt mở Đoàn tàu Bạch Mai | 1 |
| kenh14 | Đặng Triệu Tôn | 1 |
| kenh14 | đinh lăng | 1 |
| kenh14 | điều hòa | 1 |
| kenh14 | đoàn tàu Bạch Mai | 1 |
| kenh14 | đập gương | 1 |
| kenh14 | đậu xe | 1 |
| kenh14 | đền bù | 1 |
| kenh14 | động đất | 1 |
| kenh14 | ứng dụng | 1 |
| nhandan | Kinh tế | 59 |
| nhandan | Chính trị | 54 |
| nhandan | Xã hội | 52 |
| nhandan | Tin chung | 49 |
| nhandan | Thể thao | 43 |
| nhandan | Văn hóa | 30 |
| nhandan | Đồng bằng sông Hồng | 29 |
| nhandan | Môi trường | 23 |
| nhandan | Châu Âu | 19 |
| nhandan | Duyên hải Nam Trung Bộ và Tây Nguyên | 18 |
| nhandan | Khoa học - Công nghệ | 16 |
| nhandan | Y tế | 16 |
| nhandan | Chuyên trang Hà Nội | 14 |
| nhandan | Thế giới | 11 |
| nhandan | Ảnh | 8 |
| nhandan | (none) | 7 |
| nhandan | Pháp luật | 7 |
| nhandan | Châu Mỹ | 6 |
| nhandan | Giáo dục | 6 |
| nhandan | NHÂN DÂN CUỐI TUẦN | 6 |
| nhandan | Châu Á-TBD | 5 |
| nhandan | Văn hóa - Văn nghệ | 5 |
| nhandan | Du lịch | 4 |
| nhandan | Trung Đông | 4 |
| nhandan | Bạn cần biết | 3 |
| nhandan | Chuyên trang TP. Hồ Chí Minh | 3 |
| nhandan | Châu Phi | 3 |
| nhandan | Thời Nay | 3 |
| nhandan | Bình luận quốc tế | 2 |
| nhandan | Bạn đọc | 2 |
| nhandan | Theo dòng sự kiện | 2 |
| nhandan | World Cup 2026 | 2 |
| nhandan | Xây dựng Đảng | 2 |
| nhandan | Báo chí cách mạng Việt Nam | 1 |
| nhandan | Bản sắc đại ngàn | 1 |
| nhandan | Chuyển đổi số | 1 |
| nhandan | Hành động và thách thức | 1 |
| nhandan | Infographic | 1 |
| nhandan | Mô hình tốt – việc làm hay | 1 |
| nhandan | NHÂN DÂN HẰNG THÁNG | 1 |
| nhandan | Thông tin doanh nghiệp | 1 |
| nhandan | Tiêu điểm | 1 |
| nhandan | Văn hóa làng quê | 1 |
| nhandan | Xây dựng nông thôn mới | 1 |
| nhandan | Đồng bằng sông Cửu Long | 1 |
| qdnd | World Cup | 18 |
| qdnd | World Cup 2026 | 11 |
| qdnd | Tổng Bí thư | 6 |
| qdnd | Cảnh sát biển | 5 |
| qdnd | Ronaldo | 5 |
| qdnd | Messi | 4 |
| qdnd | Mỹ | 4 |
| qdnd | Cao Bằng | 3 |
| qdnd | Quân khu 2 | 3 |
| qdnd | Quân khu 4 | 3 |
| qdnd | Quân đoàn 34 | 3 |
| qdnd | TP Hồ Chí Minh | 3 |
| qdnd | Tin thể thao | 3 |
| qdnd | bộ đội biên phòng | 3 |
| qdnd | chính quyền địa phương hai cấp | 3 |
| qdnd | eo biển Hormuz | 3 |
| qdnd | giá dầu | 3 |
| qdnd | giá vàng hôm nay | 3 |
| qdnd | ma túy | 3 |
| qdnd | từ trần | 3 |
| qdnd | tỷ giá USD | 3 |
| qdnd | Đoàn TNCS Hồ Chí Minh | 3 |
| qdnd | Đắk Lắk | 3 |
| qdnd | động đất | 3 |
| qdnd | (none) | 2 |
| qdnd | An Giang | 2 |
| qdnd | Argentina | 2 |
| qdnd | Báo cáo viên | 2 |
| qdnd | Campuchia | 2 |
| qdnd | Giá vàng | 2 |
| qdnd | Hà Nội | 2 |
| qdnd | Học viện Quân y | 2 |
| qdnd | Iran | 2 |
| qdnd | Israel | 2 |
| qdnd | Khánh Hòa | 2 |
| qdnd | Lào | 2 |
| qdnd | Lào Cai | 2 |
| qdnd | Neymar | 2 |
| qdnd | Nga | 2 |
| qdnd | Quân khu 5 | 2 |
| qdnd | Thủ tướng | 2 |
| qdnd | Trung Quốc | 2 |
| qdnd | Venezuela | 2 |
| qdnd | châu Âu | 2 |
| qdnd | giá cà phê | 2 |
| qdnd | hài cốt liệt sĩ | 2 |
| qdnd | liệt sĩ | 2 |
| qdnd | nhà ở | 2 |
| qdnd | thời tiết hôm nay | 2 |
| qdnd | Đồng Nai | 2 |
| qdnd | đội tuyển Việt Nam | 2 |
| qdnd | AIDS | 1 |
| qdnd | ASEAN | 1 |
| qdnd | Belarus | 1 |
| qdnd | Binh chủng Công binh | 1 |
| qdnd | Binh đoàn 15 | 1 |
| qdnd | Binh đoàn 16 | 1 |
| qdnd | Biên phòng Cửa khẩu Săm Pun | 1 |
| qdnd | Bosnia và Qatar | 1 |
| qdnd | Bác Hồ | 1 |
| qdnd | Bạch Mai | 1 |
| qdnd | Bảng xếp hạng | 1 |
| qdnd | Bảng xếp hạng World Cup | 1 |
| qdnd | Bảng xếp hạng World Cup 2026 hôm nay | 1 |
| qdnd | Bảo hiểm | 1 |
| qdnd | Bảo tàng Phụ nữ Việt Nam | 1 |
| qdnd | Bắc Ninh | 1 |
| qdnd | Bệnh viện Bạch Mai | 1 |
| qdnd | Bệnh viện Quân y 103 | 1 |
| qdnd | Bệnh viện Quân y 175 | 1 |
| qdnd | Bệnh viện Quân y 87 | 1 |
| qdnd | Bệnh viện đa khoa Hòe Nhai | 1 |
| qdnd | Bộ CHQS TP Huế | 1 |
| qdnd | Bộ Tổng tham mưu | 1 |
| qdnd | Bộ tư lệnh 86 | 1 |
| qdnd | Bộ đội Biên phòng TP Huế | 1 |
| qdnd | Bộ đội Biên phòng TP Hải Phòng | 1 |
| qdnd | CPTPP | 1 |
| qdnd | Chiếc giày vàng | 1 |
| qdnd | Chiến dịch 500 ngày đêm | 1 |
| qdnd | Chuẩn úy Palina Dalasin | 1 |
| qdnd | Chính phủ | 1 |
| qdnd | Chính trường Anh | 1 |
| qdnd | Chứng khoán | 1 |
| qdnd | Croatia và Ghana | 1 |
| qdnd | Curacao và Bờ Biển Ngà | 1 |
| qdnd | Công an TP Hà Nội | 1 |
| qdnd | Công tác dân vận | 1 |
| qdnd | Cúc Phương | 1 |
| qdnd | Cần Thơ | 1 |
| qdnd | Cầu thủ châu Á | 1 |
| qdnd | Cục Quân khí | 1 |
| qdnd | Dembele | 1 |
| qdnd | Donald Trump | 1 |
| qdnd | Ecuador và Đức | 1 |
| qdnd | Gia đình quân nhân | 1 |
| qdnd | Giá hồ tiêu | 1 |
| qdnd | HDBank | 1 |
| qdnd | Haaland | 1 |
| qdnd | Hiệp định Abraham | 1 |
| qdnd | Huế | 1 |
| qdnd | Hy Lạp | 1 |
| qdnd | Hà La | 1 |
| qdnd | Hà Tĩnh | 1 |
| qdnd | Hàn Quốc | 1 |
| qdnd | Hè về | 1 |
| qdnd | Hải đoàn Biên phòng 18 | 1 |
| qdnd | Hải đội 202 | 1 |
| qdnd | Học viện Hậu cần | 1 |
| qdnd | Học viện Kỹ thuật Quân sự | 1 |
| qdnd | Học viện Phòng không | 1 |
| qdnd | Học viện Quốc phòng | 1 |
| qdnd | Hồ Chí Minh | 1 |
| qdnd | IAEA | 1 |
| qdnd | IMO | 1 |
| qdnd | Iraq | 1 |
| qdnd | Iraq và Senegal | 1 |
| qdnd | Kim Jong Un | 1 |
| qdnd | Kết luận của Tổng bí thư | 1 |
| qdnd | LLVT tỉnh Quảng Ninh | 1 |
| qdnd | La Văn Cầu | 1 |
| qdnd | Lai Châu | 1 |
| qdnd | Laura | 1 |
| qdnd | Link xem trực tiếp Ai Cập và Iran | 1 |
| qdnd | Link xem trực tiếp Bồ Đào Nha | 1 |
| qdnd | Link xem trực tiếp Colombia và Cộng hòa dân chủ Congo | 1 |
| qdnd | Link xem trực tiếp New Zealand và Bỉ | 1 |
| qdnd | Link xem trực tiếp Panama và Croatia | 1 |
| qdnd | Link xem trực tiếp Thổ Nhĩ Kỳ và Mỹ | 1 |
| qdnd | Lịch thi đấu | 1 |
| qdnd | Lịch thi đấu World Cup 2026 hôm nay | 1 |
| qdnd | Lữ đoàn 162 | 1 |
| qdnd | Lữ đoàn 596 | 1 |
| qdnd | MB | 1 |
| qdnd | Mbappe | 1 |
| qdnd | Merlin | 1 |
| qdnd | Mexico City | 1 |
| qdnd | Mộc bản triều Nguyễn | 1 |
| qdnd | New Zealand | 1 |
| qdnd | Nghệ An | 1 |
| qdnd | Nguyễn Công Trí | 1 |
| qdnd | Nguyễn Sĩ Dũng | 1 |
| qdnd | Nhà máy Z115 | 1 |
| qdnd | Nhà máy Z121 | 1 |
| qdnd | Nhận định Scotland và Brazil | 1 |
| qdnd | Nigeria | 1 |
| qdnd | Pháp và Na Uy | 1 |
| qdnd | Phó chủ tịch nước Võ Thị Ánh Xuân | 1 |
| qdnd | Phật giáo Hòa Hảo | 1 |
| qdnd | Phủ Thông | 1 |
| qdnd | Quân khu 1 | 1 |
| qdnd | Quân khu 3 | 1 |
| qdnd | Quân khu 9 | 1 |
| qdnd | Quân đoàn 12 | 1 |
| qdnd | Quân ủy Trung ương | 1 |
| qdnd | Quảng Ninh | 1 |
| qdnd | Quốc phòng | 1 |
| qdnd | Rudi Garcia | 1 |
| qdnd | Sarr | 1 |
| qdnd | SeABank | 1 |
| qdnd | Sư đoàn 375 | 1 |
| qdnd | Sư đoàn 377 | 1 |
| qdnd | Thanh Hóa | 1 |
| qdnd | Thổ Nhĩ Kỳ | 1 |
| qdnd | Thời tiết | 1 |
| qdnd | Thủ tướng Anh | 1 |
| qdnd | Thủy thủ | 1 |
| qdnd | Tiểu đoàn 703 | 1 |
| qdnd | Trung tá QNCN Đinh Thị Hà | 1 |
| qdnd | Trung đoàn 102 | 1 |
| qdnd | Trung đoàn 754 | 1 |
| qdnd | Trung đoàn 88 | 1 |
| qdnd | Trí thức trẻ | 1 |
| qdnd | Trường Sa | 1 |
| qdnd | Trường Sĩ quan Chính trị | 1 |
| qdnd | Trần Phi Hổ | 1 |
| qdnd | Tuyển Anh | 1 |
| qdnd | Tàu Cảnh sát biển | 1 |
| qdnd | Tân cảng | 1 |
| qdnd | Tô Văn Đực | 1 |
| qdnd | Tùy viên Quân sự | 1 |
| qdnd | Tổng thống Mỹ | 1 |
| qdnd | Tự chủ đại học | 1 |
| qdnd | UN Women | 1 |
| qdnd | UNICEF | 1 |
| qdnd | Ukraine | 1 |
| qdnd | Uruguay | 1 |
| qdnd | VPBank | 1 |
| qdnd | Video bàn thắng Ai Cập và Iran | 1 |
| qdnd | Video bàn thắng BỈ và New Zealand | 1 |
| qdnd | Video bàn thắng Colombia và CHDC Congo | 1 |
| qdnd | Video bàn thắng Croatia và Panama | 1 |
| qdnd | Video bàn thắng Nhật Bản và Thụy Điển | 1 |
| qdnd | Video bàn thắng Tunisia và Hà Lan | 1 |
| qdnd | Video bàn thắng Tây Ban Nha và Uruguay | 1 |
| qdnd | Video trận đấu Anh và Ghana | 1 |
| qdnd | Video trận đấu Cape Verde và Saudi Arabia | 1 |
| qdnd | Viện Khoa học và Công nghệ quân sự | 1 |
| qdnd | Vòm Vàng | 1 |
| qdnd | Vùng 3 Hải quân | 1 |
| qdnd | Vùng Cảnh sát biển 2 | 1 |
| qdnd | Vùng Cảnh sát biển 4 | 1 |
| qdnd | Văn phòng Chính phủ | 1 |
| qdnd | Vị Xuyên | 1 |
| qdnd | Xe máy | 1 |
| qdnd | bóng đá | 1 |
| qdnd | bữa cơm | 1 |
| qdnd | chip bán dẫn | 1 |
| qdnd | chiến dịch 500 ngày đêm | 1 |
| qdnd | chiến tranh | 1 |
| qdnd | chính quyền | 1 |
| qdnd | chăn nuôi | 1 |
| qdnd | chất độc da cam | 1 |
| qdnd | chế biến | 1 |
| qdnd | cộng tác viên | 1 |
| qdnd | diễn biến hòa bình | 1 |
| qdnd | diễn tập | 1 |
| qdnd | dữ liệu | 1 |
| qdnd | gout | 1 |
| qdnd | gìn giữ hòa bình | 1 |
| qdnd | hàng không Mỹ | 1 |
| qdnd | kinh tế tập thể | 1 |
| qdnd | kỹ năng nghề | 1 |
| qdnd | link xem trực tiếp Nhật Bản | 1 |
| qdnd | luật | 1 |
| qdnd | lương hưu | 1 |
| qdnd | lịch sử | 1 |
| qdnd | lịch thi đấu World Cup | 1 |
| qdnd | mùa hạ | 1 |
| qdnd | mạng xã hội | 1 |
| qdnd | mẫu sinh phẩm ADN | 1 |
| qdnd | mẹ Việt Nam Anh hùng | 1 |
| qdnd | nghiệp vụ công tác văn phòng | 1 |
| qdnd | nghề ướp trà sen | 1 |
| qdnd | nghỉ uống nước | 1 |
| qdnd | ngành xuất bản | 1 |
| qdnd | ngư dân | 1 |
| qdnd | người cao tuổi | 1 |
| qdnd | nhiếp ảnh | 1 |
| qdnd | nhà giàn | 1 |
| qdnd | nông sản | 1 |
| qdnd | năng lượng | 1 |
| qdnd | phòng chống cháy rừng | 1 |
| qdnd | phương tiện bay không người lái | 1 |
| qdnd | phường Tây Hồ | 1 |
| qdnd | phụ nữ | 1 |
| qdnd | quân sự | 1 |
| qdnd | robot AI | 1 |
| qdnd | sát hạch lái xe | 1 |
| qdnd | thuế dịch vụ số | 1 |
| qdnd | tin tổng hợp | 1 |
| qdnd | trường Đại học Thủ Dầu Một | 1 |
| qdnd | trực tiếp Curacao và Bờ Biển Ngà | 1 |
| qdnd | trực tiếp Ecuador và Đức | 1 |
| qdnd | trực tiếp Paraguay và Australia | 1 |
| qdnd | trực tiếp Tunisia và Hà Lan | 1 |
| qdnd | tài xế công nghệ | 1 |
| qdnd | tên lửa đánh chặn | 1 |
| qdnd | tỉnh Gia Lai | 1 |
| qdnd | tỉnh Điện Biên | 1 |
| qdnd | video bàn thắng | 1 |
| qdnd | video bàn thắng Bồ Đào Nha | 1 |
| qdnd | vì hòa bình | 1 |
| qdnd | vòng 32 đội World Cup | 1 |
| qdnd | văn chương | 1 |
| qdnd | vũ trang | 1 |
| qdnd | xe hợp đồng | 1 |
| qdnd | xe mô tô | 1 |
| qdnd | xuất bản | 1 |
| qdnd | xác nhận nhập học | 1 |
| qdnd | Âm nhạc | 1 |
| qdnd | Điện Biên | 1 |
| qdnd | Đoàn Kinh tế | 1 |
| qdnd | Đoàn Văn công Quân đội nhân dân Lào | 1 |
| qdnd | Đại hội | 1 |
| qdnd | Đại tá VĂN MẠNH SOÁI | 1 |
| qdnd | Đại tướng Phan Văn Giang | 1 |
| qdnd | Đất đai | 1 |
| qdnd | Đặng Tố Quyên | 1 |
| qdnd | đuối nước | 1 |
| qdnd | đại học | 1 |
| qdnd | đội tuyển Anh | 1 |
| qdnd | đội tuyển Đức | 1 |
| saostar | Phim ảnh | 126 |
| saostar | Sao | 68 |
| saostar | Âm nhạc | 48 |
| saostar | Sao Sport | 45 |
| saostar | Vòng quanh thế giới | 29 |
| saostar | Người mẫu - Hoa hậu | 22 |
| saostar | Cận cảnh cuộc sống | 20 |
| saostar | Du lịch - Khám phá | 16 |
| saostar | BĐS - Tài chính | 7 |
| saostar | Fashion - Beauty | 7 |
| saostar | Công nghệ | 6 |
| saostar | Ăn - Chơi | 4 |
| saostar | Học đường | 3 |
| saostar | Sức khỏe | 1 |
| soha | (none) | 74 |
| soha | World Cup | 21 |
| soha | sao Việt | 15 |
| soha | Trung Quốc | 9 |
| soha | báo công an | 5 |
| soha | Mỹ | 3 |
| soha | Lục Thị Hồng Liên | 2 |
| soha | Nga | 2 |
| soha | Tin nóng trong ngày | 2 |
| soha | Ukraine | 2 |
| soha | an ninh thế giới | 2 |
| soha | bánh ram ít | 2 |
| soha | châu âu | 2 |
| soha | con giáp | 2 |
| soha | công an TP Hà Nội | 2 |
| soha | giá vàng | 2 |
| soha | quảng ninh | 2 |
| soha | sao hàn | 2 |
| soha | tai nạn giao thông | 2 |
| soha | ô tô | 2 |
| soha | 5g | 1 |
| soha | BHXH | 1 |
| soha | Bitcoin | 1 |
| soha | Brazil | 1 |
| soha | Báo Người Lao Động | 1 |
| soha | Bạch Mai | 1 |
| soha | Bệnh viện Bạch Mai | 1 |
| soha | Bộ xương | 1 |
| soha | Bữa ăn | 1 |
| soha | Canada | 1 |
| soha | Claude Mythos | 1 |
| soha | Công an cảnh báo | 1 |
| soha | Công an tỉnh Cà Mau | 1 |
| soha | David Vander Meer | 1 |
| soha | EVN | 1 |
| soha | Facebook nghe lén | 1 |
| soha | HIV | 1 |
| soha | Hyundai | 1 |
| soha | Hành chính công | 1 |
| soha | IAEA | 1 |
| soha | IBM | 1 |
| soha | Iraq | 1 |
| soha | Israel tự sản xuất vũ khí | 1 |
| soha | Jaehyun | 1 |
| soha | Không quân Triều Tiên | 1 |
| soha | Kim Jong-un | 1 |
| soha | Kiều Tiên | 1 |
| soha | Lisa | 1 |
| soha | Lê Thị Hồng Nhung | 1 |
| soha | Mark Zuckerberg | 1 |
| soha | Mùa nào bệnh nấy | 1 |
| soha | Nguyễn Đình Lâm | 1 |
| soha | Nhật Bản | 1 |
| soha | Phú Quốc | 1 |
| soha | Ronaldo | 1 |
| soha | Sinh vật | 1 |
| soha | Soha Special | 1 |
| soha | Su-57 | 1 |
| soha | Suzuki | 1 |
| soha | Tin ngắn | 1 |
| soha | Tiểu Vy | 1 |
| soha | Toyota | 1 |
| soha | Trần Anh Tiến | 1 |
| soha | UAV | 1 |
| soha | UAV đánh chặn | 1 |
| soha | VINFAST | 1 |
| soha | Việt Nam | 1 |
| soha | Võ Thị Hằng | 1 |
| soha | Vũ Thúy Quỳnh | 1 |
| soha | ai | 1 |
| soha | australia | 1 |
| soha | biên bản ghi nhớ Mỹ-Iran | 1 |
| soha | biển lý sơn | 1 |
| soha | biệt thự thông minh | 1 |
| soha | bán dâm tại Quảng Đông | 1 |
| soha | bão Nhật Bản | 1 |
| soha | bỉ | 1 |
| soha | bỏng nặng | 1 |
| soha | bộ công an | 1 |
| soha | cháy rừng | 1 |
| soha | cách luộc thịt | 1 |
| soha | cây | 1 |
| soha | căn cứ quân sự | 1 |
| soha | cảnh báo lừa đảo EVN | 1 |
| soha | cờ bạc trực tuyến | 1 |
| soha | du học sinh Việt Nam | 1 |
| soha | du khách | 1 |
| soha | dưỡng lão | 1 |
| soha | dịch vụ may đo Hội An | 1 |
| soha | dọn dẹp | 1 |
| soha | em chồng | 1 |
| soha | giá vàng giảm | 1 |
| soha | giá điện | 1 |
| soha | haaland | 1 |
| soha | hang động Bắc Na Uy | 1 |
| soha | huỳnh thánh y | 1 |
| soha | hà nội | 1 |
| soha | iran | 1 |
| soha | khách Tây | 1 |
| soha | khách sạn | 1 |
| soha | làm mát | 1 |
| soha | làm sạch dép Crocs | 1 |
| soha | làm vườn | 1 |
| soha | lương hưu 2026 | 1 |
| soha | lớp 10 | 1 |
| soha | máy bay | 1 |
| soha | máy bay không người lái | 1 |
| soha | mùa hè tử thần | 1 |
| soha | mưa Hà Nội | 1 |
| soha | mệnh Kim tháng 7 | 1 |
| soha | mừng cưới | 1 |
| soha | nhà máy địa nhiệt | 1 |
| soha | nhật bản | 1 |
| soha | nắng nóng ở Paris | 1 |
| soha | phun thuốc diệt cỏ | 1 |
| soha | phúc khảo điểm thi lớp 10 | 1 |
| soha | phường Hoành Sơn | 1 |
| soha | quy định kiểm tra thuế | 1 |
| soha | quy định mới giấy phép lái xe | 1 |
| soha | quán cà phê cháy TPHCM | 1 |
| soha | quốc gia | 1 |
| soha | quỳnh kool | 1 |
| soha | rapper | 1 |
| soha | rắn trong nhà | 1 |
| soha | shipper | 1 |
| soha | thay đổi giấy phép lái xe | 1 |
| soha | thu nhập chịu thuế | 1 |
| soha | thú vui tìm hiểu bất động sản | 1 |
| soha | thẻ vé giao thông | 1 |
| soha | thủ phạm | 1 |
| soha | tin giả | 1 |
| soha | tin nóng | 1 |
| soha | tiêm kích F-35 | 1 |
| soha | tiếng Việt | 1 |
| soha | tiết kiệm | 1 |
| soha | trẻ em tử vong vì nóng | 1 |
| soha | trồng cây | 1 |
| soha | tuyến đường sắt | 1 |
| soha | tuyển dụng giả gấu | 1 |
| soha | tài khoản Zalo bị theo dõi | 1 |
| soha | tài khoản ngân hàng | 1 |
| soha | tài nguyên công nghệ | 1 |
| soha | tàu dầu Nga | 1 |
| soha | tỉnh thái nguyên | 1 |
| soha | tổ chức sử dụng trái phép chất ma túy | 1 |
| soha | vợ chồng | 1 |
| soha | vụ án bé gái Thái Lan | 1 |
| soha | world cup 2026 | 1 |
| soha | xe cảnh sát | 1 |
| soha | xoài | 1 |
| soha | xử lý hành chính | 1 |
| soha | án tử hình Tây Ninh | 1 |
| soha | âm thanh lạ từ quan tài | 1 |
| soha | ô tô bị chém kính | 1 |
| soha | ô tô lao vào đám đông | 1 |
| soha | Đặng Thị Kim Ngân | 1 |
| soha | Đức tài trợ Houthi | 1 |
| soha | điện thoại đang bị theo dõi | 1 |
| soha | đoàn tàu Bạch Mai | 1 |
| soha | đuối nước | 1 |
| soha | đường dây ma túy | 1 |
| soha | đội tuyển Việt Nam | 1 |
| soha | động đất | 1 |
| soha | động đất kép | 1 |
| soha | ủy quyền nhận lương hưu | 1 |
| thanhnien | Thời sự | 32 |
| thanhnien | World Cup 2026 | 31 |
| thanhnien | Thế giới | 25 |
| thanhnien | Giới trẻ | 15 |
| thanhnien | Giáo dục | 12 |
| thanhnien | Kinh tế | 12 |
| thanhnien | Chính sách - Phát triển | 11 |
| thanhnien | Văn hóa | 11 |
| thanhnien | Sức khỏe | 10 |
| thanhnien | Đời nghệ sĩ | 9 |
| thanhnien | Cộng đồng | 8 |
| thanhnien | Dân sinh | 8 |
| thanhnien | Bạn cần biết | 7 |
| thanhnien | Pháp luật | 7 |
| thanhnien | Tin tức công nghệ | 7 |
| thanhnien | Thị trường | 6 |
| thanhnien | Bóng đá Việt Nam | 5 |
| thanhnien | Thời trang 24/7 | 5 |
| thanhnien | Giải trí | 4 |
| thanhnien | Địa ốc | 4 |
| thanhnien | Đời sống | 4 |
| thanhnien | Ẩm thực | 4 |
| thanhnien | Chính trị | 3 |
| thanhnien | Câu chuyện văn hóa | 3 |
| thanhnien | Ngân hàng | 3 |
| thanhnien | Sản phẩm | 3 |
| thanhnien | Thủ thuật | 3 |
| thanhnien | Các môn khác | 2 |
| thanhnien | Khỏe đẹp mỗi ngày | 2 |
| thanhnien | Kinh tế xanh | 2 |
| thanhnien | Quân sự | 2 |
| thanhnien | Sống đẹp | 2 |
| thanhnien | Tin tức - Sự kiện | 2 |
| thanhnien | (none) | 1 |
| thanhnien | Bạn đọc | 1 |
| thanhnien | Chuyện lạ | 1 |
| thanhnien | Chống tin giả | 1 |
| thanhnien | Câu chuyện du lịch | 1 |
| thanhnien | Game | 1 |
| thanhnien | Gia đình | 1 |
| thanhnien | Góc nhìn | 1 |
| thanhnien | Khám phá | 1 |
| thanhnien | Làm đẹp | 1 |
| thanhnien | Mới- Mới- Mới | 1 |
| thanhnien | Phim | 1 |
| thanhnien | Sống - Yêu - Ăn - Chơi | 1 |
| thanhnien | Thành tựu y khoa | 1 |
| thanhnien | Thẩm mỹ an toàn | 1 |
| thanhnien | Tin tức thời sự nhanh 24h | 1 |
| thanhnien | Trực tuyến | 1 |
| thanhnien | Tư vấn | 1 |
| thanhnien | Video | 1 |
| thanhnien | Xe - Giao thông | 1 |
| thanhnien | Xu hướng - Chuyển đổi số | 1 |
| tienphong | Xã hội | 64 |
| tienphong | Bóng đá | 43 |
| tienphong | Thế giới | 28 |
| tienphong | Pháp luật | 26 |
| tienphong | Tin tức | 26 |
| tienphong | Hoa học trò | 24 |
| tienphong | Kinh tế | 21 |
| tienphong | Sinh viên Việt Nam | 21 |
| tienphong | Âm nhạc | 17 |
| tienphong | Hậu trường SHOWBIZ | 16 |
| tienphong | Giải trí | 12 |
| tienphong | Xe | 12 |
| tienphong | Địa ốc | 12 |
| tienphong | Hậu trường sao | 10 |
| tienphong | Giới trẻ | 9 |
| tienphong | Sức khỏe | 9 |
| tienphong | Video | 9 |
| tienphong | Khoa học | 7 |
| tienphong | Hành trình | 6 |
| tienphong | Nhịp sống | 6 |
| tienphong | Thị trường | 6 |
| tienphong | Sóng xanh | 5 |
| tienphong | Đẹp hơn mỗi ngày | 5 |
| tienphong | Giáo dục | 4 |
| tienphong | Hàng không - Du lịch | 4 |
| tienphong | Tài chính - Chứng khoán | 4 |
| tienphong | Kết nối Hoa Học Trò | 3 |
| tienphong | Media Địa ốc | 3 |
| tienphong | Nhịp sống Thủ đô | 3 |
| tienphong | Nhịp sống phương Nam | 3 |
| tienphong | Ảnh | 3 |
| tienphong | (none) | 2 |
| tienphong | Gương mặt sinh viên | 2 |
| tienphong | Horoscope | 2 |
| tienphong | Phim ảnh | 2 |
| tienphong | Podcast | 2 |
| tienphong | Bạn đọc | 1 |
| tienphong | Diễn đàn | 1 |
| tienphong | Hoa hậu | 1 |
| tienphong | Học đường | 1 |
| tienphong | Thể thao | 1 |
| tienphong | Tuyển sinh | 1 |
| tienphong | Văn hóa | 1 |
| tienphong | World Cup 2026 | 1 |
| tienphong | Yêu | 1 |
| tienphong | Ảnh-Clip hay | 1 |
| tuoitre | thoi-su | 204 |
| tuoitre | the-gioi | 114 |
| tuoitre | kinh-doanh | 89 |
| tuoitre | phap-luat | 49 |
| tuoitre | giao-duc | 33 |
| tuoitre | suc-khoe | 33 |
| vietnamnet | World Cup | 98 |
| vietnamnet | Tin tức | 24 |
| vietnamnet | Tài chính | 21 |
| vietnamnet | Thể thao | 19 |
| vietnamnet | Thế giới | 18 |
| vietnamnet | Thị trường | 18 |
| vietnamnet | Tuyển sinh | 18 |
| vietnamnet | Dân sinh | 16 |
| vietnamnet | Pháp luật | 11 |
| vietnamnet | Thế giới sao | 11 |
| vietnamnet | Tin nóng | 11 |
| vietnamnet | Ô tô - Xe máy | 10 |
| vietnamnet | Chính trị | 8 |
| vietnamnet | Giao thông | 8 |
| vietnamnet | Dân tộc và Tôn giáo | 7 |
| vietnamnet | Bản tin thời sự | 6 |
| vietnamnet | Công nghệ | 6 |
| vietnamnet | Gia đình | 6 |
| vietnamnet | Văn hóa - Giải trí | 6 |
| vietnamnet | Tư vấn sức khỏe | 5 |
| vietnamnet | Đi đâu chơi đi | 5 |
| vietnamnet | Phim - Truyền hình | 4 |
| vietnamnet | Quân sự | 4 |
| vietnamnet | Dự án | 3 |
| vietnamnet | Hạ tầng số | 3 |
| vietnamnet | Kinh doanh | 3 |
| vietnamnet | Nhà trường | 3 |
| vietnamnet | Quốc phòng | 3 |
| vietnamnet | Thế giới đó đây | 3 |
| vietnamnet | Bất động sản | 2 |
| vietnamnet | Chuyện lạ | 2 |
| vietnamnet | Chân dung | 2 |
| vietnamnet | Tâm sự | 2 |
| vietnamnet | Video | 2 |
| vietnamnet | Đầu tư | 2 |
| vietnamnet | Ẩm thực | 2 |
| vietnamnet | (none) | 1 |
| vietnamnet | AI CONTEST | 1 |
| vietnamnet | AMACCAO | 1 |
| vietnamnet | An ninh mạng | 1 |
| vietnamnet | Bàn luận | 1 |
| vietnamnet | Bóng đá Việt Nam | 1 |
| vietnamnet | Chia sẻ | 1 |
| vietnamnet | Chuyển đổi số | 1 |
| vietnamnet | Di sản | 1 |
| vietnamnet | Du học | 1 |
| vietnamnet | Du lịch | 1 |
| vietnamnet | Giới trẻ | 1 |
| vietnamnet | Khám phá | 1 |
| vietnamnet | Làm đẹp | 1 |
| vietnamnet | Mỹ thuật - Sân khấu | 1 |
| vietnamnet | Ngày mai tươi sáng | 1 |
| vietnamnet | Nhạc | 1 |
| vietnamnet | Nội dung chuyên đề | 1 |
| vietnamnet | Nội thất | 1 |
| vietnamnet | Sản phẩm | 1 |
| vietnamnet | Sức khỏe | 1 |
| vietnamnet | Thời sự | 1 |
| vietnamnet | Trắc nghiệm | 1 |
| vietnamnet | Tuần Việt Nam | 1 |
| vietnamnet | Tư vấn | 1 |
| vietnamnet | Tư vấn tài chính | 1 |
| vietnamnet | Xây dựng Đảng | 1 |
| vietnamnet | xăng dầu | 1 |
| vietnamnet | Ăn Ăn Uống Uống | 1 |
| vietnamnet | Đối ngoại | 1 |
| vietnamnet | Đời sống | 1 |
| vietnamnet | Đời sống tôn giáo | 1 |
| vietnamplus | Xã hội | 121 |
| vietnamplus | Thế giới | 63 |
| vietnamplus | Đời sống | 32 |
| vietnamplus | Bóng đá | 27 |
| vietnamplus | Multimedia | 22 |
| vietnamplus | Chính trị | 21 |
| vietnamplus | Kinh doanh | 18 |
| vietnamplus | Thị trường | 15 |
| vietnamplus | Công nghệ | 14 |
| vietnamplus | Kinh tế | 12 |
| vietnamplus | Châu Á-TBD | 11 |
| vietnamplus | Văn hóa | 11 |
| vietnamplus | Điểm đến | 9 |
| vietnamplus | Chứng khoán | 6 |
| vietnamplus | Du lịch | 6 |
| vietnamplus | Bất động sản | 4 |
| vietnamplus | Khoa học ứng dụng | 3 |
| vietnamplus | Doanh nghiệp | 2 |
| vietnamplus | Sản phẩm mới | 2 |
| vietnamplus | Giao thông | 1 |
| vietnamplus | Môi trường | 1 |
| vietnamplus | Pháp luật | 1 |
| vietnamplus | Web Story | 1 |
| vietnamplus | Điện ảnh | 1 |
| vneconomy | Thế giới | 39 |
| vneconomy | Kinh tế số | 29 |
| vneconomy | Thị trường | 27 |
| vneconomy | Chứng khoán | 26 |
| vneconomy | Dân sinh | 26 |
| vneconomy | Bất động sản | 21 |
| vneconomy | Kinh tế xanh | 11 |
| vneconomy | Tiêu điểm | 11 |
| vneconomy | Đầu tư | 11 |
| vneconomy | Doanh nghiệp | 10 |
| vneconomy | Tài chính | 10 |
| vneconomy | Du lịch | 9 |
| vneconomy | eMagazine | 9 |
| vneconomy | Doanh nghiệp niêm yết | 7 |
| vneconomy | Đẹp + | 6 |
| vneconomy | Hạ tầng | 4 |
| vneconomy | Sức khỏe | 4 |
| vneconomy | Địa phương | 4 |
| vneconomy | Giải trí | 3 |
| vneconomy | Dự án | 2 |
| vneconomy | Tiêu & Dùng | 2 |
| vneconomy | Video | 2 |
| vneconomy | Chuyển động xanh | 1 |
| vneconomy | Khung pháp lý | 1 |
| vneconomy | Nhà | 1 |
| vneconomy | Thế | 1 |
| vnexpress | suc-khoe | 146 |
| vnexpress | the-gioi | 104 |
| vnexpress | kinh-doanh | 77 |
| vnexpress | thoi-su | 76 |
| vnexpress | phap-luat | 57 |
| vnexpress | giao-duc | 22 |

![Articles per section](figures/articles_per_section.png)


## 3. Articles per publish day

| d | articles |
| --- | --- |
| 2026-06-22 | 178 |
| 2026-06-23 | 443 |
| 2026-06-24 | 2157 |
| 2026-06-25 | 716 |
| 2026-06-26 | 1448 |
| 2026-06-27 | 1019 |

![Articles per day](figures/articles_per_day.png)


## 4. Missingness by field (% null)

| outlet | n | %miss_body | %miss_section | %miss_publish_datetime | %miss_author |
| --- | --- | --- | --- | --- | --- |
| 24h | 417 | 0.2 | 0.7 | 0.0 | 0.2 |
| baochinhphu | 194 | 0.0 | 23.7 | 0.0 | 0.0 |
| cafef | 305 | 0.0 | 1.0 | 0.0 | 0.0 |
| dantri | 427 | 3.7 | 3.7 | 0.0 | 0.0 |
| kenh14 | 299 | 0.0 | 7.0 | 0.0 | 0.0 |
| nhandan | 525 | 0.8 | 1.3 | 0.0 | 1.3 |
| qdnd | 390 | 0.3 | 0.5 | 0.0 | 0.3 |
| saostar | 402 | 0.0 | 0.0 | 0.0 | 0.0 |
| soha | 300 | 0.0 | 24.7 | 0.0 | 0.0 |
| thanhnien | 285 | 0.4 | 0.4 | 0.0 | 0.4 |
| tienphong | 441 | 0.2 | 0.5 | 0.0 | 0.5 |
| tuoitre | 522 | 0.0 | 0.0 | 0.0 | 0.0 |
| vietnamnet | 404 | 0.2 | 0.2 | 0.0 | 0.2 |
| vietnamplus | 404 | 0.0 | 0.0 | 0.0 | 20.5 |
| vneconomy | 277 | 0.0 | 0.0 | 0.0 | 0.0 |
| vnexpress | 482 | 0.0 | 0.0 | 0.0 | 98.8 |
| ALL | 6074 | 0.4 | 2.9 | 0.0 | 9.4 |

## 5. Article length (Vietnamese word tokens)

| outlet | n_with_body | mean | median |
| --- | --- | --- | --- |
| 24h | 416 | 551.7 | 502.5 |
| baochinhphu | 194 | 949.5 | 725.0 |
| cafef | 305 | 701.4 | 643.0 |
| dantri | 411 | 628.2 | 595.0 |
| kenh14 | 299 | 705.4 | 642.0 |
| nhandan | 521 | 656.7 | 561.0 |
| qdnd | 389 | 568.4 | 457.0 |
| saostar | 402 | 531.4 | 497.5 |
| soha | 300 | 591.2 | 526.0 |
| thanhnien | 284 | 522.1 | 480.5 |
| tienphong | 440 | 495.6 | 442.0 |
| tuoitre | 522 | 501.2 | 436.0 |
| vietnamnet | 403 | 496.2 | 410.0 |
| vietnamplus | 404 | 627.4 | 522.5 |
| vneconomy | 277 | 1185.2 | 1089.0 |
| vnexpress | 482 | 549.3 | 492.5 |

![Mean length per outlet](figures/mean_length_per_outlet.png)


## 6. Language

| lang | articles |
| --- | --- |
| vi | 6049 |
|  | 25 |

_Non-`vi` (flagged): 0._


## 7. Duplication

- Articles with extractable body: **6049**
- Exact-duplicate copies (verbatim body, after first): **50**
- Exact-duplicate rate: **0.8%**
- Distinct content clusters: **5999**
- Cross-outlet verbatim clusters (syndication signal): **28** (56 articles)

- Near-duplicate (same-story) copies: **52** (3.6%), in **41** multi-article clusters
- **Cross-outlet** same-story clusters: **36** (74 articles) — the syndication/overlap signal that exact-hash misses

