# Política Interna de Liberación

Este documento describe el proceso y los criterios mínimos para la liberación de nuevas versiones del proyecto "Reserva-vuelos".

## Control de Versiones
- Se utiliza versionado tomando valores 0.0.0 =el primero indicando version completa, el segundo cambios mayores y el tercero cambios menores
- Cada versión liberada debe registrarse en el archivo `VERSION.txt`.

## Criterios de Liberación
- Todas las pruebas automáticas y manuales deben pasar exitosamente.
- El código debe ser revisado y aprobado por el desarrollador responsable (único miembro del equipo).
- La validación y firma de liberación se realiza mediante la aprobación del pull request en GitHub.


## Flujo de Liberación
1. Realizar todos los cambios y pruebas en una rama de desarrollo.
2. Crear un pull request hacia la rama principal.
3. Revisar y aprobar el pull request en GitHub (firma digital).
4. Realizar el merge y desplegar la nueva versión.

## Normativas y Buenas Prácticas
- Se siguen buenas prácticas de desarrollo seguro y control de calidad.
- No se aplica una normativa formal (ej. ISO 12207) pero se busca mantener estándares profesionales.
- No se utiliza una licencia de software específica.

## Observaciones
- No hay equipo de QA ni revisores adicionales; el desarrollador es responsable de todo el proceso.
- Se recomienda mantener este documento actualizado y adaptarlo si el equipo crece o cambian los procesos.
