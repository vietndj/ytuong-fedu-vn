# TAG CHANGELOG — FEDU Ideas Bank (ytuong.fedu.vn)

> File này vừa là nhật ký thay đổi, vừa là **training data** cho AI học phân loại theo cách anh Việt muốn.
> AI PHẢI đọc file này TRƯỚC khi chạy bất kỳ cleanup nào.

---

## FORMAT

### Auto Cleanup
```
## [DATE] Auto Cleanup Run
| Field | Old | → Canonical | Count |
```

### Human Override (AI học từ đây)
```
## [DATE] HUMAN OVERRIDE ⚡
### Context: [mô tả tình huống]
### Action: [anh Việt đã làm gì]  
### Rule learned: [AI rút ra nguyên tắc gì]
### Future: [áp dụng ra sao lần sau]
```

---

## [2026-09-29] BOOTSTRAP — Khởi tạo hệ thống

### Phân tích ban đầu (296 ideas)
- shooting_style: 46 biến thể → cần chuẩn về 8 canonical slugs
- industries: 47 biến thể → cần chuẩn về 10 canonical slugs

### Canonical đã xác lập (từ audit data thực)

#### shooting_style
| Canonical ID | Name | Absorbs | Count hiện tại |
|---|---|---|---|
| `talking-head` | Talking Head | "Talking Head" (wrong case), "talking_head" | 35+1 |
| `dien-anh` | Điện Ảnh | "Cinematic B-Roll", "Cinematic B-roll", "B-Roll Điện Ảnh", "Điện Ảnh (Cinematic)", "Điện Ảnh Đời Thường (Cinematic)", "Cinematic / Đời thường", "lifestyle-cinematic", "Phim Điện Ảnh (Cinematic Stills)", "Điện Ảnh & Chữa Lành (Cinematic Mood / ASMR)", "Vlog Lifestyle / B-Roll Điện Ảnh", "Vlog", "Cinematic Vlog", "Cinematic Vlog / Cut On Action", "Cinematic", "Cinematic B-roll" | 110+13 |
| `chuyen-canh` | Chuyển Cảnh | "Chuyển Cảnh (Transition)", "chuyen_canh", "Chuyển Cảnh Thời Trang (OOTD Transition)" | 54+7 |
| `storytelling` | Kể Chuyện | "Kể Chuyện (Storytelling)", "Visual Storytelling" | 26+2 |
| `voice-over` | Lồng Tiếng | (clean) | 14 |
| `walk-and-talk` | Walk & Talk | "Walk and Talk", "Walk & Talk / Phỏng Vấn", "Walk and Talk Documentary" | 5+3 |
| `theo-nhip-nhac` | Theo Nhịp Nhạc | "POV & Fast-Paced Montage", "POV & Aesthetic B-Roll Montage", "pov", "Bố Cục (Framing)", "bien-hinh" | 3+5 |
| `ugc-thuc-chien` | UGC Thực Chiến | "UGC Thực Chiến", "Review Sản Phẩm / UGC", "Solo Creator Setup", "quang-cao", "Lookbook Thực Chiến", "Chỉn Chu / Bố Cục", "A Day In The Life (Vlog Không Lời)", "Quay B-Roll Quảng Cáo Điện Ảnh", "BTS / Hậu Trường Sáng Tạo", "Split Screen / Behind-The-Scenes" | 1+10 |

#### industries
| Canonical ID | Name | Absorbs | Count hiện tại |
|---|---|---|---|
| `ky-thuat-quay` | Kỹ Thuật Quay Dựng | "Kỹ Thuật Quay Dựng & Điện Ảnh", "ky-thuat-quay-dung", "Nhiếp Ảnh & Quay Phim", "Nhiếp Ảnh & Làm Phim", "Nhiếp Ảnh & Điện Ảnh", "Quay Dựng & Điện Ảnh", "Sáng Tạo Nội Dung & Video", "Sáng Tạo Nội Dung & Điện Ảnh", "sang-tao-noi-dung" | 57+9 |
| `cong-nghe` | Công Nghệ & Thiết Bị | "cong_nghe", "Công Nghệ & Thiết Bị" | 37+2 |
| `kien-truc` | Kiến Trúc & Không Gian | "Kiến Trúc & Không Gian Sống" | 33+1 |
| `am-thuc` | Ẩm Thực & F&B | "Ẩm Thực & F&B" | 26+1 |
| `thuong-hieu` | Thương Hiệu Cá Nhân | "thuong-hieu-ca-nhan", "Thương Hiệu Cá Nhân & Dịch Vụ" | 23+2 |
| `thoi-trang` | Thời Trang | "Thời Trang & Phụ Kiện", "Thời Trang & Phong Cách Sống", "Thời Trang & Streetwear" | 23+3 |
| `du-lich` | Du Lịch & Khám Phá | "Du Lịch & Khám Phá", "Du Lịch & Trải Nghiệm Sống", "Du Lịch & Văn Hóa", "du-lich-khach-san", "Phong Cách Sống & Du Lịch" | 19+5 |
| `the-thao` | Thể Thao & Năng Động | "Thể Thao & Năng Động" | 6+1 |
| `spa-lam-dep` | Làm Đẹp & Spa | "lam-dep", "Làm đẹp" | 5+2 |
| `doi-song` | Đời Sống & Lifestyle | "Đời Sống & Gia Đình", "Đời Sống & Phong Cách Sống", "Lifestyle & Phát Triển Bản Thân", "doi-thuong", "phat-trien-ban-than", "Phong Cách Sống & Nghệ Thuật", "Cinematic Lifestyle", "Vlog & Phong Cách Sống", "giao-duc", "Sự Kiện & Phỏng Vấn", "Đường Phố & Đời Sống", "Bố cục" | 0+12 |

### Status
- [ ] Chưa apply — chờ anh Việt duyệt bảng trên
- Để thực thi: gõ `DON DEP TAG` và xác nhận

---

<!-- 
=== HUMAN OVERRIDE TEMPLATE ===
## [DATE] HUMAN OVERRIDE ⚡
### Context: 
### Action:  
### Rule learned: 
### Future: 
-->
