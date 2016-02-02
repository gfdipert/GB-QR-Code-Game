from django import forms

class QRCode(forms.Form):
	guide_id = forms.IntegerField(label="Guide ID")
	page_title = forms.CharField(label="Progress page title")
	phrase = forms.CharField(label="The game phrase.  Use '/' to delimit phrase components.")
	message_title = forms.CharField(label="Message title")
	message = forms.CharField(label="Message to display under the phrase.")
	completedurl = forms.URLField(label="Customizable Hyperlink text for completed phrase link.",required=False)
