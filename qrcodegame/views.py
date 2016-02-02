from django.shortcuts import render
from .forms import QRCode


def qr_code_game_new(request):
    form = QRCode()
    return render(request, 'qrcodegame/game_edit.html', {'form': form})