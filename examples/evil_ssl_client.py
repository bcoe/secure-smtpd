import smtplib
import time

msg = """From: foo@localhost
To: bar@localhost

Here's my message!
"""
count = 0
while True:
    try:
        count += 1
        if (count % 10) == 0:
            server = smtplib.SMTP('localhost', port=465)
        else:
            server = smtplib.SMTP_SSL('localhost', port=465)
        
        server.set_debuglevel(1)
        server.login('bcoe', 'foobar')
        server.sendmail('foo@localhost', ['bar@localhost'], msg)
        server.quit()
    except Exception as e:
        print(e)
    time.sleep(0.05)
