from pdf2docx import Converter

# Convert PDF to DOCX
def convert_pdf_to_docx(pdf_path, docx_path):
    cv = Converter(pdf_path)
    cv.convert(docx_path, start=0, end=None)
    cv.close()

# Specify the paths for the PDF and DOCX files
pdf_file = '/Users/chenyimin/PycharmProjects/plugins-quickstart/1995.pdf'  # Replace with the path to your PDF file
docx_file = '/Users/chenyimin/PycharmProjects/plugins-quickstart/1995.docx'  # Replace with the desired output path for the Word document

# Convert the PDF to DOCX
convert_pdf_to_docx(pdf_file, docx_file)
