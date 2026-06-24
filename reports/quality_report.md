# Vietnamese News Diversity — Phase 1 Data-Quality Report

*Supply-side snapshot. Descriptive completeness check on the published cross-section; no exposure or substantive-coverage claims.*

- **Generated:** 2026-06-24T15:51:48.894951+07:00
- **Window:** 2026-06-03 → 2026-06-24 (Asia/Ho_Chi_Minh)
- **Articles:** 1706  |  **Outlets:** 16  |  **Sections observed:** 457
- **Segmentation:** {'underthesea': 1695} (token counts)


## 1. Articles per outlet

| outlet | outlet_type | articles |
| --- | --- | --- |
| nhandan | party_official | 203 |
| vnexpress | semi_commercial | 203 |
| tuoitre | union_mass_daily | 200 |
| vneconomy | sector_business | 102 |
| saostar | popular_lifestyle | 100 |
| 24h | popular_lifestyle | 100 |
| qdnd | party_official | 100 |
| dantri | semi_commercial | 100 |
| vietnamplus | party_official | 100 |
| vietnamnet | semi_commercial | 100 |
| tienphong | union_mass_daily | 100 |
| kenh14 | popular_lifestyle | 64 |
| cafef | sector_business | 63 |
| thanhnien | union_mass_daily | 61 |
| soha | popular_lifestyle | 60 |
| baochinhphu | party_official | 50 |

![Articles per outlet](figures/articles_per_outlet.png)


## 2. Articles per outlet × section

_Section provenance differs by outlet, which is itself a measurement-validity observation (not a data error). VnExpress and Tuổi Trẻ supply clean per-section RSS, so their `section` values are controlled slugs (`thoi-su`, `phap-luat`, …). Nhân Dân (party_official) exposes no reliable per-section feed and uses flat article URLs; its `section` is recovered from page categories where present — natural-language labels mixing topical and geographic taxonomies (`Thể thao`, `Môi trường`, `Duyên hải Nam Trung Bộ và Tây Nguyên`) — and `(none)` otherwise. The section vocabulary is therefore not directly comparable across outlet types and will need harmonisation before any section-based diversity metric._


| outlet | section | articles |
| --- | --- | --- |
| 24h | Ronaldo | 3 |
| 24h | giá vàng | 3 |
| 24h | Hà Nội | 2 |
| 24h | Messi | 2 |
| 24h | Quỳnh Anh Shyn | 2 |
| 24h | mỹ | 2 |
| 24h | (none) | 1 |
| 24h | ADN | 1 |
| 24h | Andy Burnham | 1 |
| 24h | Apple | 1 |
| 24h | Biệt thự 525 m2 | 1 |
| 24h | Bồ Đào Nha | 1 |
| 24h | CHDC Congo Colombia | 1 |
| 24h | Chồng ghen tuông | 1 |
| 24h | Declan Rice | 1 |
| 24h | Giá vàng hôm nay | 1 |
| 24h | Giẫm đạp | 1 |
| 24h | HLV Deschamps | 1 |
| 24h | Honda Prelude Limited Edition | 1 |
| 24h | Honda Vario 125 | 1 |
| 24h | Hồng Đăng du lịch | 1 |
| 24h | Keito Nakamura | 1 |
| 24h | Lisa | 1 |
| 24h | Lê Phương | 1 |
| 24h | Lý Kim Minh | 1 |
| 24h | Lý lịch tư pháp | 1 |
| 24h | Mỹ | 1 |
| 24h | Mỹ Tâm | 1 |
| 24h | Neymar Junior | 1 |
| 24h | Nga | 1 |
| 24h | Ngoại trưởng Mỹ | 1 |
| 24h | Ngọc Quỳnh | 1 |
| 24h | Núi Cấm | 1 |
| 24h | Omoda C5 | 1 |
| 24h | Panama | 1 |
| 24h | Pháp | 1 |
| 24h | Putin | 1 |
| 24h | Realme p4x 4g | 1 |
| 24h | Scotland | 1 |
| 24h | Thượng viện Mỹ | 1 |
| 24h | Timothée Chalamet | 1 |
| 24h | Tiểu Long Nữ | 1 |
| 24h | Trái Đất | 1 |
| 24h | Tập đoàn Sơn Hải | 1 |
| 24h | Tụ điện | 1 |
| 24h | Vĩnh Long | 1 |
| 24h | Vương Sở Nhiên | 1 |
| 24h | Xe MPV | 1 |
| 24h | Xioban | 1 |
| 24h | biển số giả | 1 |
| 24h | clip phút 90+ | 1 |
| 24h | con ac ac wimbledon | 1 |
| 24h | du lịch hội an | 1 |
| 24h | dứa | 1 |
| 24h | giá mắc cọp | 1 |
| 24h | giá xăng | 1 |
| 24h | giảm cân | 1 |
| 24h | giấy chứng nhận quyền sử dụng đất | 1 |
| 24h | học phí khối Y Dược | 1 |
| 24h | hố đen ngủ đông | 1 |
| 24h | iPhone | 1 |
| 24h | iPhone 18 Pro | 1 |
| 24h | lừa tình | 1 |
| 24h | mang hung khí điều khiển xe mô tô | 1 |
| 24h | mâm cơm gia đình | 1 |
| 24h | mã độc WhatsApp | 1 |
| 24h | nang wags | 1 |
| 24h | nga | 1 |
| 24h | phường Thanh Xuân | 1 |
| 24h | rút BHXH một lần | 1 |
| 24h | sử dụng điện thoại | 1 |
| 24h | tai nạn giao thông | 1 |
| 24h | tennis dinh cao | 1 |
| 24h | thành phố Bắc Ninh | 1 |
| 24h | thời tiết Hà Nội | 1 |
| 24h | tim mạch | 1 |
| 24h | trái cây nhập khẩu | 1 |
| 24h | tôm khô | 1 |
| 24h | tăng nặng mức phạt | 1 |
| 24h | tổ dân phố | 1 |
| 24h | tỷ giá usd | 1 |
| 24h | ung thư dạ dày | 1 |
| 24h | viêm cơ tim | 1 |
| 24h | vo gạo trước khi nấu cơm | 1 |
| 24h | vợ Duy Mạnh | 1 |
| 24h | xe máy | 1 |
| 24h | ĐT Anh | 1 |
| 24h | Điểm chuẩn | 1 |
| 24h | Điện lực TPHCM | 1 |
| 24h | Đề thi môn Văn | 1 |
| 24h | Đỗ Mỹ Linh sau sinh | 1 |
| 24h | điểm chuẩn vào lớp 10 | 1 |
| baochinhphu | (none) | 12 |
| baochinhphu | Chủ tịch Quốc hội | 3 |
| baochinhphu | Nghị quyết 57-NQ/TW | 2 |
| baochinhphu | Phó Thủ tướng | 2 |
| baochinhphu | Tổng Bí thư | 2 |
| baochinhphu | Agribank | 1 |
| baochinhphu | Hộ kinh doanh | 1 |
| baochinhphu | Người cao tuổi | 1 |
| baochinhphu | Thanh Tra | 1 |
| baochinhphu | Vĩnh Long | 1 |
| baochinhphu | Y tế | 1 |
| baochinhphu | an ninh phi truyền thống | 1 |
| baochinhphu | bác sĩ | 1 |
| baochinhphu | bảo hiểm bắt buộc trong xây dựng\ | 1 |
| baochinhphu | công nghệ hiện đại | 1 |
| baochinhphu | giao thông | 1 |
| baochinhphu | giấy phép xây dựng | 1 |
| baochinhphu | hài cốt liệt sĩ | 1 |
| baochinhphu | miễn thuế | 1 |
| baochinhphu | nghỉ việc | 1 |
| baochinhphu | nhà giáo ưu tú | 1 |
| baochinhphu | phó thủ tướng thường trực | 1 |
| baochinhphu | phường | 1 |
| baochinhphu | thu ngân sách | 1 |
| baochinhphu | thủ tướng | 1 |
| baochinhphu | tín dụng xanh | 1 |
| baochinhphu | tăng trưởng hai con số | 1 |
| baochinhphu | vi phạm | 1 |
| baochinhphu | vận tải | 1 |
| baochinhphu | vốn tín dụng chính sách | 1 |
| baochinhphu | Đoàn Thanh niên Chính phủ | 1 |
| baochinhphu | Đại học Nam Cần Thơ | 1 |
| baochinhphu | đo lường | 1 |
| baochinhphu | đăng ký doanh nghiệp | 1 |
| cafef | việt nam | 4 |
| cafef | cổ phiếu | 3 |
| cafef | nga | 2 |
| cafef | (none) | 1 |
| cafef | 5 loại cá | 1 |
| cafef | Apple | 1 |
| cafef | Bắc Ninh | 1 |
| cafef | Bộ Tài chính | 1 |
| cafef | Công an TP Đà Nẵng | 1 |
| cafef | DIC Corp | 1 |
| cafef | Dự án quan trọng của Nga | 1 |
| cafef | Galaxy Cruiser 700 | 1 |
| cafef | Google | 1 |
| cafef | Messi | 1 |
| cafef | Móng tay | 1 |
| cafef | Mẹ đảm miền Tây | 1 |
| cafef | Nam sinh mê Toán | 1 |
| cafef | Nắng nóng cực đoan | 1 |
| cafef | Phát hiện 30 kg vàng | 1 |
| cafef | Sun PhuQuoc Airways | 1 |
| cafef | Trường Đại học Y Dược Hải Phòng | 1 |
| cafef | Trợ lý cảnh sát | 1 |
| cafef | VietJet | 1 |
| cafef | Vinspeed | 1 |
| cafef | WinCommerce | 1 |
| cafef | anker | 1 |
| cafef | bảo hiểm nhân thọ | 1 |
| cafef | bất động sản | 1 |
| cafef | chuyển khoản | 1 |
| cafef | châu âu | 1 |
| cafef | công an | 1 |
| cafef | công nghệ | 1 |
| cafef | cơ quan thuế | 1 |
| cafef | cửa trượt nhà bếp | 1 |
| cafef | dự án | 1 |
| cafef | giấy tờ | 1 |
| cafef | hoa hậu | 1 |
| cafef | khách hàng | 1 |
| cafef | lừa đảo | 1 |
| cafef | malaysia | 1 |
| cafef | miền Tây | 1 |
| cafef | ngân hàng | 1 |
| cafef | nhnn | 1 |
| cafef | nhà ở xã hội | 1 |
| cafef | quy định mới | 1 |
| cafef | sống lâu | 1 |
| cafef | thi hành lệnh bắt tạm giam | 1 |
| cafef | thương mại điện tử | 1 |
| cafef | thị trường | 1 |
| cafef | trung quốc | 1 |
| cafef | tập đoàn Sơn Hải | 1 |
| cafef | vàng | 1 |
| cafef | vận tải biển | 1 |
| cafef | wimbledon | 1 |
| cafef | Đóng BHXH | 1 |
| cafef | điện thoại đang bị theo dõi | 1 |
| cafef | đại học | 1 |
| dantri | Thế giới | 12 |
| dantri | Thời sự | 12 |
| dantri | Pháp luật | 10 |
| dantri | Kinh doanh | 9 |
| dantri | Sức khỏe | 9 |
| dantri | Nội vụ | 7 |
| dantri | (none) | 6 |
| dantri | Giáo dục | 6 |
| dantri | Thể thao | 6 |
| dantri | Bất động sản | 5 |
| dantri | Giải trí | 5 |
| dantri | Công nghệ | 4 |
| dantri | Đời sống | 4 |
| dantri | Du lịch | 1 |
| dantri | Khoa học | 1 |
| dantri | Lao động - Việc làm | 1 |
| dantri | Tâm điểm | 1 |
| dantri | Tấm lòng nhân ái | 1 |
| kenh14 | (none) | 7 |
| kenh14 | World Cup 2026 | 4 |
| kenh14 | giải trí | 3 |
| kenh14 | thể thao | 3 |
| kenh14 | World Cup | 2 |
| kenh14 | nắng nóng | 2 |
| kenh14 | ronaldo | 2 |
| kenh14 | đời sống | 2 |
| kenh14 | Ca sĩ Việt | 1 |
| kenh14 | Facebook | 1 |
| kenh14 | Google | 1 |
| kenh14 | Lý Kim Minh | 1 |
| kenh14 | Mua nhà | 1 |
| kenh14 | NSƯT Ngọc Quỳnh | 1 |
| kenh14 | Phạm Quỳnh Anh | 1 |
| kenh14 | Psi Scott | 1 |
| kenh14 | Starbucks | 1 |
| kenh14 | Sỏi bàng quang | 1 |
| kenh14 | Thi vào lớp 10 | 1 |
| kenh14 | Vinamilk | 1 |
| kenh14 | Z-School Tour | 1 |
| kenh14 | bellingham | 1 |
| kenh14 | bạo hành | 1 |
| kenh14 | chuyển khoản | 1 |
| kenh14 | chuyển khoản nhầm | 1 |
| kenh14 | croatia | 1 |
| kenh14 | dân văn phòng | 1 |
| kenh14 | giá vàng hôm nay | 1 |
| kenh14 | lyly | 1 |
| kenh14 | lịch sử | 1 |
| kenh14 | lớp 10 | 1 |
| kenh14 | messi | 1 |
| kenh14 | miền bắc nắng nóng | 1 |
| kenh14 | nạp tiền | 1 |
| kenh14 | phạm băng băng | 1 |
| kenh14 | thiếu nữ bỏ nhà đi | 1 |
| kenh14 | thịt lợn | 1 |
| kenh14 | tranh cãi | 1 |
| kenh14 | trần triết viễn | 1 |
| kenh14 | tuyển anh | 1 |
| kenh14 | tôm khô | 1 |
| kenh14 | ung thư | 1 |
| kenh14 | vỡ hoàng thể | 1 |
| kenh14 | Đường sắt mở Đoàn tàu Bạch Mai | 1 |
| kenh14 | Đặng Triệu Tôn | 1 |
| kenh14 | điều hòa | 1 |
| kenh14 | điện thoại | 1 |
| nhandan | Kinh tế | 26 |
| nhandan | Chính trị | 22 |
| nhandan | Thể thao | 20 |
| nhandan | Xã hội | 18 |
| nhandan | Đồng bằng sông Hồng | 14 |
| nhandan | Văn hóa | 11 |
| nhandan | Châu Âu | 10 |
| nhandan | Môi trường | 10 |
| nhandan | Tin chung | 10 |
| nhandan | Thế giới | 8 |
| nhandan | Y tế | 8 |
| nhandan | (none) | 5 |
| nhandan | Văn hóa - Văn nghệ | 5 |
| nhandan | Duyên hải Nam Trung Bộ và Tây Nguyên | 4 |
| nhandan | Khoa học - Công nghệ | 4 |
| nhandan | Pháp luật | 3 |
| nhandan | Thời Nay | 3 |
| nhandan | Trung Đông | 3 |
| nhandan | Bình luận quốc tế | 2 |
| nhandan | Bạn đọc | 2 |
| nhandan | Chuyên trang Hà Nội | 2 |
| nhandan | Châu Phi | 2 |
| nhandan | Giáo dục | 2 |
| nhandan | Ảnh | 2 |
| nhandan | Chuyển đổi số | 1 |
| nhandan | Châu Mỹ | 1 |
| nhandan | Châu Á-TBD | 1 |
| nhandan | Văn hóa làng quê | 1 |
| nhandan | Xây dựng nông thôn mới | 1 |
| nhandan | Xây dựng Đảng | 1 |
| nhandan | Đồng bằng sông Cửu Long | 1 |
| qdnd | World Cup 2026 | 5 |
| qdnd | Ronaldo | 4 |
| qdnd | World Cup | 3 |
| qdnd | Mỹ | 2 |
| qdnd | Tổng Bí thư | 2 |
| qdnd | eo biển Hormuz | 2 |
| qdnd | nhà ở | 2 |
| qdnd | Đoàn TNCS Hồ Chí Minh | 2 |
| qdnd | (none) | 1 |
| qdnd | AIDS | 1 |
| qdnd | An Giang | 1 |
| qdnd | Biên phòng Cửa khẩu Săm Pun | 1 |
| qdnd | Bảng xếp hạng World Cup 2026 hôm nay | 1 |
| qdnd | Bảo hiểm | 1 |
| qdnd | Bảo tàng Phụ nữ Việt Nam | 1 |
| qdnd | Bộ Tổng tham mưu | 1 |
| qdnd | Campuchia | 1 |
| qdnd | Cao Bằng | 1 |
| qdnd | Chuẩn úy Palina Dalasin | 1 |
| qdnd | Chính trường Anh | 1 |
| qdnd | Chứng khoán | 1 |
| qdnd | Cảnh sát biển | 1 |
| qdnd | Cục Quân khí | 1 |
| qdnd | Giá hồ tiêu | 1 |
| qdnd | Giá vàng | 1 |
| qdnd | Học viện Quốc phòng | 1 |
| qdnd | Iran | 1 |
| qdnd | Israel | 1 |
| qdnd | Khánh Hòa | 1 |
| qdnd | Link xem trực tiếp Bồ Đào Nha | 1 |
| qdnd | Link xem trực tiếp Colombia và Cộng hòa dân chủ Congo | 1 |
| qdnd | Link xem trực tiếp Panama và Croatia | 1 |
| qdnd | Lào Cai | 1 |
| qdnd | Lịch thi đấu World Cup 2026 hôm nay | 1 |
| qdnd | Messi | 1 |
| qdnd | Mộc bản triều Nguyễn | 1 |
| qdnd | New Zealand | 1 |
| qdnd | Nga | 1 |
| qdnd | Nhận định Scotland và Brazil | 1 |
| qdnd | Quân khu 4 | 1 |
| qdnd | Quân đoàn 34 | 1 |
| qdnd | Quảng Ninh | 1 |
| qdnd | TP Hồ Chí Minh | 1 |
| qdnd | Thanh Hóa | 1 |
| qdnd | Thủ tướng | 1 |
| qdnd | Thủ tướng Anh | 1 |
| qdnd | Thủy thủ | 1 |
| qdnd | Tin thể thao | 1 |
| qdnd | Trung tá QNCN Đinh Thị Hà | 1 |
| qdnd | Trung đoàn 102 | 1 |
| qdnd | Trung đoàn 88 | 1 |
| qdnd | Trường Sĩ quan Chính trị | 1 |
| qdnd | Trần Phi Hổ | 1 |
| qdnd | Tô Văn Đực | 1 |
| qdnd | UN Women | 1 |
| qdnd | VPBank | 1 |
| qdnd | Video bàn thắng Colombia và CHDC Congo | 1 |
| qdnd | Video bàn thắng Croatia và Panama | 1 |
| qdnd | Video trận đấu Anh và Ghana | 1 |
| qdnd | Vị Xuyên | 1 |
| qdnd | bóng đá | 1 |
| qdnd | chính quyền địa phương hai cấp | 1 |
| qdnd | diễn biến hòa bình | 1 |
| qdnd | giá dầu | 1 |
| qdnd | hài cốt liệt sĩ | 1 |
| qdnd | hàng không Mỹ | 1 |
| qdnd | lịch sử | 1 |
| qdnd | mẹ Việt Nam Anh hùng | 1 |
| qdnd | nghiệp vụ công tác văn phòng | 1 |
| qdnd | ngành xuất bản | 1 |
| qdnd | ngư dân | 1 |
| qdnd | người cao tuổi | 1 |
| qdnd | nhiếp ảnh | 1 |
| qdnd | nhà giàn | 1 |
| qdnd | nông sản | 1 |
| qdnd | quân sự | 1 |
| qdnd | thời tiết hôm nay | 1 |
| qdnd | tài xế công nghệ | 1 |
| qdnd | tỉnh Gia Lai | 1 |
| qdnd | tỷ giá USD | 1 |
| qdnd | video bàn thắng Bồ Đào Nha | 1 |
| qdnd | Đoàn Kinh tế | 1 |
| qdnd | Đại tá VĂN MẠNH SOÁI | 1 |
| qdnd | Đất đai | 1 |
| qdnd | Đắk Lắk | 1 |
| qdnd | đội tuyển Việt Nam | 1 |
| saostar | Phim ảnh | 29 |
| saostar | Sao | 19 |
| saostar | Âm nhạc | 12 |
| saostar | Sao Sport | 8 |
| saostar | Vòng quanh thế giới | 8 |
| saostar | Người mẫu - Hoa hậu | 6 |
| saostar | Cận cảnh cuộc sống | 5 |
| saostar | Du lịch - Khám phá | 5 |
| saostar | Fashion - Beauty | 4 |
| saostar | BĐS - Tài chính | 2 |
| saostar | Sức khỏe | 1 |
| saostar | Ăn - Chơi | 1 |
| soha | (none) | 18 |
| soha | World Cup | 2 |
| soha | báo công an | 2 |
| soha | quảng ninh | 2 |
| soha | BHXH | 1 |
| soha | EVN | 1 |
| soha | HIV | 1 |
| soha | Hành chính công | 1 |
| soha | Israel tự sản xuất vũ khí | 1 |
| soha | Kim Jong-un | 1 |
| soha | Lê Thị Hồng Nhung | 1 |
| soha | Mùa nào bệnh nấy | 1 |
| soha | Mỹ | 1 |
| soha | Soha Special | 1 |
| soha | Suzuki | 1 |
| soha | Trung Quốc | 1 |
| soha | cây | 1 |
| soha | cờ bạc trực tuyến | 1 |
| soha | giá vàng giảm | 1 |
| soha | hà nội | 1 |
| soha | làm sạch dép Crocs | 1 |
| soha | lớp 10 | 1 |
| soha | mệnh Kim tháng 7 | 1 |
| soha | mừng cưới | 1 |
| soha | nhà máy địa nhiệt | 1 |
| soha | phun thuốc diệt cỏ | 1 |
| soha | quy định kiểm tra thuế | 1 |
| soha | sao Việt | 1 |
| soha | shipper | 1 |
| soha | thu nhập chịu thuế | 1 |
| soha | tiêm kích F-35 | 1 |
| soha | tiếng Việt | 1 |
| soha | trẻ em tử vong vì nóng | 1 |
| soha | xe cảnh sát | 1 |
| soha | xử lý hành chính | 1 |
| soha | âm thanh lạ từ quan tài | 1 |
| soha | ô tô bị chém kính | 1 |
| soha | điện thoại đang bị theo dõi | 1 |
| soha | đường dây ma túy | 1 |
| soha | ủy quyền nhận lương hưu | 1 |
| thanhnien | Thời sự | 12 |
| thanhnien | Thế giới | 7 |
| thanhnien | Giới trẻ | 4 |
| thanhnien | World Cup 2026 | 4 |
| thanhnien | Đời nghệ sĩ | 4 |
| thanhnien | Thị trường | 3 |
| thanhnien | Bạn cần biết | 2 |
| thanhnien | Cộng đồng | 2 |
| thanhnien | Giáo dục | 2 |
| thanhnien | Kinh tế | 2 |
| thanhnien | Tin tức công nghệ | 2 |
| thanhnien | Văn hóa | 2 |
| thanhnien | Ẩm thực | 2 |
| thanhnien | Chống tin giả | 1 |
| thanhnien | Dân sinh | 1 |
| thanhnien | Game | 1 |
| thanhnien | Khỏe đẹp mỗi ngày | 1 |
| thanhnien | Làm đẹp | 1 |
| thanhnien | Phim | 1 |
| thanhnien | Pháp luật | 1 |
| thanhnien | Sức khỏe | 1 |
| thanhnien | Thời trang 24/7 | 1 |
| thanhnien | Thủ thuật | 1 |
| thanhnien | Tin tức - Sự kiện | 1 |
| thanhnien | Tin tức thời sự nhanh 24h | 1 |
| thanhnien | Địa ốc | 1 |
| tienphong | Xã hội | 23 |
| tienphong | Bóng đá | 9 |
| tienphong | Hoa học trò | 7 |
| tienphong | Sinh viên Việt Nam | 6 |
| tienphong | Thế giới | 6 |
| tienphong | Hậu trường SHOWBIZ | 5 |
| tienphong | Kinh tế | 5 |
| tienphong | Tin tức | 5 |
| tienphong | Xe | 5 |
| tienphong | Giới trẻ | 3 |
| tienphong | Hậu trường sao | 3 |
| tienphong | Nhịp sống | 3 |
| tienphong | Âm nhạc | 3 |
| tienphong | Giáo dục | 2 |
| tienphong | Pháp luật | 2 |
| tienphong | Thị trường | 2 |
| tienphong | Video | 2 |
| tienphong | Địa ốc | 2 |
| tienphong | (none) | 1 |
| tienphong | Giải trí | 1 |
| tienphong | Hàng không - Du lịch | 1 |
| tienphong | Hành trình | 1 |
| tienphong | Học đường | 1 |
| tienphong | Media Địa ốc | 1 |
| tienphong | Sức khỏe | 1 |
| tuoitre | thoi-su | 74 |
| tuoitre | the-gioi | 50 |
| tuoitre | kinh-doanh | 31 |
| tuoitre | phap-luat | 17 |
| tuoitre | giao-duc | 15 |
| tuoitre | suc-khoe | 13 |
| vietnamnet | World Cup | 22 |
| vietnamnet | Tuyển sinh | 10 |
| vietnamnet | Tin tức | 9 |
| vietnamnet | Thị trường | 5 |
| vietnamnet | Công nghệ | 4 |
| vietnamnet | Thế giới sao | 4 |
| vietnamnet | Thể thao | 4 |
| vietnamnet | Tin nóng | 4 |
| vietnamnet | Ô tô - Xe máy | 4 |
| vietnamnet | Pháp luật | 3 |
| vietnamnet | Thế giới | 3 |
| vietnamnet | Bản tin thời sự | 2 |
| vietnamnet | Dân sinh | 2 |
| vietnamnet | Quân sự | 2 |
| vietnamnet | Tài chính | 2 |
| vietnamnet | Đi đâu chơi đi | 2 |
| vietnamnet | AI CONTEST | 1 |
| vietnamnet | Bàn luận | 1 |
| vietnamnet | Chuyển đổi số | 1 |
| vietnamnet | Chuyện lạ | 1 |
| vietnamnet | Chân dung | 1 |
| vietnamnet | Dân tộc và Tôn giáo | 1 |
| vietnamnet | Gia đình | 1 |
| vietnamnet | Giới trẻ | 1 |
| vietnamnet | Hạ tầng số | 1 |
| vietnamnet | Kinh doanh | 1 |
| vietnamnet | Phim - Truyền hình | 1 |
| vietnamnet | Quốc phòng | 1 |
| vietnamnet | Trắc nghiệm | 1 |
| vietnamnet | Tư vấn | 1 |
| vietnamnet | Tư vấn sức khỏe | 1 |
| vietnamnet | Văn hóa - Giải trí | 1 |
| vietnamnet | Ăn Ăn Uống Uống | 1 |
| vietnamnet | Đối ngoại | 1 |
| vietnamplus | Xã hội | 23 |
| vietnamplus | Thế giới | 13 |
| vietnamplus | Đời sống | 13 |
| vietnamplus | Bóng đá | 10 |
| vietnamplus | Kinh doanh | 8 |
| vietnamplus | Multimedia | 8 |
| vietnamplus | Thị trường | 5 |
| vietnamplus | Văn hóa | 4 |
| vietnamplus | Chính trị | 3 |
| vietnamplus | Công nghệ | 3 |
| vietnamplus | Bất động sản | 2 |
| vietnamplus | Châu Á-TBD | 2 |
| vietnamplus | Chứng khoán | 1 |
| vietnamplus | Du lịch | 1 |
| vietnamplus | Khoa học ứng dụng | 1 |
| vietnamplus | Kinh tế | 1 |
| vietnamplus | Sản phẩm mới | 1 |
| vietnamplus | Điểm đến | 1 |
| vneconomy | Thế giới | 19 |
| vneconomy | Chứng khoán | 11 |
| vneconomy | Bất động sản | 10 |
| vneconomy | Kinh tế số | 8 |
| vneconomy | Thị trường | 8 |
| vneconomy | Dân sinh | 7 |
| vneconomy | Tài chính | 6 |
| vneconomy | Tiêu điểm | 5 |
| vneconomy | Kinh tế xanh | 4 |
| vneconomy | Sức khỏe | 4 |
| vneconomy | Đầu tư | 4 |
| vneconomy | Du lịch | 3 |
| vneconomy | Doanh nghiệp | 2 |
| vneconomy | Doanh nghiệp niêm yết | 2 |
| vneconomy | Hạ tầng | 2 |
| vneconomy | Đẹp + | 2 |
| vneconomy | Địa phương | 2 |
| vneconomy | Thế | 1 |
| vneconomy | Tiêu & Dùng | 1 |
| vneconomy | Video | 1 |
| vnexpress | suc-khoe | 57 |
| vnexpress | the-gioi | 42 |
| vnexpress | kinh-doanh | 34 |
| vnexpress | thoi-su | 33 |
| vnexpress | phap-luat | 25 |
| vnexpress | giao-duc | 12 |

![Articles per section](figures/articles_per_section.png)


## 3. Articles per publish day

| d | articles |
| --- | --- |
| 2026-06-22 | 178 |
| 2026-06-23 | 448 |
| 2026-06-24 | 1054 |

![Articles per day](figures/articles_per_day.png)


## 4. Missingness by field (% null)

| outlet | n | %miss_body | %miss_section | %miss_publish_datetime | %miss_author |
| --- | --- | --- | --- | --- | --- |
| 24h | 100 | 0.0 | 1.0 | 0.0 | 0.0 |
| baochinhphu | 50 | 0.0 | 24.0 | 0.0 | 0.0 |
| cafef | 63 | 0.0 | 1.6 | 0.0 | 0.0 |
| dantri | 100 | 6.0 | 6.0 | 0.0 | 0.0 |
| kenh14 | 64 | 0.0 | 10.9 | 0.0 | 0.0 |
| nhandan | 203 | 2.0 | 2.5 | 0.0 | 2.5 |
| qdnd | 100 | 1.0 | 1.0 | 0.0 | 1.0 |
| saostar | 100 | 0.0 | 0.0 | 0.0 | 0.0 |
| soha | 60 | 0.0 | 30.0 | 0.0 | 0.0 |
| thanhnien | 61 | 0.0 | 0.0 | 0.0 | 0.0 |
| tienphong | 100 | 0.0 | 1.0 | 0.0 | 1.0 |
| tuoitre | 200 | 0.0 | 0.0 | 0.0 | 0.0 |
| vietnamnet | 100 | 0.0 | 0.0 | 0.0 | 0.0 |
| vietnamplus | 100 | 0.0 | 0.0 | 0.0 | 16.0 |
| vneconomy | 102 | 0.0 | 0.0 | 0.0 | 0.0 |
| vnexpress | 203 | 0.0 | 0.0 | 0.0 | 99.0 |
| ALL | 1706 | 0.6 | 3.0 | 0.0 | 13.1 |

## 5. Article length (Vietnamese word tokens)

| outlet | n_with_body | mean | median |
| --- | --- | --- | --- |
| 24h | 100 | 583.6 | 547.5 |
| baochinhphu | 50 | 904.4 | 690.0 |
| cafef | 63 | 737.4 | 741.0 |
| dantri | 94 | 679.0 | 637.5 |
| kenh14 | 64 | 708.7 | 674.0 |
| nhandan | 199 | 700.5 | 603.0 |
| qdnd | 99 | 579.1 | 445.0 |
| saostar | 100 | 544.8 | 504.0 |
| soha | 60 | 594.7 | 518.0 |
| thanhnien | 61 | 523.9 | 506.0 |
| tienphong | 100 | 580.8 | 461.0 |
| tuoitre | 200 | 504.0 | 436.5 |
| vietnamnet | 100 | 519.3 | 429.0 |
| vietnamplus | 100 | 639.0 | 518.0 |
| vneconomy | 102 | 1149.7 | 1101.5 |
| vnexpress | 203 | 582.2 | 497.0 |

![Mean length per outlet](figures/mean_length_per_outlet.png)


## 6. Language

| lang | articles |
| --- | --- |
| vi | 1695 |
|  | 11 |

_Non-`vi` (flagged): 0._


## 7. Duplication

- Articles with extractable body: **1695**
- Exact-duplicate copies (verbatim body, after first): **9**
- Exact-duplicate rate: **0.5%**
- Distinct content clusters: **1686**
- Cross-outlet verbatim clusters (syndication signal): **3** (6 articles)

- Near-duplicate (same-story) copies: **57** (3.4%), in **49** multi-article clusters
- **Cross-outlet** same-story clusters: **44** (92 articles) — the syndication/overlap signal that exact-hash misses

