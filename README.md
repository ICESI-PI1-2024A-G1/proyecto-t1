# CCSA - Módulo de Contabilidad

## Integrantes

- Cristian Eduardo Botina (A00395008)
- Juan Manuel Marín (A00382037)
- Óscar Andrés Gómez (A00394142)
- Alejandro Córdoba Erazo (A00395678)

## Introducción

Bienvenido al repositorio del Módulo de Contabilidad del sistema CCSA (Centro Compartido de Servicios Académicos). Este proyecto se enfoca en el desarrollo y gestión de las funciones contables esenciales para la oficina descrita. A continuación, se presenta la documentación detallada del trabajo actual en el módulo.

## Contenido del Repositorio

1. **Product Backlog**
    - Lista completa de historias de usuario con estimaciones realizadas del sprint actual utilizando la metodología de Planning Poker, y criterios de aceptación obtenidos con ayuda del cliente. Toda la organización del product backlog realizó en la plataforma de Jira, para tener un control del desarrollo a través de Scrum.

2. **Modelo de Datos - Diagrama Entidad-Relación**
    - Representación visual de la estructura y relaciones entre las entidades del sistema. Se realizó en la herramienta Datamodeler, y es necesario para comprender la estructura de las bases de datos que utilizará el sistema.

3. **Diagrama de Clases UML**
    - Descripción gráfica de las clases y sus relaciones en el sistema. Se realizó en Visual Paradigm, y es necesario para comprender la estructura de los métodos y clases que utilizará el sistema.

4. **Diagramas de Secuencias**
    - Representación visual de tres procesos clave del módulo, destacando las interacciones entre los componentes. Se realizó en Visual Paradigm y se han desarrollado los siguientes:
    
	    - Actualizar solicitud
	    - Asignar solicitud a un miembro
	    - Crear equipo

5. **Mockups del Módulo**
    - Prototipos visuales de la interfaz de usuario para comprender la apariencia y la navegación del sistema. Se realizaron en Figma y se actualizaron con base a los requerimientos y Feedback del cliente.

6. **Diagrama de Casos de Uso**
    - Descripción detallada de los casos de uso del sistema y las interacciones entre los actores. Se realizó en Visual Paradigm y engloba las historias de usuario desarrolladas en Jira.

7. **Django**
    - Sección dedicada a la implementación en Django, incluyendo el código fuente del módulo. Se incluyó el modulo de Bootstrap por sus funciones y herramientas visuales ofrecidas en html.

8. **Django Auth**
    - Detalles sobre la implementación y gestión de la autenticación en Django. Se desarrolló un inicio de sesión que valida si el usuario existe y si es administrador. De ser así, ingresa a la vista de solicitudes.

9. **Django Vistas**
    - Descripción detallada de las vistas implementadas en Django para el módulo de contabilidad. Hasta el momento, se ha desarrollado la vista de solicitudes, donde aparecen aquellas agregadas hasta la fecha junto a distintos datos en forma de tabla, donde se puede editar el estado actual de cada una.

### Instalación y Ejecución

- Clonar el repositorio `git clone https://github.com/ICESI-PI1-2024A-G1/proyecto-t1.git` y ubicarse en la carpeta `src`.
- Crear el entorno virtual con `py -m venv env`, y activarlo con `.\env\Scripts\activate`. 
- Instalar todas las dependencias necesarias con `pip install -r requirements.txt`
- Añadir el archivo de variables de entorno `.env` a la raíz del repositorio con los valores necesarios (en la entrega de Intu se encuentra un archivo de ejemplo):
	- ADMIN_EMAIL: Contiene el email que será registrado al usuario administrador, este será utilizado para verificarlo al realizar el login
	- ADMIN_PASSWORD: La contraseña que se le asigna al administrador (es un valor arbitrario, al crear el usuario se le asignará esta contraseña)
	- EMAIL_HOST_ADDRESS: Correo electrónico con el que funcionará la verificación en 2 pasos y las notificaciones de la aplicación.
	- EMAIL_HOST_PASSWORD: Contraseña de aplicación, para un correo de Google se puede obtener desde  [Contraseñas de Aplicación](https://myaccount.google.com/apppasswords)
- Realizar todas las migraciones con `py manage.py makemigrations` seguido de `py manage.py migrate`
- Generar los datos de ejemplo con el comando `py generate.py shell`
	- Si no tienes los permisos, abre una consola de PowerShell con permisos de administrador y ejecuta `Set-ExecutionPolicy Unrestricted` y vuelve a intentarlo
- Finalmente, se puede ejecutar el servidor con el comando `py manage.py runserver`

### Tests

Para ejecutar los tests es importante ubicarse en la carpeta `src` y ejecutarlos de la siguiente forma:

```shell
py manage.py test apps.[app-name].tests.[test-name]
```

Las pruebas unitarias disponibles son:
- `apps.requests.tests.tests_requests`
- `apps.requests.tests.tests_sharepoint_api`
- `apps.login.tests.tests_login`
- `apps.registration.tests.tests_registration`
- `apps.teams.tests.tests_teams`


## Contribuciones

Este repositorio está en constante evolución. Se espera que la documentación resulte útil como guía.
