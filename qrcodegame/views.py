from .forms import QRCode

def qr_code_game_new(request):
    form = QRCode()
    return render(request, 'blog/game_edit.html', {'form': form})