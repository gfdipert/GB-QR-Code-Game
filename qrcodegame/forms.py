from django import forms

class QRCode(forms.Form):
	guide_id = forms.IntField(label="Guide ID", min_length=5)
	page_title = forms.CharField(label="Progress page title")
	phrase = forms.CharField(label="The game phrase.  Use '/' to delimit phrase components, or specify your own with -d.")
	message_title = forms.CharField(label="Message title")
	message = forms.CharField(label="Message to display under the phrase.")
	--completedurl = forms.URLField(label="Customizable Hyperlink text for completed phrase link.",default="Tap Here!",required=False)
