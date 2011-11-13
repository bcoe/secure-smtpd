import smtplib

msg = """From: foo@localhost
To: bar@localhost

Here's my message!
"""

server = smtplib.SMTP_SSL('localhost', port=465)
server.set_debuglevel(1)
server.login('foo', 'bar')
server.sendmail('foo@localhost', ['bar@localhost'], msg)
server.quit()