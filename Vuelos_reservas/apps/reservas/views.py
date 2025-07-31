from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Reserva
#CORONA GARCIA CHRISTIAN JAVIER
@login_required
def mis_reservas(request):
    reservas = Reserva.objects.filter(usuario=request.user).select_related('vuelo')
    return render(request, 'reservas/mis_reservas.html', {'reservas': reservas})
