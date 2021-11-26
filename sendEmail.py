import smtplib
import random

#information for using gmal
#port 587 is preferred
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def emailTo(emailAddress, fname, lname):
    #enter your google gmail credentials here for testing. Do not upload them
    port = 587
    password = ""
    username = ""

    sentFrom = username
    to = emailAddress
    subject = "Please click on the following link to activate your account"
    uniqueValue = fname+lname + str(randomValue())
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Activate your account"
    msg['From'] = username
    msg['To'] = to
    text = "Please activate your account."
    html = """\
    <html>
      <head></head>
      <body>
        <p>Hello There<br>
           Click here to activate your account <br>
           <a href="https://www.python.org">%s</a>
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


def randomValue():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=100))
