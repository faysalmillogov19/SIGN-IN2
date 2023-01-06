from pyhanko import stamp
from pyhanko.pdf_utils import text, images
from pyhanko.pdf_utils.font import opentype
from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter
from pyhanko.sign import signers,fields
from datetime import datetime
from PIL import Image
from io import BytesIO
import base64
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import socket
from parameters.models import Default_parameters
from emailling.models import ServerConfiguration, Protocole



def signature(cert, key, input, pass_phrase, nom_complet, img, position, ttf, url):

	out_file=str(datetime.now().strftime("_%Y_%m_%d_%H_%M_%S"))+str('.pdf')
	out_file='static/uploads/files/'+out_file
	
	signer = signers.SimpleSigner.load(
		key, cert,
		ca_chain_files=(cert,),
		#key_passphrase=pass_phrase
	)

	with open(input, 'rb') as inf:
		w = IncrementalPdfFileWriter(inf)
		fields.append_signature_field(
			w, sig_field_spec=fields.SigFieldSpec(
				str(nom_complet), box=position
			)
	)

		meta = signers.PdfSignatureMetadata(field_name=str(nom_complet))
		pdf_signer = signers.PdfSigner(
			meta, signer=signer, stamp_style=stamp.QRStampStyle(
				# Let's include the URL in the stamp text as well
				stamp_text='Signed by: %(signer)s\nTime: %(ts)s\nURL: %(url)s',
				text_box_style=text.TextBoxStyle(
					font=opentype.GlyphAccumulatorFactory(ttf)
				),
				background=images.PdfImage(img)
			),
		)
		with open(out_file, 'wb') as outf:
			# with QR stamps, the 'url' text parameter is special-cased and mandatory, even if it
			# doesn't occur in the stamp text: this is because the value of the 'url' parameter is
			# also used to render the QR code.
			pdf_signer.sign_pdf(
				w, output=outf,
				appearance_text_params={'url': url}
			)
			
	return out_file

def create_own_signatureImage(img):
	data = Image.open(BytesIO(base64.b64decode(img.replace('data:image/png;base64,', ''))))
	own_signature_name=str(datetime.now().strftime("_%Y_%m_%d_%H_%M_%S"))+str('.png')
	own_signature_name='static/uploads/Signature_sample_images/custom_signature/'+own_signature_name
	data.save(own_signature_name, 'PNG')
	return own_signature_name

def add_text_to_PDF(input, img, output_file_name):
	packet = io.BytesIO()
	can = canvas.Canvas(packet, pagesize=letter)
	can.setFillColorRGB(1, 0, 0)
	can.setFont("Times-Roman", 16)
	position=[9.15, 8.27, 7.435, 6.6, 3.17]
	base=800/12.2
	for i in range(len(input)):
		y=position[i]*base 
		can.drawString(240, y, input[i])

	host_name = socket.gethostname()
	IP_address = socket.gethostbyname(host_name)
	can.drawString(240, 5.73*base, IP_address)

	msg=Default_parameters.objects.first()
	can.drawString(240, 2.32*base, msg.signature_certificat_message)

	config= ServerConfiguration.objects.first()
	can.drawString(240, 4.02*base, config.email)
		
	can.drawImage(img, 240, -460, width=120, preserveAspectRatio=True, mask='auto')
	can.save()
	packet.seek(0)
	new_pdf = PdfFileReader(packet)
	existing_pdf = PdfFileReader(open(msg.signature_certificat_template_url, "rb"))
	output = PdfFileWriter()
	page = existing_pdf.getPage(0)
	page.mergePage(new_pdf.getPage(0))
	output.addPage(page)
	outputStream = open(output_file_name, "wb")
	output.write(outputStream)
	outputStream.close()
	return output_file_name

def uploadFile(file_input, folder, extension):
	name=str(datetime.now().strftime("_%Y_%m_%d_%H_%M_%S"))+str(extension)
	file_name=folder+name
	if not os.path.exists(file_name):
		default_storage.save(file_name, file_input)
	return file_name