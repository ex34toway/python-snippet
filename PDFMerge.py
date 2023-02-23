#!/usr/bin/env python

from PyPDF2 import PdfWriter, PdfReader  

if __name__ == "__main__":
    filename = "targe.pdf"
    pdfOutput = PdfWriter()
    for i in range(20):
        fi = i + 1
        pdfFile = f"/path/to/your/pdfs/{fi}.pdf"
        pdfInput = PdfReader(open(pdfFile, "rb"))
        numPages = len(pdfInput.pages)
        for i in range(numPages):
            pdfOutput.add_page(pdfInput.pages[i])
    outputStream = open(filename, "wb")
    pdfOutput.write(outputStream)
