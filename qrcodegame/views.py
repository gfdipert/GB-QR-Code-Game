from django.shortcuts import render
from qrcode.main import QRCode
import urllib
from .forms import QRCode


def qr_code_game_new(request):
    form = QRCode()
    if form.is_valid():
    	return render(request, 'qrcodegame/game_edit.html', {'form': form})
    else:
    	form=QRCode()
    return render(request, 'qrcodegame/game_edit.html', {'form': form})

def submit(request):
	#grab values from form
	guideid = request.POST.get('guide_id')
	pagetitle = request.POST.get('page_title')
	phrase = request.POST.get('phrase')
	messagetitle = request.POST.get('message_title')
	message = request.POST.get('message')
	completedurl = request.POST.get('completedurl')
	completedtext = request.POST.get('completedtext')

	storagekey = request.POST.get('storagekey')
	if storagekey is None:
		storagekey = 'guide__' + guideid + '__'
	html = request.POST.get('html')
	if html is None:
		html = 'qrgame.html'



