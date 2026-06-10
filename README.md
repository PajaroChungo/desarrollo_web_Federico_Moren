Hola buenas, este es el archivo de documentación de la página Actividades DCC, trabajo de Federico Moren. 
------------------------------------------------------------------
Si desea probar el código lea la documentación en el archivo "crear_db_juguete.py" en la carpeta "database", se ha creado una pequeña base de juguete para probar las funcionalidades.

Notesé que para ello es necesario tener activa la "venv" del proyecto, para ver los requisitos revise el archivo "requirement.txt".
------------------------------------------------------------------
A continuación se detallan algunas desiciones de diseño al momento de crear la aplicación web (se habla sobre la Tarea 3, para anteriores revisar README de las otras ramas):

-Métricas:
    Para la página de métricas se decidio usar Highcharts ya que fue el método usado por el auxiliar. Para poder visualizar mejor como se comportan estas se modifico la base de juguetes de modo que ahora se tienen tiempos de registros diferentes y diferentes comunas.

-Perfil de Actividad:
    Debido a un tema de espacio se decidio crear una página en especial para cada actividad. De este modo la lista de actividades no se sobrecarga de información visual al agregar la función de comentarios y en cambio se encuentra en cada perfil.
    Se hizo algo parecido a lo que pasa en redes sociales, ahora tocar el nombre de un usuario redirige a la anteriormente creada "perfil de miembro", y al tocar el nombre de una actividad (tanto en lista de actividades como en perfil de miembro) redirige al "perfil de actividad". 

    En esta página se muestran las imágenes con una mayor resolución y sin cropearse, ya que ahora no hay que preocuparse tanto por el espacio que ocupan otras actividades, como en la lista.
    Además, y como ya se menciono, se encuentra el formulario y la lista de comentarios. Se implementan las funcionalidades pedidas; se puede escoger nombre de usuario al momento de crear un comentario, escribir y publicarlo. Luego este se guarda en la db y aparece en la lista correspondiente a su actividad.

    Notesé que se modifico base de juguetes para mostrar comentarios en distintas publicaciones, para poder evaluar de mejor manera el comportamiento de la página.

No esta demás mencionar que se pensó dejar menos detalles en la lista de actividades, cosa de que fuera una "preview" de lo que se fuera a encontrar en el perfil de actividades, sin embargo se decidio no hacerlo para no romper lo construído en las tareas anteriores.
