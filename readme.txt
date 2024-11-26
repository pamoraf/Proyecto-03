# Proyecto de Esquema de Secreto Compartido de Shamir

## Descripción
Este proyecto implementa el esquema srecreto compartido de Shamir para ocultar y develar archivos de texto.

## Requisitos y Comandos de Instalación:
    Python 3.x
    pip para instalar dependencias de Python
    cryptography para realizar el encriptado y desencriptado

### Instalación

1. **Clona el Repositorio**:
   Abre una terminal y ejecuta el siguiente comando para clonar el repositorio:
   ```
   git clone <url-del-repositorio>
   cd <directorio-del-repositorio>
   ```

2. **Instalar dependencias**:
Instale las dependencias necesarias utilizando pip. Asegúrese de que el entorno virtual esté activado si lo está utilizando. En la carpeta debe de existir un archivo llamado requirements.txt En el se encuentra todas las dependencias necesarias para el uso de la pagina web.

Instale las dependencias con:

pip install -r requirements.txt

### Ejecutar el Proyecto
Respecto a la ejecucion el programa se ejecuta directamente en la terminal pasando la opcion (cifrar/descifrar) como argumentos
Para cifrar:
python3 src/main/main.py d <eval_file>  <encrypted_file> 

	<eval_file> : El archivo en donde se guardan los fragmentos de las evaluaciones de la llave generada con la contraseña (etension .frg).
	
	<encrypted_file> : El archivo con el texto cifrado en bytes (extension .aes).

Para descifrar:
python3 src/main/main.py c <eval_file>  <total_evaluatoins> <minimum_evaluations>  <input_file>

	<eval_file> : El archivo en donde se guardan los fragmentos de las evaluaciones de la llave generada con la contraseña (extension .frg).

	<total_evaluatoins>  : La cantidad total de evaluaciones (numero entero positivo).

	<minimum_evaluations> : La cantidad mínima de evaluaciones necesarias para descifrar el texto (numero entero positivo).

	<input_file> : El archivo de texto a ocultar (extension .txt).

EL programa ademas provee las opciones:
-h y --help
en donde se explica el como ejecutar el programa.

## Uso
Ejemplo de Cifrado
Si deseas cifrar un archivo mensaje.txt, donde se generen 5 evaluaciones y se requieran al menos 3 para descifrar, ejecuta:
python3 src/main/main.py c claves.frg 5 3 mensaje.txt
Esto generará:
    Un archivo cifrado llamado mensaje.aes.
    Un archivo con los fragmentos claves.frg.

Ejemplo de Descifrado
Para recuperar el contenido original utilizando al menos 3 fragmentos de claves.frg y el archivo cifrado mensaje.aes, ejecuta:
python3 src/main/main.py d claves.frg mensaje.aes
El contenido descifrado se guardará en un archivo con el mismo nombre original anadiendo _revealed.txt (por ejemplo, mensaje_revealed.txt).

## Notas Importantes
    -El archivo de fragmentos debe tener extensión .frg.
    -El archivo de texto a ocultar debe tener extensión .txt.
    -El archivo cifrado generado tendrá extensión .aes.
    -Si se introducen menos fragmentos de los necesarios para descifrar se generara un archivo de texto vacio.
    -Los archivos de revelado se generan en el mismo directorio que los archivos cifrados.
