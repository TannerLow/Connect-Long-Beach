import smtplib
import random

#information for using gmal
#port 587 is preferred
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def get_credentials():
    file = open("email_credentials.txt")
    contents = file.readlines()
    credentials = {"email": "", "password": ""}
    credentials["email"] = contents[0].strip()
    credentials["password"] = contents[1].strip()
    return credentials


def emailTo(emailAddress, code, credentials):
    #enter your google gmail credentials here for testing. Do not upload them
    port = 587
    password = credentials["password"]
    username = credentials["email"]
    sentFrom = username
    to = emailAddress
    subject = "Please click on the following link to activate your account"
    uniqueValue = code
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Activate your account"
    msg['From'] = username
    msg['To'] = to
    text = "Please activate your account."
    html = """\
    <html>
      <head></head>
      <body>
        <p>
            Hello from ConnectLB! Your verification code is <b>%s</b>
        </p>
      </body>
    </html>
    """ % uniqueValue
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    msg.attach(part1)
    msg.attach(part2)

    print(uniqueValue)
    try:
        server = smtplib.SMTP('smtp.gmail.com', port)
        server.starttls()
        server.login(username, password)
        server.sendmail(username, to, msg.as_string())
        server.quit()
    except:
        print('something went wrong')

#generate a random value of 10
def randomValue():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
