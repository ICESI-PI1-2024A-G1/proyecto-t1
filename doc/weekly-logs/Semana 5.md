**Bitácora de la Semana 5 con Metodología Scrum: Desarrollo del Módulo de Contabilidad CCSA**

Roles:

- Scrum Master: Óscar Andrés Gómez
- Product Owner: Óscar Andrés Gómez
- Dev. Team: Alejandro Córdoba Erazo
- Dev. Team: Cristian Eduardo Botina
- Dev. Team: Juan Manuel Marín
- Dev. Team: Óscar Andrés Gómez 

Día 1 - Lunes

Integrantes:

- Cristian Eduardo Botina (A00395008)

1. Qué hice ayer: Implementar la funcionalidad de editar equipos
2. Qué haré hoy:  Discutir aspectos varios sobre la implementación de trazabilidad y su relación con la base de datos implementada en excel
3. Qué dificultades tuve: El modelo relacional propuesto tuvo que ser modificado para adaptarse a los requerimientos iniciales.

- Juan Manuel Marín (A00382037)

1. Qué hice ayer: Revisar las configuraciones de seguridad de acceso a rutas sin estar logueado e implementar tests.
2. Qué haré hoy: Configurar el muestreo de información dependiendo del usuario logueado.
3. Qué dificultades tuve: Ninguna.

- Óscar Andrés Gómez (A00394142)

1. Qué hice ayer: Descartar por completo el uso de servicios en la nube para la base de datos en excel, y empezar la implementación local
2. Qué haré hoy: Usar las librería pandas para controlar el input y el output de requests en el archivo excel
3. Qué dificultades tuve: Ninguna

- Alejandro Córdoba Erazo (A00395678)

1. Qué hice ayer: Nada por falta de tiempo
2. Qué haré hoy: Nada por falta de tiempo
3. Qué dificultades tuve: No tuve tiempo

Día 2 - Martes

Integrantes:

- Cristian Eduardo Botina (A00395008)

1. Qué hice ayer: Resolver dudas sobre el papel de las solicitudes en el modelo de datos
2. Qué haré hoy:  Corregir los errores en el formulario de equipos, ya que este creaba una nueva instancia de las entradas en lugar de editarlas.
3. Qué dificultades tuve: Ninguna

- Juan Manuel Marín (A00382037)

1. Qué hice ayer: Configurar filtro de información según el usuario logueado.
2. Qué haré hoy: Agregar la pantalla 404, incluir al usuario superusuario en el generador de información de prueba y agregar la pantalla de permisos.
3. Qué dificultades tuve: Ninguna.

- Óscar Andrés Gómez (A00394142)

1. Qué hice ayer: Implementación de una api compatible con el modelo de datos viejo.
2. Qué haré hoy: Continuar la implementación de la api, ahora voy a agregar un método para obtener todas las requests y devolverlas como un JsonResponse para que su manejo sea más sencillo.
3. Qué dificultades tuve: ninguna

- Alejandro Córdoba Erazo (A00395678)

1. Qué hice ayer: Nada por falta de tiempo
2. Qué haré hoy: Resolver dudas al equipo sobre la aplicación
3. Qué dificultades tuve: Ninguna

Día 3 - Miércoles

Integrantes:

- Cristian Eduardo Botina (A00395008)

1. Qué hice ayer: Corregir los errores del formulario de editar equipos, cambiar el selector de los miembros por una checkbox en lugar del selector múltiple. 
2. Qué haré hoy:  Implementar las notificaciones por correo electrónico al cambiar el estado y asignar las solicitudes.
3. Qué dificultades tuve: El modelo de solicitudes tuvo que ser eliminado de django para manejar los datos completamente por excel.

- Juan Manuel Marín (A00382037)

1. Qué hice ayer: Agregar pantallas de error y permisos.
2. Qué haré hoy: Implementar la posibilidad de recuperar contraseña.
3. Qué dificultades tuve: Ninguna.

- Óscar Andrés Gómez (A00394142)

1. Qué hice ayer: Implementar una petición get para la api.
2. Qué haré hoy: Implementar la búsqueda por cada componente y la búsqueda por id
3. Qué dificultades tuve: Han habido problemas con el formato de creación de requests por la librería pandas

- Alejandro Córdoba Erazo (A00395678)

1. Qué hice ayer: Resolver dudas al equipo sobre las funcionalidades
2. Qué haré hoy: Obtener y configurar en mi equipo la nueva estructura del proyecto
3. Qué dificultades tuve: Desconocimiento sobre la nueva estructura

Día 4 - Jueves

Integrantes:

- Cristian Eduardo Botina (A00395008)
  
1. Qué hice ayer: Implementar las notificaciones por correo electrónico al cambiar el estado y asignar las solicitudes.
2. Qué haré hoy:  Implementar las pruebas de requests y equipos, corregir errores varios de la api de sharepoint.
3. Qué dificultades tuve: Las sentencias try except arrojaban excepciones inadecuadas que dificultaron la depuración del código.

- Juan Manuel Marín (A00382037)

1. Qué hice ayer: Implementar la opción de recuperar contraseña.
2. Qué haré hoy: Nada.
3. Qué dificultades tuve: Ninguna. 

- Óscar Andrés Gómez (A00394142)

1. Qué hice ayer: Terminar distintos tipos de búsquedas para la api
2. Qué haré hoy: Terminar la implementación y cambiar todas las vistas para que usen la api
3. Qué dificultades tuve: Conflictos entre sistemas operativos por las urls

- Alejandro Córdoba Erazo (A00395678)

1. Qué hice ayer: Obtener y configurar la nueva estructura del proyecto
2. Qué haré hoy: Investigar sobre el admin de django y los permisos ya implementados
3. Qué dificultades tuve: Ninguno

Día 5 - Viernes

Integrantes:

- Cristian Eduardo Botina (A00395008)

1. Qué hice ayer: Implementar las pruebas de requests y equipos, adaptar el generador de datos para que limpie los archivos de excel en cada ejecución.
2. Qué haré hoy:  Revisar las pruebas unitarias de la aplicación de equipos, y adaptarlos para seguir la relación de uno a muchos del modelo actualizado
3. Qué dificultades tuve: El generador de datos generaba conflictos con la relación también, por lo que tuve que adaptarlo igual.

- Juan Manuel Marín (A00382037)

1. Qué hice ayer: Nada.
2. Qué haré hoy: Agregar texto de razón al cambiar el estado de las solicitudes, enviar emails con el cambio y agregar pantalla de contacto por email.
3. Qué dificultades tuve: Crear el nuevo apartado en la tabla de trazabilidad y actualizar la página.

- Óscar Andrés Gómez (A00394142)

1. Qué hice ayer: Terminar la migración de las vistas a usar la api con todos sus tests unitarios
2. Qué haré hoy: Terminar el trabajo de trazabilidad de las solicitudes que había comenzado mi compañero Alejandro
3. Qué dificultades tuve: Era difícil situar una base de datos temporal para testear

- Alejandro Córdoba Erazo (A00395678)

1. Qué hice ayer: Investigar sobre el admin de django y sobre los roles ya implementados
2. Qué haré hoy: Implementar el admin de django, actualizar el modelo de datos y definir el formato para los pull request en el repositorio
3. Qué dificultades tuve: Ninguno

Día 6 - Sábado

Integrantes:

- Cristian Eduardo Botina (A00395008)

1. Qué hice ayer: Corregir errores de los tests de equipos y adaptar las tablas para seguir un diseño responsive.
2. Qué haré hoy:  Nada
3. Qué dificultades tuve: Ninguna

- Juan Manuel Marín (A00382037)

1. Qué hice ayer: Agregar funcionalidad al cambio de solicitudes, enviar notificaciones y agregar pantalla de contacto por email.
2. Qué haré hoy: Avanzar en el reporte del sprint 1.
3. Qué dificultades tuve: Ninguna.

- Óscar Andrés Gómez (A00394142)

1. Qué hice ayer: Finalizar por completo la funcionalidad de trazabilidad de las solicitudes
2. Qué haré hoy: Documentar todo el trabajo realizado para que sea fácil de entender en futuras modificaciones
3. Qué dificultades tuve: ninguna

- Alejandro Córdoba Erazo (A00395678)

1. Qué hice ayer:  Implementar el admin de django, actualizar el modelo de datos y definir el formato para los pull request en el repositorio
2. Qué haré hoy: Terminar el reporte y completar los requerimientos para la entrega
3. Qué dificultades tuve: ninguna

Día 7 - Domingo

Integrantes:

- Cristian Eduardo Botina (A00395008)

1. Qué hice ayer: Nada.
2. Qué haré hoy:  Terminar la documentación de los métodos y tests de equipos.
3. Qué dificultades tuve: Ninguna

- Juan Manuel Marín (A00382037)

1. Qué hice ayer: Avanzar en el reporte final del sprint 1.
2. Qué haré hoy: Nada.
3. Qué dificultades tuve: Nada. 

- Óscar Andrés Gómez (A00394142)

1. Qué hice ayer: Terminar documentación en código para verificar que todo estuviera en orden
2. Qué haré hoy: Revisar cada detalle para tener una entrega de sprint limpia y poder empezar las tareas del sprint 2
3. Qué dificultades tuve: Ninguna

- Alejandro Córdoba Erazo (A00395678)

1. Qué hice ayer:
2. Qué haré hoy:
3. Qué dificultades tuve:

**Sprint Retrospective - Semana 5 con Metodología Scrum**

Aspectos Positivos:

- Comunicación clara: Los integrantes del equipo expresaron de manera concisa qué han hecho, qué harán y si han tenido dificultades.
- Progreso constante: Se observa un avance en las tareas asignadas a lo largo de la semana, especialmente en aspectos como la implementación de funcionalidades y la resolución de problemas.
- Colaboración: Aunque hubo un miembro que no pudo realizar actividades algunos días, se destaca la disposición de resolver dudas y ayudar al equipo cuando es necesario.
- Documentación y pruebas: Se evidencia la importancia dada a la documentación de código y la realización de pruebas unitarias para garantizar la calidad del software.
  
Aspectos a Mejorar:

- Distribución de tareas: Es necesario asegurarse de que todos los miembros del equipo estén involucrados activamente en las actividades del proyecto para evitar situaciones en las que algunos miembros no realicen tareas debido a la falta de tiempo.
- Manejo de excepciones: Algunos integrantes mencionaron dificultades con las excepciones generadas, por lo que sería útil revisar y mejorar la gestión de errores en el código.
- Coordinación de versiones y sistemas: Hasta el momento se tuvieron algunos problemas relacionados con los archivos ignorados o configuraciones de las variables de entorno.

Acciones Propuestas:

- Revisar asignación de tareas: El Scrum Master podría evaluar la carga de trabajo de cada miembro al inicio de la semana y redistribuir tareas si es necesario para evitar situaciones en las que algunos miembros no puedan contribuir.
- Implementar mejores prácticas de manejo de errores: Se puede realizar una revisión detallada del código para identificar y corregir posibles problemas con la gestión de excepciones, asegurando así un comportamiento más robusto del sistema.
- Mejorar el manejo de pull requests: El equipo de desarrollo debería realizar pull requests más relevantes para asegurar que el código**