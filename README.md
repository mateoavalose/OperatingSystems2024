# Final Sistemas Operativos 2024-2
**1. ¿Por qué un programador usaría WSL en lugar de Windows puro para el desarrollo de un proyecto?**

Windows Subsystem for Linux (WSL) permite ejecutar un entorno de Linux directamente en Windows sin necesidad de instalar una máquina virtual o hacer un dual-boot (de forma nativa). Esto permite una integración rápida con muchos entornos de desarrollo que están diseñados para sistemas Linux. Con WSL, se pueden usar herramientas y scripts de Linux que no están disponibles en Windows, facilitando la gestión de paquetes, el uso de scripts de Bash, y el desarrollo web en entornos similares a los de los servidores de producción, que normalmente usan Linux.

---

**2. ¿Cómo explicaría la diferencia entre Git y GitHub?**

Git es un sistema de control de versiones distribuido que permite a los desarrolladores realizar un seguimiento de los cambios en el código y colaborar en el desarrollo de software. Git almacena la historia de los cambios localmente y permite la creación de ramas para experimentar sin afectar la versión principal.

GitHub, en cambio, es una plataforma en la nube que utiliza Git para almacenar repositorios de código de manera centralizada y facilitar la colaboración. Además de ofrecer almacenamiento, GitHub proporciona herramientas adicionales para revisar el código, gestionar proyectos y colaborar de forma pública o privada.

---

**3. ¿Por qué es importante el uso de Git en un proyecto de desarrollo? Por ejemplo, en la creación de una página web.**

Git permite llevar un control preciso de las versiones del código, lo que facilita identificar y revertir cambios en caso de errores. En el desarrollo de una página web, Git facilita la colaboración de varios desarrolladores sin que interfieran en el trabajo de los demás y permite el trabajo en paralelo con el uso de ramas, que son útiles para desarrollar nuevas características sin afectar la versión en producción.

---

**4. Según lo aprendido a lo largo de la materia ¿En qué situaciones usaría Bash y no un lenguaje de programación como Python o Java?**

Bash es ideal para tareas de administración de sistemas y automatización de comandos repetitivos que deban interactuar directamente con el sistema operativo, como la gestión de archivos, la manipulación de directorios, la instalación de paquetes y la ejecución de scripts. Por ejemplo, Bash es preferible cuando se necesita ejecutar secuencias simples de comandos del sistema, mientras que Python o Java son más apropiados para desarrollos complejos o donde se requiera una lógica de programación más avanzada y el uso de librerías.

---

**5. Digamos que usted será uno de los desarrolladores de un proyecto de software y tendrá la tarea de crear una instancia de EC2 que será usada como servidor ¿Cuál sistema operativo elegiría usted y por qué?**

Para un servidor de desarrollo en EC2, elegiría un sistema operativo como Amazon Linux o Ubuntu. Estos sistemas son ampliamente compatibles con las herramientas de desarrollo y administración de servidores, son ligeros en cuanto a consumo de recursos, y cuentan con buena documentación y soporte. Amazon Linux, además, está optimizado para trabajar en AWS, por lo que podría ofrecer un mejor rendimiento en la infraestructura de Amazon.

---

**6. ¿Cuál es el servicio de AWS que más interés le generó? Explique su respuesta.**

Uno de los servicios más interesantes prar mí es Amazon Lambda. Este servicio permite ejecutar código sin la necesidad de gestionar servidores (serverless). Esto facilita el desarrollo de aplicaciones de forma escalable y económica, ya que se paga solo por la cantidad de ejecución en lugar de por un servidor completo (tiempos de milisegundos). Lambda es ideal para tareas automatizadas y microservicios sin la necesidad de gestionar un servidor completo.

---

**7. ¿En qué le gustaría profundizar más en AWS? Explique su respuesta.**

Me gustaría profundizar en Amazon RDS, el servicio de bases de datos relacionales de AWS. Actualmente sé cómo gestionar bases de datos localmente y en docker, pero me gustaría entender cómo gestionar una base de datos en nube con un servicio especializado en eso. Además, creo que podría estar mejor optimizado para un deployment que el uso de docker para la base de datos corriendo en la instancia de EC2. 

---

**8. ¿Para qué sirve FastAPI? En el contexto de un proyecto ¿Para qué lo usaría?**

FastAPI es un framework de Python para construir APIs de manera rápida y eficiente, y soporta las especificaciones OpenAPI y JSON Schema, lo que facilita la validación automática y la documentación de endpoints. En un proyecto, yo lo usaría para desarrollar APIs RESTful, especialmente en situaciones en las que se necesita un alto rendimiento y facilidad de implementación, como en microservicios o aplicaciones que requieren una API backend para interactuar con el frontend. Lo más importante para mí es la rapidez en la que se puede realizar el deploy de una API utilizando FastAPI.

---

**9. Explique dos formas de publicar la URL de un endpoint.**

1. **Implementación en un servidor en la nube:** Se puede desplegar la aplicación en un servidor en la nube (como una instancia de EC2 en AWS), asociar una IP pública y configurar el puerto para que sea accesible desde internet. Con un nombre de dominio, se puede hacer que el endpoint sea más accesible.

2. **Plataformas de hosting de APIs (Ngrok):** Servicios como Ngrok, Vercel o Netlify permiten desplegar aplicaciones web y APIs, además ofrecen un dominio público automáticamente. Esto facilita el despliegue rápido sin necesidad de gestionar el servidor desde cero.

---

**10. ¿Qué es un daemon? ¿Por qué se debería crear un archivo .service?**

Un daemon es un programa que se ejecuta en segundo plano y responde a eventos o realiza tareas programadas. Un archivo `.service` en Linux define un servicio gestionado por `systemd`, especificando cómo iniciar, detener y reiniciar el daemon. Esto es útil para que el sistema operativo inicie automáticamente el daemon en el arranque y lo mantenga en ejecución, facilitando la gestión y monitoreo de servicios importantes.

---

**11. Investigue qué es un cron y crontab en Bash. Muestre un ejemplo sobre su máquina local.**

`cron` es un servicio en sistemas Unix y Linux que permite programar la ejecución automática de tareas o comandos a intervalos regulares, como cada minuto, día, semana o mes. Este sistema es útil para automatizar procesos como copias de seguridad, limpiezas de archivos temporales o actualizaciones periódicas. 

`crontab` es el archivo o lista donde se almacenan las tareas programadas de cada usuario y especifica el calendario de ejecución para cada tarea. Mediante el comando `crontab`, los usuarios pueden agregar, editar o eliminar tareas en su archivo de tareas programadas.

### Sintaxis de `crontab`

Cada línea en el archivo `crontab` sigue esta estructura:
```plaintext
# Minuto (0-59) Hora (0-23) Día (1-31) Mes (1-12) Día de la semana (0-7) Comando
```
Por ejemplo:
```plaintext
30 2 * * 1 /home/user/script.sh
```
Esta línea ejecuta el script `script.sh` cada lunes a las 2:30 AM.

### Ejecución Inicial

Al iniciar por primera vez el comando `crontab -e` e iniciar nano, aparece el siguiente archivo:
```vim
# Edit this file to introduce tasks to be run by cron.
#
# Each task to run has to be defined through a single line
# indicating with different fields when the task will be run
# and what command to run for the task
#
# To define the time you can provide concrete values for
# minute (m), hour (h), day of month (dom), month (mon),
# and day of week (dow) or use '*' in these fields (for 'any').
#
# Notice that tasks will be started based on the cron's system
# daemon's notion of time and timezones.
#
# Output of the crontab jobs (including errors) is sent through
# email to the user the crontab file belongs to (unless redirected).
#
# For example, you can run a backup of all your user accounts
# at 5 a.m every week with:
# 0 5 * * 1 tar -zcf /var/backups/home.tgz /home/
#
# For more information see the manual pages of crontab(5) and cron(8)
#
# m h  dom mon dow   command
```

### Ejemplo en máquina local

1. Se el archivo `crontab` para editar las tareas programadas:
   ```bash
   crontab -e
   ```

2. Se añade una línea para ejecutar un comando. Por ejemplo, para crear una copia de un archivo cada día a las 6:00 AM:
   ```bash
   0 6 * * * cp /home/mateo/archivo.txt /home/mateo/backup/archivo_$(date +\%F).txt
   ```

### Verificar las tareas programadas

Para ver las tareas programadas en el `crontab`, se ejecuta:
```bash
crontab -l
```

Esta funcionalidad permite realizar tareas repetitivas y de mantenimiento en el sistema sin intervención manual.
El `crontab` quedó de la siguiente forma:

```vim
# Edit this file to introduce tasks to be run by cron.
#
# Each task to run has to be defined through a single line
# indicating with different fields when the task will be run
# and what command to run for the task
#
# To define the time you can provide concrete values for
# minute (m), hour (h), day of month (dom), month (mon),
# and day of week (dow) or use '*' in these fields (for 'any').
#
# Notice that tasks will be started based on the cron's system
# daemon's notion of time and timezones.
#
# Output of the crontab jobs (including errors) is sent through
# email to the user the crontab file belongs to (unless redirected).
#
# For example, you can run a backup of all your user accounts
# at 5 a.m every week with:
# 0 5 * * 1 tar -zcf /var/backups/home.tgz /home/
#
# For more information see the manual pages of crontab(5) and cron(8)
#
# m h  dom mon dow   command
0 6 * * * cp /home/mateo/archivo.txt /home/mateo/backup/archivo_$(date +\%F).txt
```