import pdfminer
import spacy
import os
import pandas as pd
import re

import pdf2txt

def convert_pdf_to_txt(f):
    output_filename=os.path.basename(os.path.splitext(f)[0]) +".txt"
    output_filepath=os.path.join("output/text/",output_filename)
    pdf2txt.main(args=[f,"--outfile",output_filepath])
    print(output_filepath+" saved successfully")
    return open(output_filepath).read()

nlp = spacy.load("en_core_web_sm")

result={'name':[],'phone':[],'email':[],'skills':[]}
names =[]
phones=[]
emails=[]
skills=[]

def parse_content(text):
    skillset=re.compile("java|python|sql|hadoop")
    phone_num=re.compile("(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})")
    doc=nlp(text)
    name=[entity.text for entity in doc.ents if entity.label_ is "PERSON"][0]
    print(name)
    email= [word for word in doc if word.like_email==True][0]
    print(email)
    phone= str(re.findall(phone_num,text.lower()))
    skill_list= re.findall(skillset,text.lower())
    unique_skills=str(set(skill_list))
    names.append(name)
    phones.append(phone)
    emails.append(email)
    skills.append(unique_skills)
    print("Extraction completed successfully")


for file in os.listdir('resume/'):
    if file.endswith('.pdf'):
        print('Reading ...'+ file)
        txt=convert_pdf_to_txt(os.path.join('resume/' ,file))
        parse_content(txt)

result['name']=names
result['phone']=phones
result['email']=emails
result['skills']=skills

result_df=pd.DataFrame(result)
result_df.to_csv('output/csv/parsed_resumes.csv')