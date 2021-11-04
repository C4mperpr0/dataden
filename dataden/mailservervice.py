import traceback

def sendmail(server_mail, to_addr, subject, message):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    msg = MIMEMultipart()
    msg['From'] = server_mail['user']
    msg['To'] = to_addr
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))
    text = msg.as_string()

    try:
        server = smtplib.SMTP(server_mail['address'], server_mail['port'])
        server.starttls()
        server.login(server_mail['user'], server_mail['password'])
        server.sendmail(
            server_mail['user'],
            to_addr,
            text
        )
        server.quit()
    except smtplib.SMTPException:
        print(traceback.format_exc())
        return False
    return True


def generate_registermail(username, verification_id):
    s = f'''
    Hello {username},
    to register your Mail at DataDen click on the following link: http://data-den.ddns.net:8080/verify?u={verification_id}
    If you have not registered on our website, ignore this mail and you will be deleted in our system automatically!
    '''
    return s
