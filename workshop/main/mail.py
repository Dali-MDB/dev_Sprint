import smtplib


# Email configuration
sender_email = "travelagencyt36@gmail.com"
receiver_email = "khalilwadjih1@gmail.com"
password = "rode twmm lyyn fnmq"  
subject = "Test Email from Python"
body = "This is a test email sent from Python."


text = f'Subject: {subject}\n\n{body}'


server = smtplib.SMTP("smtp.gmail.com",587)
server.starttls()
server.login(sender_email,password)
server.sendmail(sender_email,receiver_email,text)
print("Email sent successfully!")