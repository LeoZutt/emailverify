import quickemailverification
from unidecode import unidecode
import tldextract

client = quickemailverification.Client('53661396b1fc058ab009ef3da01ee6edd06d9cfc33ed9685baf446c5ef9b')
quickemailverification = client.quickemailverification()

def emailFormats(firstName, lastName, domain):

    emails = [

        firstName + "." + lastName + "@" + domain,      #max.muster@muster.ch
        firstName[0] + '.' + lastName + '@' + domain,   #m.muster@muster.ch
        firstName + "_" + lastName + "@" + domain,      #max_muster@muster.ch
        firstName + '@' + domain,                       #max@muster.ch

        lastName + '@' + domain,                        #muster@muster.ch
        firstName[0] + lastName + '@' + domain,         #mmuster@muster.ch
        firstName + lastName[0] + '@' + domain,         #maxm@muster.ch
        firstName[0] + lastName[0] + '@' + domain,      #mm@muster.ch
        lastName + firstName[0] + '@' + domain,         #musterm@muster.ch
        firstName + '-' + lastName + '@' + domain,      #max-muster@muster.ch
        firstName + '.' + lastName[0] + '@' + domain    #max.m@muster.ch
    ]

    return emails

def checkEmail(emails):

    for email in emails:
        response = quickemailverification.verify(email)
        print(response.body)
        status = response.body["safe_to_send"]
        acceptAll = response.body["accept_all"]

        print(status)
        if status == "true":
            print("Email found")
            print(email)
            break
        if acceptAll == "true":
            print("Accept All")
            print(emails[0])
            break


firstName = "leonhard"
lastName = "Ruegg"
domain = "zutt.ch"

domain = tldextract.extract(domain)
domain = domain.domain + "." + domain.suffix

firstName = firstName.lower()
lastName = lastName.lower()

umlautMode = False
umlaute = ['ä','ü','ö']

for umlaut in umlaute:
    if umlaut in firstName:
        umlautMode = True
    if umlaut in lastName:
        umlautMode = True

emails = emailFormats(unidecode(firstName), unidecode(lastName), domain)

quickMode = True

if quickMode == True:
    emails = emails[0:4]

print(emails)

if umlautMode == True:
    vowel_char_map = {ord('ä'): 'ae', ord('ü'): 'ue', ord('ö'): 'oe'}
    firstName = firstName.translate(vowel_char_map)
    lastName = lastName.translate(vowel_char_map)
    print(lastName)
    firstName = unidecode(firstName)
    lastName = unidecode(lastName)
    umlautmails = emailFormats(firstName, lastName, domain)
    if quickMode == True:
        umlautmails = umlautmails[0:4]
    emails.extend(umlautmails)
    umlautMode = False

print(emails)
checkEmail(emails)