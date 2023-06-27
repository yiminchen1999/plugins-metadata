import os
import docx
import pandas as pd
import PyPDF2
from datasets import Dataset


def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        text = ""
        for page in range(num_pages):
            text += reader.pages[page].extract_text()
    return text



import pandas as pd

def create_dataset(pdf_path):
    text = extract_text_from_pdf(pdf_path)

    # Parse the text and extract the information
    # Implement your own logic here based on the structure of your PDF

    # Example implementation assuming the information is separated by newlines
    lines = text.split('\n')
    data = []
    for line in lines:
        # Extract the desired fields from each line
        # Implement your own logic here based on the structure of your PDF
        id = ...
        url = ...
        title = ...
        paper_text = ...
        data.append([str(id), str(url), str(title), str(paper_text)])  # Convert id, url, and title to strings

    # Create the dataset
    dataset = pd.DataFrame(data, columns=['id', 'url', 'title', 'text'])
    return dataset




def save_dataset(dataset, output_path):
    dataset = Dataset.from_pandas(dataset)
    dataset.save_to_disk(output_path)

pdf_path = '1995.pdf'
output_path = "/1995papers_output"
dataset = create_dataset(pdf_path)
save_dataset(dataset, output_path)


