import smtplib
from email.message import EmailMessage

def send_selection_email(email, name, job_title):
    try:
        msg = EmailMessage()
        msg["Subject"] = f"SmartHireX: Selected for {job_title}"
        msg["From"] = "your_email@example.com"
        msg["To"] = email
        msg.set_content(f"""
        Hi {name},

        Congratulations! 🎉
        You have been shortlisted for the role of {job_title}.

        We will reach out with further details soon.

        Best,
        SmartHireX Team
        """)

        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login("your_email@example.com", "your_app_password")
            smtp.send_message(msg)

        return True
    except Exception as e:
        print(f"Error sending email to {email}: {e}")
        return False

