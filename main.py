# pip freeze > requirements.txt
import streamlit as st
import smtplib
import dns.resolver
from unidecode import unidecode
import tldextract
import streamlit.components.v1 as components

def emailFormats(firstName, lastName, domain):

    # This function combines the firstName, lastName and the domain
    # to all common email formats

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

def EmailVerify(emails, domain):

    try:
        # MX record lookup
        records = dns.resolver.resolve(domain, 'MX')
        mxRecord = records[0].exchange
        mxRecord = str(mxRecord)

        # This email will be used to "send" an email to the server
        fromAddress = 'just_a_place_holder@domain.com'

        # This email address will be used to check if the server is accept all
        # If this obviously invalid email is accepted, the server is accept all
        acceptall = "invalid.email.9238381" + "@" + domain

        # Connect to the server and verify the email address
        server = smtplib.SMTP()
        server.connect(mxRecord)
        server.helo(server.local_hostname)
        server.mail(fromAddress)


    except:
        emailfound = True
        message = "- Invalid Domain - "
        email = "Invalid Domain"
        return email, str(message), None

    code, message = server.rcpt(str(acceptall))
    emailfound = False

    if code == 250:
        emailfound = True
        message = "- Accept All - "
        server.quit()
        return emails[0], str(message), None

    for email in emails:
        code, message = server.rcpt(str(email))
        if code == 250:
            emailfound = True
            server.quit()
            return email, "Valid Email", str(message)

    if emailfound == False:
        newmessage = "- No Valid Email Found -"
        server.quit()
        return emails[0], newmessage, str(message)

# Set the interface of the webapp
st.write("""## Email Verifier """)

col1, col2, col3 = st.columns(3)
with col1:
    firstName = st.text_input("First Name: ",
                              help="Also accepts Email-Address or First- and Lastname with space in between")
with col2:
    lastName = st.text_input(label="Last Name: ")
with col3:
    domain = st.text_input("Domain: ")

emailonly = st.checkbox('Email Format Only', value=False, help="Only constructs the email address without verifying it.")

# Set the button and start all the functions when clicked
if st.button("Submit", use_container_width=True, type="primary"):

    error = False

    if len(firstName)<1:
        st.error("First Name Missing")
        error = True

    if len(lastName)<1:
        st.error("Last Name Missing")
        error = True

    if len(domain)<1:
        st.error("Domain Missing")
        error = True


    if error == False:

        # Extract the domain from webaddress
        domain = tldextract.extract(domain)
        domain = domain.domain + "." + domain.suffix

        # Split first and lastName if both have been copied into firstName field
        if " " in firstName:
            namesplit = firstName.split()
            firstName = namesplit[0]
            lastName = namesplit[1]

        firstName = firstName.lower()
        lastName = lastName.lower()

        # If a mail address is copied into the firstName field, verify this address
        # If not, generate the different email formats and verify those
        if "@" in firstName:
            emails = [firstName]
            domain = tldextract.extract(firstName)
            domain = domain.domain + "." + domain.suffix
        else:
            emails = emailFormats(unidecode(firstName), unidecode(lastName), domain)

        # Check for Umlaute
        umlautMode = False
        umlaute = ['ä', 'ü', 'ö']
        umlautName = firstName + lastName

        for umlaut in umlaute:
            if umlaut in umlautName:
                umlautMode = True

        # If and Umlaut is detected, both email format variants are generated and verified
        # Eg. leonhard.ruegg@zutt.ch and also leonhard.rueegg@zutt.ch and so forth
        if umlautMode == True:
            vowel_char_map = {ord('ä'): 'ae', ord('ü'): 'ue', ord('ö'): 'oe'}
            firstName = firstName.translate(vowel_char_map)
            lastName = lastName.translate(vowel_char_map)
            firstName = unidecode(firstName)
            lastName = unidecode(lastName)
            umlautmails = emailFormats(firstName, lastName, domain)
            emails = umlautmails + emails
            umlautMode = False

        # Verify the emails
        if emailonly == False:
            email, message, help = EmailVerify(emails, domain)
        else:
            email = emails[0]
            message = "Email Format Only"
            help = None

        # Display the valid email
        with st.container():
            st.metric(label="", value=email, delta=message, help=help)

# Allow the enter button to be used for submit
components.html(
    """
<script>
const doc = window.parent.document;
buttons = Array.from(doc.querySelectorAll('button[kind=primary]'));
const submit_button = buttons.find(el => el.innerText === 'Submit');
doc.addEventListener('keydown', function(e) {
    switch (e.keyCode) {
        case 13: // (13 = enter)
            submit_button.click();
            break;

    }
});
</script>
""",
    height=0,
    width=0,
)