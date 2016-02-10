from django import forms

class QRCode(forms.Form):
    
	guide_id = forms.IntegerField(label="Guide ID")
	page_title = forms.CharField(label="Progress page title")
	phrase = forms.CharField(label="The game phrase.  Use '/' to delimit phrase components.")
	message_title = forms.CharField(label="Message title")
	message = forms.CharField(label="Message to display under the phrase")
	completedurl = forms.URLField(label="Turns on form that user can submit information to once qr game is completed.",required=False)
	completedtext = forms.CharField(label="Customizable Hyperlink text for completed phrase link.",required=False)
	storagekey = forms.CharField(label="Storage key",initial='guide__GuideID__')
	html = forms.CharField(label="HTML File Name",initial='qrgame.html')

	def clean(self):
		cleaned_data = super(QRCode, self).clean()
		completedurl = cleaned_data.get('completedurl')
		completedtext = cleaned_data.get('completedtext')
		msg = "shit broke"
		if "maude" not in completedurl:
			 self.add_error('completedurl', msg)