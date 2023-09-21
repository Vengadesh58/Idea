from .. import models, schemas, utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

router = APIRouter(
    prefix="/email", tags=['email']
)


@router.post("/send-email/", status_code=status.HTTP_201_CREATED)
async def send_email(email_request: schemas.EmailRequest):
    try:
        # Email configuration
        # Replace with your SMTP server address
        smtp_server = "vlgspfitcdx.devsys.net.sap"
        smtp_port = 587  # Replace with your SMTP server port
        smtp_username = "your_username"  # Replace with your SMTP username
        smtp_password = "your_password"  # Replace with your SMTP password

        # Create an SMTP connection
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)

        # Create the email message
        msg = MIMEMultipart()
        msg["From"] = smtp_username
        msg["To"] = email_request.to_email
        msg["Subject"] = email_request.subject
        msg.attach(MIMEText(email_request.message, "plain"))

        # Send the email
        server.sendmail(smtp_username, email_request.to_email, msg.as_string())
        server.quit()

        return {"message": "Email sent successfully"}

    except Exception as e:
        return {"message": f"Failed to send email: {str(e)}"}
