# QUY TẮC DEPLOY DỰ ÁN ytuong-fedu-vn (BẮT BUỘC)

## Kiến trúc deploy
- Cloudflare Pages chỉ đọc thư mục `dist/` (cấu hình trong `wrangler.json` → `pages_build_output_dir: "dist"`)
- Mọi file/thư mục ở root KHÔNG tự động lên web. Phải có lệnh copy vào `dist/`.

## Quy tắc khi tạo trang web mới
1. Tạo file ở root (VD: `training/index.html`)
2. **BẮT BUỘC** thêm lệnh `shutil.copytree()` hoặc `shutil.copy2()` vào script build tương ứng để copy sang `dist/`
3. Nghiệm thu = kiểm tra file **trong `dist/`**, KHÔNG phải ở root

## Quy tắc nghiệm thu trước khi git push
1. Kiểm tra `dist/` có chứa đúng file/thư mục mới tạo
2. Nếu tạo trang mới (VD: `/training`), chạy `curl -s -o /dev/null -w "%{http_code}" https://ytuong.fedu.vn/<path>` sau khi deploy để xác nhận HTTP 200
3. KHÔNG bao giờ chỉ kiểm tra ở root rồi kết luận PASS

## Luồng build hiện tại
- `build_ideas_bank.py` → sync `index.html`, `ideas_data.js`, `reports/`, `master_classifications.json`, `curation_config.json` → `dist/`
- `training_data_builder.py` → sync `training_data.js`, `training/` → `dist/`
