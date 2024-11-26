# Proyecto de Esquema de Secreto Compartido de Shamir

## Descripción
Este proyecto implementa el esquema de secreto compartido de Shamir para ocultar y develar archivos de texto. Divide una clave en fragmentos, asegurando que solo una cantidad mínima de fragmentos sea suficiente para recuperar la información original.

## Requisitos y Comandos de Instalación

### Requisitos
- Python 3.x
- `pip` para instalar dependencias de Python
- Biblioteca `cryptography` para encriptación y desencriptación

### Instalación

1. **Clonar el Repositorio**  
   Abre una terminal y ejecuta:  
   ```bash
   git clone <url-del-repositorio>
   ```
   ```bash
   cd <directorio-del-repositorio>
   ```

2. Instalar Dependencias
Asegúrate de tener un archivo requirements.txt en el directorio principal del proyecto. Instala las dependencias ejecutando:
   ```bash
   pip install -r requirements.txt

3.Ejecutar el Proyecto

El programa se ejecuta desde la terminal. Puedes elegir entre cifrar o descifrar archivos de texto mediante los siguientes comandos:
Cifrar:
   ```bash
   python3 src/main/main.py c <eval_file> <total_evaluations> <minimum_evaluations> <input_file>
   ```
- <eval_file>: Nombre del archivo donde se guardarán los fragmentos de las evaluaciones de la llave generada (extensión .frg).
- <total_evaluations>: Número total de evaluaciones (entero positivo mayor a 2).
- <minimum_evaluations>: Cantidad mínima de evaluaciones necesarias para descifrar el texto (entero positivo, 1 < t ≤ total_evaluations).
- <input_file>: Archivo de texto a ocultar (extensión .txt).

Descifrar:
 ```bash
 python3 src/main/main.py d <eval_file> <encrypted_file>
 ```
- <eval_file>: Archivo con los fragmentos de las evaluaciones de la llave generada (extensión .frg).
- <encrypted_file>: Archivo cifrado con el texto en bytes (extensión .aes).

Opciones de Ayuda

Para obtener más información, ejecuta:
 ```bash
python3 src/main/main.py -h
 ```

Uso
Ejemplo de Cifrado

Si deseas cifrar un archivo mensaje.txt, generar 5 evaluaciones y requerir al menos 3 para descifrar:
 ```bash
 python3 src/main/main.py c claves.frg 5 3 mensaje.txt
 ```

Esto generará:

 - Un archivo cifrado llamado mensaje.aes.
 - Un archivo de fragmentos llamado claves.frg.

Ejemplo de Descifrado

Para recuperar el contenido original con al menos 3 fragmentos de claves.frg y el archivo cifrado mensaje.aes:

 ```bash
 python3 src/main/main.py d claves.frg mensaje.aes
 ```

El resultado se guardará en un archivo llamado mensaje_revealed.txt.
Notas Importantes

- El archivo de fragmentos debe tener extensión .frg.
- El archivo de texto a ocultar debe tener extensión .txt.
- El archivo cifrado generado tendrá extensión .aes.
- Si se introducen menos fragmentos de los necesarios para descifrar, se generará un archivo de texto vacío.
- Los archivos generados se almacenan en el mismo directorio que los archivos originales.
