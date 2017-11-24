from reportlab.pdfgen import canvas
import os
from os.path import join, getsize
import PIL
from PyPDF2 import PdfFileReader, PdfFileWriter



def get_width_height(imagePath):
	im = PIL.Image.open(imagePath)
	return im.width, im.height


def get_list_image_paths(imageDirectory):
	"""
	Returns a list of image paths present in the input directory
	"""
	mypath = imageDirectory

	list_full_names = []
	for root, dirs, files in os.walk(mypath):
		for single_file in files:
			if ".jpg" in single_file:
				full_path = join(root, single_file)
				list_full_names.append(full_path)

	return list_full_names


def create_pdf(imageDirectory, outputPDFName=None):
	"""
	Creates a single PDF from a folder full of images.
	"""
	if outputPDFName is None:
		namePDF = str(imageDirectory) + ".pdf"
	else:
		namePDF = outputPDFName

	# to prevent unnecessary overwrites
	if os.path.exists(namePDF):
		print(os.path.basename(namePDF), " already exists!")
		return


	c = canvas.Canvas(namePDF) #, page0_size)



	for page_path in get_list_image_paths(imageDirectory):
		w, h = get_width_height(page_path)
		c.setPageSize((w,h))
		c.drawImage(page_path, 0, 0)
		c.showPage()


	c.save()

def merge_pdfs(folder_with_pdfs, outputPDFName=None):
	"""
	Merges the *.pdf files into one single .pdf file
	"""
	output = PdfFileWriter()

	if outputPDFName is None:
		outputPDFName = str(folder_with_pdfs) + ".pdf"
	
	mypath = folder_with_pdfs

	for root, dirs, files in os.walk(mypath):
		for single_file in files:
			if ".pdf" in single_file:
				pdfOne = PdfFileReader(open(  join(root,single_file) , "rb"))
				
				for pageIndex in range(0, pdfOne.getNumPages()):
					output.addPage(pdfOne.getPage(pageIndex))

	outputStream = open( join(root, outputPDFName) , "wb")
	output.write(outputStream)
	outputStream.close()

def create_subfolder_pdf(parentFolder):
    for root, dirs, files in os.walk(parentFolder):
        for dir in dirs:
            create_pdf(os.path.join(root, dir))

if __name__ == '__main__':
	pass
