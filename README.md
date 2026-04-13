Hola buenas, este es el archivo de documentación de la página Actividades DCC, trabajo de Federico Moren.

A continuación se hablarán de manera acotada algunas desiciones del diseño de la aplicación:

-Inicio: 
Se optó por algo simplista y funcional, posee un botón para cada una de las páginas a las que se puede llegar. Se creo un SessionStorage para simular la existencia de un servidor, esto se uso en este caso para indicar al usuario, de no haberse registrado, que lo haga para poder subir alguna actividad. De hacerlo y volver a la página de inicio se saluda con el nombre ingresado para dar más personalización.

-Página Registro: 
Lo más notable a decir es la creación del SessionStorage una vez registrado el usuario, lo cual luego se usará en otras partes de la página.
Se optó por dar a los "funcionarios", un tipo de usuario, la capacidad de escoger el cargo al que pertenecen con el fin de diferenciarlos mejor entre ellos. Una vez este aparece como elección es necesaria para continuar.
Notesé que una vez registrado se limpia el formulario y se le deja al usuario en la página. En un inicio pensé en guiarlo directamente a la página de inicio, pero dado que se trata de un prototipo, de equivocarse al ingresar datos se puede sobreescribir el usuario directamente desde la página (lo que hace más fácil probar el código), o ir con el botón indicado a las actividades ó lista de usuarios.

-Publicar actividades:
Se optó por dejar en una misma página el ingreso de información para crear una actividad como la lista de actividades, esto por la comodidad que ofrece. Con comodidad me refiero a poder ver en tiempo real que se ha creado correctamente lo que se ingreso. Además si bien hasta el momento se estaba haciendo un SessionStorage por cuestión de tiempo no se pudo aplicar a esta página, lo que provoca que se deshaga la actividad una vez se recarge la página.
Donde si se uso esta funcionalidad fue en la aparición del form para crear actividades, este solo esta disponible si alguien se ha registrado con anterioridad, lo que evita que usuarios no registrados creen actividades sin los datos necesarios. Esto último debido a que la actividad usa la información de contacto y nombre del usuario.
Las imágenes y videos se puedes ver una vez estan subidos en la sección de actividad de cada tarjeta.

-Lista Usuarios:
La lista muestra 4 usuarios a la vez, se podría hacer de un poco más por la cómodidad que otorga ver más resultados sin tener que presionar un botón, sin embargo se decidió ese número debido a la ausencia de un servidor y base de datos que justifique este cambio.
Si el usuario se ha registrado este aparecerá en la lista (un poco como pasa en Ucursos), esto es más que nada por si se busca gente con gmail, nombre o apellido similar a uno, o que compartan el tipo de usuario (no muy útil, pero interesante de aplicar).
Notesé que al igual que pasa en la página de registro, escoger la opción de filtro de "funcionarios" habilita el filtro por "cargo", lo que viene siendo útil y acorde al filtro anterior.

-Métricas:
Las métricas en este caso vienen a ser un tipo de placeholder, debido a que no se tenían muchos datos debido a la naturaleza del prototipo, se "crearon" datos para los gráficos, intentando mantenerse fiel a lo visto en la página y entre ellos.
Estos fueron hechos con una página externa (https://quickchart.io/documentation/chart-types/) y no interactúan directamente con la página (agregar una actividad no va a cambiar los datos), esto se hizo de acuerdo a lo pedido y hablado en clases.