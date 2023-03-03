import streamlit as st
import quickemailverification

client = quickemailverification.Client('8f92c4dc647d26551a6fbcb23bc1a60a4470d91b39f6af4c63dc8a140c76')
quickemailverification = client.quickemailverification()

def checkEmail(emails):

    for i in emails:
        response = quickemailverification.verify(i)

        status = response.body["safe_to_send"]
        st.write(i +": " + status)

    st.write('Nothing Found... Sorry :(')

st.write("""
## Eric's Email Verifier 
""")

firstName = st.sidebar.text_input("First Name: ")
lastName = st.sidebar.text_input("Last Name: ")
companyWebsite = st.sidebar.text_input("Company Domain: ")

if st.sidebar.button("Sumbit"):
    st.sidebar.success('Submitted')
    st.write('Please Wait...')
    mostCommonEmailsList = []
    mostCommonEmailsList.append(firstName + "." +lastName +"@" + companyWebsite)
    ## Call the function :
    checkEmail(mostCommonEmailsList)

    st.write('\n\n DONE - THANK YOU')
