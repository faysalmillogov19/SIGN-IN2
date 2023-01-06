from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def add_text_to_PDF(input, img, output_file_name):
	packet = io.BytesIO()
	can = canvas.Canvas(packet, pagesize=letter)
	can.setFillColorRGB(1, 0, 0)
	can.setFont("Times-Roman", 16)
	position=[9.15, 8.27, 7.435, 6.6, 5.73, 4.87, 4.02, 3.17, 2.32]
	base=800/12.2
	for i in range(len(input)):
		y=position[i]*base 
		can.drawString(240, y, input[i])
		
	can.drawImage(img, 240, -460, width=120, preserveAspectRatio=True, mask='auto')
	can.save()
	packet.seek(0)
	new_pdf = PdfFileReader(packet)
	existing_pdf = PdfFileReader(open("Certificat_signature_template.pdf", "rb"))
	output = PdfFileWriter()
	page = existing_pdf.getPage(0)
	page.mergePage(new_pdf.getPage(0))
	output.addPage(page)
	outputStream = open(output_file_name, "wb")
	output.write(outputStream)
	outputStream.close()
	return output_file_name
	
p=add_text_to_PDF(["identifiant", "nom", "email", "telephone", "ip", "client", "de", "a", "message"], "car.jpg", "output_file_name.pdf" )
print(p)
	
	
	


