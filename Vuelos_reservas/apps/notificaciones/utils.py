from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
#CORONA GARCIA CHRISTIAN JAVIER
def enviar_confirmacion_reserva(reserva, usuario_email=None):
    """
    Envía un correo de confirmación de reserva usando una plantilla HTML.
    Args:
        reserva: Instancia de la reserva creada.
        usuario_email: Email del usuario (opcional, si no está en reserva).
    """
    email_destino = usuario_email or getattr(reserva, 'email', None) or getattr(reserva.usuario, 'email', None)
    if not email_destino:
        return False  # No hay email para enviar

    asunto = f"Confirmación de reserva #{reserva.id} - Vuelo {reserva.vuelo.numero_vuelo}"
    # Buscar asiento del pasajero principal (usuario)
    asiento = None
    try:
        from apps.reservas.models import Pasajero
        pasajero = Pasajero.objects.filter(reserva=reserva, email=reserva.usuario.email).first()
        if pasajero:
            asiento = pasajero.asiento
    except Exception:
        pass
    contexto = {
        'reserva': reserva,
        'vuelo': reserva.vuelo,
        'asiento': asiento,
        'usuario': getattr(reserva, 'usuario', None),
        'precio': reserva.precio_total,
    }
    mensaje_html = render_to_string('emails/confirmacion_reserva.html', contexto)
    from email.mime.image import MIMEImage
    import os
    logo_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'Logo.png')
    email = EmailMessage(
        asunto,
        mensaje_html,
        settings.EMAIL_HOST_USER,
        [email_destino],
    )
    email.content_subtype = 'html'
    try:
        with open(logo_path, 'rb') as f:
            logo = MIMEImage(f.read())
            logo.add_header('Content-ID', '<logo_vueloreserva>')
            logo.add_header('Content-Disposition', 'inline', filename='Logo.png')
            email.attach(logo)
    except Exception as e:
        print(f"[NOTIFICACION] No se pudo adjuntar logo: {e}")
    email.send(fail_silently=False)
    return True
