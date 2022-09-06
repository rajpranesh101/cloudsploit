import os
import boto3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

ses_client = boto3.client('ses')

SENDER = "rajpraneshm@clouddestinations.com"
RECEIVER = "rajpraneshm@clouddestinations.com"
CHARSET = "utf-8"
msg = MIMEMultipart('mixed')
msg['Subject'] = "AWS Security Audit"
msg['From'] = SENDER
msg['To'] = RECEIVER

msg_body = MIMEMultipart('alternative')
# text based email body
BODY_TEXT = " "
# HTML based email body
BODY_HTML = "<html><body><h4>Hello Security Team</h4><p>I have attached aws security audit csv file </p></body></html>"
textpart = MIMEText(BODY_TEXT.encode(CHARSET), 'plain', CHARSET)
htmlpart = MIMEText(BODY_HTML.encode(CHARSET), 'html', CHARSET)

msg_body.attach(textpart)
msg_body.attach(htmlpart)


# Full path to the file that will be attached to the email.
ATTACHMENT1 = "file.csv"
#ATTACHMENT2 = "path/to/prospectus_form.pdf"

# Adding attachments
att1 = MIMEApplication(open(ATTACHMENT1, 'rb').read())
att1.add_header('Content-Disposition', 'attachment',
                  filename=os.path.basename(ATTACHMENT1))
'''                  
att2 = MIMEApplication(open(ATTACHMENT1, 'rb').read())
att2.add_header('Content-Disposition', 'attachment',
                  filename=os.path.basename(ATTACHMENT2))
'''
msg.attach(msg_body)
msg.attach(att1)
#msg.attach(att2)

try:
    response = ses_client.send_raw_email(
        Source=SENDER,
        Destinations=[
            RECEIVER
        ],
        RawMessage={
            'Data': msg.as_string(),
        }
    )
    print("Message id : ", response['MessageId'])
    print("Message send successfully!")
except Exception as e:
    print("Error: ", e)
