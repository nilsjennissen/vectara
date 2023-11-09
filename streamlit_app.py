# ---------------------------------------------  IMPORT  ------------------------------------------------------------ #
import os
import tempfile
import time

import streamlit as st
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser
from langchain.vectorstores import Vectara

# ----------------------------------------  STREAMLIT SECRETS  ------------------------------------------------------ #
CUSTOMER_ID = st.secrets.VECTARA_CUSTOMER_ID
API_KEY = st.secrets.VECTARA_API_KEY
CORPUS_ID = int(st.secrets.VECTARA_CORPUS_ID)


# ----------------------------------------  VECTARA FUNCTIONS  ------------------------------------------------------ #
def initialize_vectara():
    vectara = Vectara(
        vectara_customer_id=CUSTOMER_ID,
        vectara_corpus_id=CORPUS_ID,
        vectara_api_key=API_KEY
    )
    return vectara


vectara_client = initialize_vectara()

def get_knowledge_content(vectara, query, threshold=0.5):
    found_docs = vectara.similarity_search_with_score(
        query,
        score_threshold=threshold,
    )
    knowledge_content = ""
    for number, (score, doc) in enumerate(found_docs):
        knowledge_content += f"Document {number}: {found_docs[number][0].page_content}\n"
    return knowledge_content


# --------------------------------- -------  PROMPT TEMPLATE   ------------------------------------------------------ #
prompt = PromptTemplate.from_template(
    """You are a professional and friendly Legal Consultant and you are helping a client with a legal issue. The client 
    is asking you for advice on a legal issue. Just explain him in detail the answer and nothing else. This is the 
    issue: {issue} 
    To assist him with his issue, you need to know the following information: {knowledge} 
    """
)


# ---------------------------------------  STREAMLIT INTERFACE  ----------------------------------------------------- #
st.set_page_config(
    page_title="Vectara Legal Search Application",
    page_icon=":card_file_box:",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.title("Legal Consultation Chat")

st.sidebar.subheader("About")

st.sidebar.write("""Welcome to Vectara Legal Search Application! This innovative tool is designed to provide you with 
comprehensive information on the English translation of German commercial law. 
[GERMAN COMMERCIAL LAW](https://www.gesetze-im-internet.de/englisch_bgb/) 
Whether you're a business owner, a legal professional, or simply someone trying to navigate the complexities of a foreign 
legal environment, our application is here to assist you. 

Our legal chat feature is particularly useful when you're unfamiliar with the legal landscape in a new country. It's 
designed to provide you with immediate, accurate, and easy-to-understand information, making the process of understanding 
and complying with German commercial law a breeze.

Please note, however, that while we strive to provide accurate and up-to-date information, the content provided by this 
application can not be considered as legal advice. We strongly recommend consulting with a qualified legal professional 
for any serious legal concerns or decisions. The Vectara Legal Search Application is a tool to aid your understanding, 
but it does not replace professional legal counsel.

Now that we've got that out of the way, let's get started!""")

OPENAI_API_KEY = st.text_input("Enter your OpenAI API KEY")

if OPENAI_API_KEY == "":
    st.warning("Enter your OpenAI API KEY")
else:
    st.success("OpenAI API KEY is set")


    runnable = prompt | ChatOpenAI(streaming=True, callbacks=[StreamingStdOutCallbackHandler()], openai_api_key=OPENAI_API_KEY) | StrOutputParser()

    # -------------------------------------------  CHAT FLOW   --------------------------------------------------------- #
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if user_input := st.chat_input("Enter your issue:"):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        knowledge_content = get_knowledge_content(vectara_client, user_input)
        print("__________________ Start of knowledge content __________________")
        print(knowledge_content)
        response = runnable.invoke({"knowledge": knowledge_content, "issue": user_input})

        response_words = response.split()
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for word in response_words:
                full_response += word + " "
                time.sleep(0.05)
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})

