Hola!

Para la correcta ejecución de este script debemos tener instalada la libreria:

-"paramiko" para la intacion desde la terminal es usar el comando:
   - "pip install paramiko"

Tambien debemos tener en cuenta que los comandos que emplea este script para eliminar
los usarios sean los mismos que use tu servidor virtual ya que varian dependiendo la version
y el SO (Estos comando son para servidores linux).


-Para evitar fallas o caidas del servidor este script crea logs como "copias de seguridad"
por si ocurre una falla en el servidor pero aun asi se recomienda que hagamos una prueba 
de conexión, que es la versión light del script donde solo se verifica el correcto 
funcionamiento del mismo.

Nota: En este ultimo paso se puede jugar ocn los comando para verificar la viabilidad
      de uso con el servidor con el que estes trabajando.
