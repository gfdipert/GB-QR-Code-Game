from django.shortcuts import render
from qrcode.main import QRCode
import urllib
from .forms import QRCode
from .functions import createqrstuff


def qr_code_game_new(request): 
	if request.method == 'POST':
		form = QRCode(data=request.POST)
		if form.is_valid():
			submit(form)
			return render(request, 'qrcodegame/game_edit.html', {'form': form})
	else:
		form=QRCode()
	return render(request, 'qrcodegame/game_edit.html', {'form': form})

def submit(form):
	createqrstuff(form)



