from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
# import spacy
import PyPDF2

# nlp = spacy.load("en_core_web_sm")

def index(request):
    template = loader.get_template('first.html')
    return HttpResponse(template.render({}, request))

def annotate(request):
    x = request.POST['text']
    # doc = nlp(x)
    # html = spacy.displacy.render(doc, style='ent')
    d = {}
    # for ent in doc.ents:
    #     if ent.label_ in d.keys():
    #         d[ent.label_].append(ent.text)
    #     else:
    #         d[ent.label_] = [ent.text]
    # with open('taggingapp/static/data.json', 'w+') as datas:
    #     datas.write(str(d))
    template = loader.get_template('second.html')
    context = {
        'text': x,
        # 'dict': d,
    }
    return HttpResponse(template.render(context, request))

import os
import PyPDF2
import tempfile

def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    num_pages = len(pdf_reader.pages)
    text = ""

    for i in range(num_pages):
        page = pdf_reader.pages[i]
        text += page.extract_text()

    return text

def annotateusingupload(request):
    uploaded_file = request.FILES['file']
    file_name = uploaded_file.name
    
    if file_name.endswith('.txt'):
        # Handle text file
        text = uploaded_file.read().decode('utf-8')
    elif file_name.endswith('.pdf'):
        # Handle PDF file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(uploaded_file.read())
            temp_file_path = temp_file.name
        text = extract_text_from_pdf(temp_file_path)
        # Clean up the temporary file
        if temp_file_path:
            os.unlink(temp_file_path)
    else:
        # Invalid file type
        return HttpResponse("Unsupported file format.")

    new_string = text.replace("\n", "<br/>")

    template = loader.get_template('second.html')
    context = {
        'text': new_string,
    }

    return HttpResponse(template.render(context, request))


def help(request):
    template = loader.get_template('help.html')
    return HttpResponse(template.render({}, request))