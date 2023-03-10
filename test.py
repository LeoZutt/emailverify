import smtplib
import dns.resolver

addressToVerify="asdsa.asdsad@rotpunkt-pharma.ch"

domain = "ruegg.ch"
# MX record lookup
records = dns.resolver.resolve(domain, 'MX')
mxRecord = records[0].exchange
mxRecord = str(mxRecord)

# SMTP lib setup
server = smtplib.SMTP()
# uncomment the below line if you want to see full output.
# server.set_debuglevel(1)

# This is just a fake email that doesn't probably exist for smtp.mail(fromAddress)
fromAddress = 'just_a_place_holder@domain.com'

acceptall = "invalid.email.9238381" +"@" +domain
print(acceptall)

# SMTP Conversation
server.connect(mxRecord)
server.helo(server.local_hostname)  ### server.local_hostname(Get local server hostname)
server.mail(fromAddress)
code, message = server.rcpt(str(acceptall))
server.quit()

print("code:", code)
print("message:", message)


# Assume SMTP response 250 is success
if code == 250:
    print('Success')
else:
    print('Bad')