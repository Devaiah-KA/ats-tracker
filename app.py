from PIL import Image
from dotenv import load_dotenv

load_dotenv()

import streamlit as st 
import os
import io
import base64
import pdf2image
import google.generativeai as genai


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,pdf_content,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text


def inpout_pdf_setup(uploaded_file):
  if uploaded_file is not None:  
    #converting pdf to image
    images=pdf2image.convert_from_bytes(uploaded_file.read())
    
    first_page=images[0]
    
    #convert to bytes
    img_byte_arr=io.BytesIO()
    first_page.save(img_byte_arr,format='JPEG')
    img_byte_arr=img_byte_arr.getvalue()
    
    pdf_parts=[
      {
        "mime_type":"image/jpeg",
        #encoding to base64
         "data":base64.b64encode(img_byte_arr).decode()
      }
    ]
    return pdf_parts
  
  else:
    raise FileNotFoundError("No File Uploded")
      
    
    
 ##Streamlit APP
    
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")

##JOB DESCRIPTION
input_text=st.text_area("Job Description: ",key="input_text")
uploaded_file=st.file_uploader("Upload your resume(PDF) ",type=["pdf"])
   
if uploaded_file is not None:
  st.write("PDF Uploaded Successfully")

submit1=st.button("Tell me About the Resume")

submit2=st.button("How Can I Improvise my Skills") 

submit3=st.button("Percentage match") 

input_prompt1="""
    You are an experienced HR with Tech Experience from the field of any one job role from Data Science or Full Stack Web Development
    or Big Data Engineering or DEVOPS or Data Analyst,and your task is to review the provided resume against the
    job desciption  provided for these profiles.
    Please share  your professional evaluation on whether the candidate's  profile aligns with the role.
    Highlight the strengths and weaknesses of the applicant in relation to th specified job requirements.
"""
  
input_prompt3="""
    You are a skilled ATS(Application Tracking System)scanner with a deep understanding of any one of the job role from Data Science,Full Stack Web Development
    ,Big Data Engineering,DEVOPS,Data Analyst using deep ATS Fuctionality, your task is to evaluate the resume against
    the provided job description.First the output sshould come as percentage and  then keywords missing and last final thoughts.
"""    

#when the button is click what should happen
if submit1:
   if uploaded_file is not None:
     pdf_content=inpout_pdf_setup(uploaded_file)
     response=get_gemini_response(input_prompt1,pdf_content,input_text)
     st.subheader("The Response is")
     st.write(response)
   else:
     st.write("Please Upload Resume")
     
elif submit3:
   if uploaded_file is not None:
     pdf_content=inpout_pdf_setup(uploaded_file)
     response=get_gemini_response(input_prompt3,pdf_content,input_text)
     st.subheader("The Response is")
     st.write(response)
   else:
     st.write("Please Upload Resume")