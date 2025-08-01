#!/usr/bin/env python
import os
import sys
#CORONA GARCIA CHRISTIAN JAVIER
def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "No se pudo importar Django. ¿Está instalado y disponible en tu entorno virtual?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
