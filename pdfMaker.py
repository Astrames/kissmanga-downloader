from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import os
from os.path import join, getsize
import PIL
from PIL import ImageDraw
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

def create_canvas(imageDirectory, namePDF, bool_page0):
	"""
	Creates a canvas object, with or without page 0 according 
	to supplied args
	"""
	if bool_page0 is False:
		c = canvas.Canvas(namePDF)
		return c
	else:
		WIDTH = HEIGHT = int( 500 )
		page0_size = (WIDTH, HEIGHT)

		c = canvas.Canvas(namePDF, page0_size)

		# Creating page 000
		white = (255, 255, 255, 255)
		black = (0, 0, 0, 255)

		page0 = PIL.Image.new('RGBA', page0_size, white)

		# Colored Rectangle
		im = ImageDraw.Draw(page0)
		whiteMargin = 20
		blackOutline = 3
		im.rectangle([whiteMargin, whiteMargin, WIDTH - whiteMargin, HEIGHT - whiteMargin], fill=black)
		im.rectangle([whiteMargin + blackOutline, whiteMargin + blackOutline,
		 WIDTH - (whiteMargin + blackOutline), HEIGHT - (whiteMargin + blackOutline)],
		 fill=white)

		im = ImageReader(page0)
		c.drawImage(im, 0 , 0)
		font_size = 37
		c.setFont("Helvetica", font_size)

		if True: # For clarity, ie indentation purposes
			# METHOD 2
			# Not centred perfectly
			title = os.path.basename(imageDirectory)
			n = 12

			correct_title = []
			for i in range(0, len(title), n):
				correct_title.append(title[i:i+n])
			
			textObject = c.beginText( WIDTH/2 - WIDTH/4, HEIGHT/2 )
			
			for line in correct_title:
				textObject.textLine(line)
			c.drawText(textObject)
		c.showPage()

		return c



def create_pdf(imageDirectory, bool_page0, outputPDFName=None):
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


	# c = canvas.Canvas(namePDF) #, page0_size)

	c = create_canvas(imageDirectory, namePDF, bool_page0)


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

	# To get range of PDFs used
	for root, dirs, files in os.walk(mypath):
		D = dirs
		break

	included_pdf = '(' + D[0] + ' - ' + D[-1] + ')'


	outputPDFName = outputPDFName.replace('.pdf',included_pdf+'.pdf')


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
