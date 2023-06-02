from flask import Flask, render_template, redirect, request
import csv
import jinja2
import os
import subprocess
import pdfkit

app = Flask(__name__)

# Ruta al archivo CSV donde se guardarán los datos
ruta_datosP = 'C:/Users/Oscar/Desktop/cvs/datos_personales.csv'
ruta_formacionA = 'C:/Users/Oscar/Desktop/cvs/formacion_academica.csv'
ruta_experienciaL = 'C:/Users/Oscar/Desktop/cvs/experiencia_laboral.csv'
# Ruta al archivo PDF 
ruta_archivo_pdf = 'C:/Users/Oscar/Desktop/cvs/mi_curriculum.pdf'
ruta_plantilla = 'C:/Users/Oscar/Desktop/pagina-web/templates/plantilla_cv.html'
ruta_wkhtmltopdf = 'C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'

# Lee los datos anteriores si existen 
def leer_datos_csv(nombre_archivo):
    datos = []
    try:
        with open(nombre_archivo, 'r') as archivo_csv:
            lector_csv = csv.DictReader(archivo_csv)
            datos = list(lector_csv)
    except FileNotFoundError:
        pass

    return datos

# Donde se guardan los datos 
def guardar_datos_csv(datos, nombre_archivo):
    encabezados = datos[0].keys()

    datos_existentes = leer_datos_csv(nombre_archivo)
    datos_completos = datos_existentes + datos

    with open(nombre_archivo, 'w', newline='') as archivo_csv:
        escritor_csv = csv.DictWriter(archivo_csv, fieldnames=encabezados)
        escritor_csv.writeheader()
        escritor_csv.writerows(datos_completos)


# Lee los datos y envía los últimos
def obtener_ultimos_datos_guardados(archivo_csv):
            ultimo_dato = []
            with open(archivo_csv, 'r') as file:
                reader = csv.DictReader(file)
                datos = list(reader)
              # Obtener los últimos datos guardados
            ultimo_dato = datos[-1:] if datos else {}
            return ultimo_dato
                
# Se unifican los últimos datos obtenidos
def unificar_datos():
    rutas = [ruta_datosP, ruta_formacionA, ruta_experienciaL]
    # Obtener los datos de la ruta
    ultimos_datos = {}
    for ruta in rutas:      
        archivo_csv = ruta
        # Concatenar los datos
        ultimo_dato = obtener_ultimos_datos_guardados(archivo_csv)
        
        for diccionario in ultimo_dato:
            ultimos_datos.update(diccionario)
    
    return ultimos_datos

# Generar PDF a partir de una plantilla html
def generar_pdf(ruta_plantilla, lista_datos):  # Ruta de plantilla, diccionario, rutacss=''
    nombre_plantilla = ruta_plantilla.split('/')[-1]
    ruta_plantilla = ruta_plantilla.replace(nombre_plantilla, '')

    # Se carga la plantilla y se le envía el diccionario con los datos
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(ruta_plantilla))
    plantilla = env.get_template(nombre_plantilla)
    html = plantilla.render(lista_datos)
    # Formato del documento PDF
    options = {
        '--page-size': 'A4',
        '--margin-top': '2cm',
        '--margin-right': '2cm',
        '--margin-bottom': '2cm',
        '--margin-left': '2cm',
        'encoding': 'UTF-8'
    }
    # Indicar ruta donde se guarda el archivo y convertir a formato PDF
    config = pdfkit.configuration(wkhtmltopdf= ruta_wkhtmltopdf)
    ruta_salida = ruta_archivo_pdf
    # Indicar ruta al archivo css=rutacss antes de options
    pdfkit.from_string(html, ruta_salida, options=options, configuration=config)
    print("archivo generado con exito!!")
    
 
def abrir_pdf():
    if os.name == 'nt':  # Windows
        os.startfile(ruta_archivo_pdf)
    else:  # Linux o macOS
        subprocess.Popen(['xdg-open', ruta_archivo_pdf])



# Ruta inicial
@app.route('/')
def index():
    return redirect('/principal')

# Ruta principal
@app.route('/principal')
def principal():
    return render_template('/principal.html')

# Ruta de datos personales
@app.route('/datos-personales', methods=['GET', 'POST'])
def datos_personales():
    if request.method == 'POST':
        # Obtener los datos enviados por el formulario
        cuil = request.form['cuil']
        nombre = request.form['nombre']
        # ... completar con los demás campos

        # Guardar los datos en una lista de diccionarios
        datos_personales = [
            {
                'CUIL': cuil,
                'Nombre': nombre,
                # ... completar con los demás campos
            }
        ]
       
        # Guardar los datos en el archivo CSV
        guardar_datos_csv(datos_personales, ruta_datosP)

        # Redireccionar a la siguiente sección
        return redirect('/formacion-academica')
    return render_template('datos-personales.html')

# Ruta de formación académica
@app.route('/formacion-academica', methods=['GET', 'POST'])
def formacion_academica():
    if request.method == 'POST':
        # Obtener los datos enviados por el formulario
        titulo = request.form['titulo']
        institucion = request.form['institucion']
        # ... completar con los demás campos

        # Guardar los datos en una lista de diccionarios
        formacion_academica = [
            {
                'Titulo': titulo,
                'Institucion': institucion,
                # ... completar con los demás campos
            }
        ]

        # Guardar los datos en el archivo CSV
        guardar_datos_csv(formacion_academica, ruta_formacionA)

        # Redireccionar a la siguiente sección
        return redirect('/experiencia-laboral')
    return render_template('formacion-academica.html')

# Ruta de experiencia laboral
@app.route('/experiencia-laboral', methods=['GET', 'POST'])
def experiencia_laboral():
    if request.method == 'POST':
        # Obtener los datos enviados por el formulario
        empresa = request.form['empresa']
        rubro = request.form['rubro']
        # ... completar con los demás campos

        # Guardar los datos en una lista de diccionarios
        experiencia_laboral = [
            {
                'Empresa': empresa,
                'Rubro': rubro,
                # ... completar con los demás campos
            }
        ]

        # Guardar los datos en el archivo CSV
        guardar_datos_csv(experiencia_laboral, ruta_experienciaL)

        # Recibir datos para enviar a plantilla
        if 'crear' in request.form:            
            return redirect('/plantilla_cv')
        else:
            return redirect('/experiencia-laboral')

    return render_template('experiencia-laboral.html')

# Ruta de  plantilla
@app.route('/plantilla_cv')
def mostrar_plantilla():
    # Recibir datos para colocar en plantilla
    lista_datos = unificar_datos()
    
    # Generar PDF y abrir el archivo
    generar_pdf(ruta_plantilla, lista_datos)
    abrir_pdf()
    return redirect('/principal')


if __name__ == '__main__':
    app.run(debug=True) # Se actualiza automáticamente