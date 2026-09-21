import os
import subprocess
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

# ==========================================
# CẤU HÌNH API TELEGRAM CỦA ANH VIỆT
# Lấy tại: https://my.telegram.org/apps
# ==========================================
API_ID = 'ĐIỀN_API_ID_VÀO_ĐÂY'      # Lấy số trên web (VD: 1234567)
API_HASH = 'ĐIỀN_API_HASH_VÀO_ĐÂY'  # Chuỗi ký tự (VD: '0123456789abcdef')
PHONE_NUMBER = '+84934688632'
SESSION_NAME = 'vietndj_tele_session'

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

async def upload_video(file_path):
    print(f"\n🚀 Đang đẩy file {os.path.basename(file_path)} lên Telegram...")
    try:
        # Gửi vào "Saved Messages" (Kho lưu trữ đám mây cá nhân vô hạn)
        await client.send_file(
            'me', 
            file_path, 
            caption=f"Backup: {os.path.basename(file_path)}",
            force_document=False,
            video_note=False,
            supports_streaming=True
        )
        print(f"✅ Đã đẩy thành công: {os.path.basename(file_path)}")
        return True
    except Exception as e:
        print(f"❌ Lỗi khi tải lên: {str(e)}")
        return False

async def main():
    await client.connect()
    
    # Đăng nhập lần đầu bằng mã OTP
    if not await client.is_user_authorized():
        await client.send_code_request(PHONE_NUMBER)
        try:
            code = input('Nhập mã OTP gửi về máy Telegram của anh: ')
            await client.sign_in(PHONE_NUMBER, code)
        except SessionPasswordNeededError:
            password = input('Nhập mật khẩu 2FA (nếu có): ')
            await client.sign_in(password=password)
            
    print("\n✅ Đăng nhập Telegram User API thành công!")
    print("Sẵn sàng đẩy các file lên tới 2GB (4GB nếu Premium).\n")

    test_file = input("Kéo thả một file video nặng vào đây để test đẩy mây: ").strip().strip("'").strip('"')
    
    if os.path.exists(test_file):
        await upload_video(test_file)
    else:
        print("Không tìm thấy file!")

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
