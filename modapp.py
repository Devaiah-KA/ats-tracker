import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

load_dotenv() ## load all our environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_repsonse(input,jd,text):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([input,jd,text])
    return response.text

def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text



## streamlit app
st.title("Smart ATS")
st.text("Improve Your Resume ATS")
jd=st.text_area("Paste the Job Description")
uploaded_file=st.file_uploader("Upload Your Resume",type="pdf",help="Please upload the pdf")

submit1 = st.button("Tell me About the Resume")

submit2=st.button("Keywords Missing")

submit3=st.button("percentage match")

       
#Prompt Template

input_prompt1="""
You are an experienced HR with Tech Experience from the field of any one job role from Data Science or Full Stack Web Development
    or Big Data Engineering or DEVOPS or Data Analyst,and your task is to review the provided resume against the
    job desciption only , provided for these profiles.
    Please share your professional evaluation on whether the candidate's  profile aligns with the role in the job description.
    Highlight the strengths and weaknesses of the applicant in relation to the specified job description given.
"""

input_prompt2="""
 You are a skilled ATS(Application Tracking System)scanner with a deep understanding of any one of the job role from Data Science,Full Stack Web Development
,Big Data Engineering,DEVOPS,Data Analyst using deep ATS Fuctionality, your task is to evaluate the resume against
    the provided job description.First the output should come as percentage and then keywords missing for the job description and then  last final thoughts.
"""

input_prompt3="""
You are a skilled ATS(Application Tracking System)scanner with a deep understanding of any one of the job role from Data Science,Full Stack Web Development
,Big Data Engineering,DEVOPS,Data Analyst using deep ATS Fuctionality, your task is to evaluate the resume against
    the provided job description. The output should come as percentage,comparing how the resume fits the job description with the keywords that matched with 
    the resume in yellow highlighted text. 
"""

if submit1:
    if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        response=get_gemini_repsonse(input_prompt1,jd,text)
        st.subheader(response)
        
elif submit2:
     if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        response=get_gemini_repsonse(input_prompt2,jd,text)
        st.subheader(response)
        
elif submit3:
     if uploaded_file is not None:
         text=input_pdf_text(uploaded_file)
         response=get_gemini_repsonse(input_prompt3,jd,text)
         st.subheader(response)
         
else:
    st.write("Please upload pdf")