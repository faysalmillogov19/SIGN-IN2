from os import listdir
from os.path import isfile, join

class GlobalVar:
	

	def __init__(self):
		self.url_2_base="http://localhost:1000/"
		self.signed_url="http://localhost:1000/"
		self.signataire_url="http://localhost:1000/sign_in/"
		self.signed_alert_message_subject="Soumission de fichier pour signature"
		self.signed_alert_message="Bonjour, je vous espere bien portant. Je viens par cette presente vous soumettre le fichier pour signature."
		self.signed_alert_message_suite=" Ce Fichier est disponible via l'URL ci dessous"
		self.signed_OTP_time_validity=45
		self.signedFile_alert_sending_subject:"Envoi de fichier signe"
		self.signedFile_alert_sending_message="Bonjour, je vous espere bien portant. Je viens par cette presente vous envoyer le fichier apres  signature de toutes les parties."
		self.signed_formule_politesse="Cordialement."
	@classmethod
	def get_default_images(self ): 
		default_signatures_images_folder='static/uploads/Signature_sample_images/' 
		default_signatures_images = [default_signatures_images_folder+f for f in listdir(default_signatures_images_folder) if isfile(join(default_signatures_images_folder, f))]
		return default_signatures_images