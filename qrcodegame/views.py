from django.shortcuts import render
from qrcode.main import QRCode
import urllib
from .forms import QRCode
from .functions import createqrcodes
from django.http import HttpResponse
from django.core.files import File


def qr_code_game_new(request): 
	if request.method == 'POST':
		form = QRCode(data=request.POST)
		if form.is_valid():
			return submit(form)
	else:
		form=QRCode()
	return render(request, 'qrcodegame/game_edit.html', {'form': form})

def submit(form):
	zip_file = createqrcodes(form)
	response = HttpResponse(File(file(zip_file,'rb')), content_type='application/zip')
	response['Content-Disposition'] = 'attachment; filename="QRCodes.zip"'
	return response



