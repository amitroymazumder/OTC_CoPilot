import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText

def send_email(recipients, subject, body="Attached report", attachment=None):
    """
    Send report via email.
    Requires SMTP setup (update with your server).
    """
    SMTP_SERVER = "smtp.yourcompany.com"
    SMTP_PORT = 587
    SMTP_USER = "otc-copilot@yourcompany.com"
    SMTP_PASS = "password"

    msg = MIMEMultipart()
    msg["From"] = SMTP_USER
    msg["To"] = ", ".join(recipients)
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    if attachment:
        with open(attachment, "rb") as f:
            part = MIMEApplication(f.read(), Name=attachment.split("/")[-1])
            part["Content-Disposition"] = f'attachment; filename="{attachment.split("/")[-1]}"'
            msg.attach(part)

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SMTP_USER, SMTP_PASS)
    server.sendmail(SMTP_USER, recipients, msg.as_string())
    server.quit()
    print(f"[OK] Email sent to {recipients}")

def send_slack(webhook_url, message):
    """
    Send notification to Slack via webhook.
    """
    import requests
    response = requests.post(webhook_url, json={"text": message})
    if response.status_code == 200:
        print("[OK] Slack message sent")
    else:
        print("[ERROR] Slack message failed", response.text)
