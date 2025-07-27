# BTC/USDT Tracker Installation Guide

## Prerequisites
- Python 3.8+
- Ubuntu 20.04+ (for systemd service)
- Finnhub API key (free tier available)
- SMTP credentials (Gmail or other email provider)

## Installation Steps

1. **Clone the repository**
```bash
git clone https://github.com/your-repo/btc_tracker.git
cd btc_tracker
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables**
Copy the example environment file and fill in your credentials:
```bash
cp .env.example .env
nano .env
```

Example `.env` content:
```
FINNHUB_API_KEY=your_api_key_here
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password  # Use app-specific password for Gmail
ALERT_EMAIL=alert_receiver@example.com
```

4. **Test the application**
```bash
python btc_tracker.py
```

5. **Set up systemd service (Ubuntu)**
```bash
sudo nano /etc/systemd/system/btc_tracker.service
```

Paste the following content, replacing `/path/to/btc_tracker` with the actual path:
```ini
[Unit]
Description=BTC/USDT Tracker Service
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/path/to/btc_tracker
ExecStart=/usr/bin/python3 /path/to/btc_tracker/btc_tracker.py
Restart=always
RestartSec=5
Environment="PATH=/usr/bin:/bin"
EnvironmentFile=/path/to/btc_tracker/.env

[Install]
WantedBy=multi-user.target
```

6. **Enable and start the service**
```bash
sudo systemctl daemon-reload
sudo systemctl enable btc_tracker
sudo systemctl start btc_tracker
```

7. **Check service status**
```bash
sudo systemctl status btc_tracker
```

## Monitoring
- View logs: `journalctl -u btc_tracker -f`
- Check log file: `tail -f btc_tracker.log`

## Customization
- Adjust signal detection logic in `btc_tracker.py`
- Modify email templates in `notification.py`
- Change check interval in `btc_tracker.py` (schedule.every(55).seconds)
