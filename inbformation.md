# Hướng dẫn Triển khai (Deployment Guide)

## 1. Cấu hình Production (An toàn & Tối ưu)
Hệ thống đã được đóng gói cẩn thận với Docker, sử dụng **Gunicorn** (Production Server) và **WhiteNoise** (Static Files).

### Các file quan trọng:
- `docker-compose.yml`: Chứa cấu hình môi trường (Environment Variables) và Volumes.
- `nginx.conf`: Cấu hình mẫu cho Nginx (Reverse Proxy).
- `Dockerfile`: Đóng gói ứng dụng với thư viện `ffmpeg`.

## 2. Cách chạy ứng dụng
Chạy lệnh sau để build và khởi động:

```bash
docker compose up -d --build
```
Ứng dụng sẽ chạy tại port **8000**.

## 3. Cấu hình Tên miền (y2mate.andyanh.id.vn)
Trong file `docker-compose.yml`, các biến môi trường đã được thiết lập sẵn cho domain của bạn:

```yaml
environment:
  - DEBUG=False
  - ALLOWED_HOSTS=y2mate.andyanh.id.vn,localhost
  - CSRF_TRUSTED_ORIGINS=https://y2mate.andyanh.id.vn
```

## 4. Cấu hình Nginx (Reverse Proxy)
Trên máy chủ (VPS) của bạn, hãy cài đặt Nginx và sử dụng cấu hình trong file `nginx.conf`.
Đảm bảo trỏ domain `y2mate.andyanh.id.vn` về IP của VPS.

## 5. Lưu ý Bảo mật
- **SECRET_KEY**: Trong `docker-compose.yml`, hãy đổi `SECRET_KEY` thành một chuỗi ngẫu nhiên dài và bảo mật.
- **HTTPS**: Nên sử dụng Cloudflare hoặc Let's Encrypt để bật HTTPS cho domain.

## 6. Kiểm tra
Truy cập: `http://localhost:8000` (hoặc domain của bạn sau khi cấu hình DNS).
