Hola buenas, este es el archivo de documentación de la página Actividades DCC, trabajo de Federico Moren.
------------------------------------------------------------------
Si desea probar el código lea la documentación en el archivo "crear_db_juguete.py" en la carpeta "database", se ha creado una pequeña base de juguete para probar las funcionalidades.

Notesé que para ello es necesario tener activa la "venv" del proyecto, para ver los requisitos revise el archivo "requirement.txt".
------------------------------------------------------------------
A continuación se detallan algunas desiciones de diseño al momento de crear la aplicación web:

-Login: aunque no se pedía en primera instancia, me pareció adecuado, y dado que había que registrar al usuario por medio del registro, dar la opción de ingresar a la plataforma una vez registrado.
Esto por supuesto viene con la opción de hacer "logout" desde la navbar implementada en el archivo "base.html".
De hecho, si desea probar más de un usuario basta con crearlo y luego hacer logout para crear otro.

-Registro: dado que se iba a registrar un usuario, y darle la opción de poder volver a ingresar por medio de un login, lo más lógico fue agregar a la base de datos, en la tabla de "Miembro" el atributo "contraseña_hash". Al momento de registrarse se pide crear una contraseña (y confirmarla), esta se convierte mediante el método de hash y es guardada, esto último dado que de no hacerlo, las contraseñas se encontrarían textuales en la base de datos, lo cual es poco seguro.

Además, dado que en la tarea anterior se creo la "categoría" de usuario, y de ser "funcionario" su cargo respectivo, se decidio mantener esta desición de diseño.
Para ello notesé que en la base de datos en el apartado de usuarios se agregaron tales atributos.

-Actividades: similar a lo que ocurría en la tarea 1 con el "SessionStorage", al registrarse apareceel formulario de las actividades. De ese modo, quienes no se encuentren registrados no podrán crear actividades.
Esto resulta ser crucial, ya que en las actividades se usa la información de contacto del usuario registrado.
Además no esta demás decir que se arreglaron los problemas de la primera tarea, ahora es posible agregar más de una imagen y video. Estas luego son guardadas (usando hashlib por seguridad) en la carpeta "uploads".
Además, dado que en el enunciado no se pedía que la "url" o descripción de la actividad fueran obligatorios se decidio dejarlos como opcionales, de todas maneras, si se intenta ingresar alguno de estos dos se verificara que siguen el formato.

-Lista de Usuarios: esta lista ahora se maneja por medio de la base de datos y flask, sin embargo sigue poseyendo los mismos filtros y opciones de orden que en la tarea 1.
En esta entrega, y para resolver el problema de tener que mostrar las actividades del usuario al seleccionar uno de la lista, se decidio hacerlo por medio de un "perfil".
Similar a como pasa en otras plataformas, al hacer "click" en el nombre de un usuario de la lista, se redirije a una nueva página con todas las actividades e información de tal persona.

Es necesario considerar que el archivo de "usuarios.js" posee el código necesario para hacer aparecer el filtro de "cargo" una vez escogida la categoría "funcionario", esto es debido a que de hacerlo con flask esta no aparecía hasta presionar el botón de "buscar". Se intentó otra forma, pero requeria recargar la página y borrar lo escrito en los otros filtros de búsqueda.

-Métricas: dado que aún no sé pide trabajarla con datos como tal, nuevamente se usaron "placeholders" con datos acordes a la información de la página (no con cifras reales sí). Estas son imagenes en formato "png" que se encuentran en la carpeta "svg" para que no ocurran errores con urls como la otra vez.