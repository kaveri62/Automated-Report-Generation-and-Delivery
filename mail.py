import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText # Import this for the email body
from email.mime.base import MIMEBase
from email import encoders

# Email details
sender_email = "sender mail id"
receiver_email = "Reciever mail id"
subject = "Replace subject"
body = "Replace body of mail"

# Set up the MIME
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject' ] = subject

# Attach the body (convert string to MIMEText)
msg.attach(MIMEText(body, 'plain'))

# Attach the Excel file
filename = "system_usage.xlsx"
attachment = open(filename, "rb")
part = MIMEBase('application', 'octet-stream')
part.set_payload(attachment.read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', f"attachment; filename={filename}")
msg.attach(part)

# SMTP setup (AWS SES SMTP settings)
smtp_server = "AWS SES SMTP server" 
smtp_port = 587
smtp_user = "Replace with your SMTP username" 
smtp_password = "Replace with your SMTP password" 

# Send the email
try:
server = smtplib. SMTP(smtp_server, smtp_port)
server. starttls()
server. login(smtp_user, smtp_password)
text = msg.as_string()
server. sendmail(sender_email, receiver_email, text)
print("Email sent successfully!")
except Exception as e:
print(f"Error: {e}")
finally:
server.quit()