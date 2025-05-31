import os
import streamlit as st
import time
import random
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from PyPDF2 import PdfReader
import re
from io import BytesIO

# Streamlit app configuration
st.set_page_config(page_title="PDF Chatbot", page_icon="📄")

# Set up OpenAI API key
if "OPENAI_API_KEY" not in os.environ:
    st.error("Please set the OPENAI_API_KEY environment variable or enter it below.")
    api_key = st.text_input("Enter your OpenAI API Key:", type="password")
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
else:
    api_key = os.environ["OPENAI_API_KEY"]

# Function to extract text from PDF
def extract_pdf_text(pdf_file):
    try:
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        # Clean extracted text
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    except Exception as e:
        return f"Error extracting text: {str(e)}"

# Function to initialize chatbot
def initialize_chatbot(pdf_text):
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
    prompt_template = PromptTemplate(
        input_variables=["context", "question"],
        template="""
        You are a helpful chatbot that answers questions based on the following PDF content:
        {context}
        
        User question: {question}
        
        Provide a clear, concise answer based on the PDF content. If the answer is not in the content, say so.
        """
    )
    chain = RunnableSequence(prompt_template | llm)
    return chain, pdf_text

# Function to ask question with retry logic
def ask_question(chain, pdf_text, question, max_retries=3):
    base_delay = 1
    for attempt in range(max_retries):
        try:
            response = chain.invoke({"context": pdf_text[:4000], "question": question})
            return response.content
        except Exception as e:
            if "429" in str(e):
                delay = (base_delay * 2 ** attempt) + random.uniform(0, 0.1)
                time.sleep(delay)
            else:
                return f"Error: {str(e)}"
    return "Error: Max retries reached due to rate limiting."

# Function to create LaTeX content
def create_latex_content(conversation):
    latex_content = r"""
\documentclass[a4paper,12pt]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage{geometry}
\geometry{margin=1in}
\usepackage{enumitem}
\usepackage{xcolor}
\usepackage{parskip}

\begin{document}

\begin{center}
{\Large \textbf{PDF Chatbot Conversation Report}} \\
\vspace{0.5cm}
{\small Generated on \today}
\end{center}

\section*{Conversation History}
\begin{itemize}[leftmargin=*]
%s
\end{itemize}

\end{document}
"""
    conversation_items = ""
    for q, a in conversation:
        conversation_items += f"\\item \\textbf{{Question:}} {q}\n"
        conversation_items += f"\\item \\textbf{{Answer:}} {a}\n"
    return latex_content % conversation_items

# Streamlit app
def main():
    st.title("PDF Chatbot")
    st.write("Upload a PDF and ask questions about its content. Download the conversation as a LaTeX file.")

    # PDF upload
    pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])
    
    # Initialize session state
    if "pdf_text" not in st.session_state:
        st.session_state.pdf_text = None
    if "chain" not in st.session_state:
        st.session_state.chain = None
    if "conversation" not in st.session_state:
        st.session_state.conversation = []
    
    # Process uploaded PDF
    if pdf_file and st.session_state.pdf_text is None:
        with st.spinner("Extracting text from PDF..."):
            pdf_text = extract_pdf_text(pdf_file)
            if "Error" in pdf_text:
                st.error(pdf_text)
                return
            st.session_state.pdf_text = pdf_text
            st.session_state.chain, _ = initialize_chatbot(pdf_text)
            st.success("PDF processed! You can now ask questions.")

    # Chat interface
    if st.session_state.pdf_text:
        st.subheader("Ask Questions")
        question = st.text_input("Your question:", key="question_input")
        
        if question:
            with st.spinner("Generating response..."):
                answer = ask_question(st.session_state.chain, st.session_state.pdf_text, question)
                if "Error" in answer:
                    st.error(answer)
                else:
                    st.session_state.conversation.append((question, answer))
                    st.write(f"**You**: {question}")
                    st.write(f"**Bot**: {answer}")

        # Display conversation history
        if st.session_state.conversation:
            st.subheader("Conversation History")
            for i, (q, a) in enumerate(st.session_state.conversation, 1):
                st.write(f"**Q{i}**: {q}")
                st.write(f"**A{i}**: {a}")
        
        # Download LaTeX file
        if st.session_state.conversation:
            latex_content = create_latex_content(st.session_state.conversation)
            latex_bytes = BytesIO(latex_content.encode('utf-8'))
            st.download_button(
                label="Download Conversation as LaTeX",
                data=latex_bytes,
                file_name="chatbot_report.tex",
                mime="text/plain"
            )
            st.info("Download the LaTeX file and compile it with `latexmk -pdf chatbot_report.tex` to generate a PDF.")

if __name__ == "__main__":
    main()