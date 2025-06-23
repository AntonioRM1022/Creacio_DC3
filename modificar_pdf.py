import fitz  # PyMuPDF
import mysql.connector
import datetime
import subprocess
import sys
def obtener_datos_desde_bd(curso, matricula):
    # Conecta a la base de datos MySQL (ajusta esto según tu configuración)
    conexion = mysql.connector.connect(
        user='root',
        password='Antoniomtz1022',
        host='localhost',
        database='prueba',
        port='3306'
    )
    cursor = conexion.cursor()

    # Ejemplo: Consulta para obtener datos específicos de las tablas 'Empleados' y 'Empresa'
    consulta = """
SELECT 
    E.Nombre, 
    E.Curp, 
    E.Puesto, 
    E.Nacional, 
    Emp.nombre_razon_social, 
    Emp.rfc, 
    C.nombre_curso, 
    C.duracion_semanas, 
    C.fecha_inicio, 
    C.fecha_fin, 
    C.area_tematica
FROM 
    Empleados E
JOIN 
    curso C ON codigo_curso = %s
JOIN 
    empresa Emp ON Emp.id = '1'
WHERE 
    E.Matricula = %s;

    """
    cursor.execute(consulta, (curso, matricula))
    filas = cursor.fetchall()

    conexion.close()

    return filas

def modificar_pdf(input_path, output_path, datos_a_ingresar):
    # Abre el archivo PDF existente
    pdf_document = fitz.open(input_path)

    for datos in datos_a_ingresar:
        # Selecciona la página a modificar (puedes ajustar esto según tus necesidades)
        pagina_modificar = 0  # Página donde deseas ingresar los datos

        # Obtiene la página y su rectángulo
        pagina = pdf_document[pagina_modificar]
        
        # Añade el texto utilizando datos de la base de datos
        datos_x = 75
        datos_y = 155
        font_size = 11
        curp_con_espacios = '  '.join(datos[1])
        texto_a_empleador = f"{datos[0]}\n\n\n\n{datos[2]} "
        pagina.insert_text((datos_x, datos_y), texto_a_empleador, fontname="helv", fontsize=font_size)
        # arriba esta nombre, y puesto de la tabla empleado
        #abajo esta curp y nacional
        datos_x = 73
        datos_y = 190
        font_size = 12
        curp_con_espacios = '  '.join(datos[1])
        texto_a_empleador = f"{curp_con_espacios}  {datos[3]}"
        pagina.insert_text((datos_x, datos_y), texto_a_empleador, fontname="helv", fontsize=font_size)
        #hasta aqui
        #aqui estan datos de la empresa
        datos_x = 77
        datos_y = 225
        font_size = 11
        rfc_con_espacios = '  '.join(datos[5])
        texto_empresa = f"{datos[4]}\n\n{rfc_con_espacios}"
        pagina.insert_text((datos_x, datos_y + 50), texto_empresa, fontname="helv", fontsize=font_size)
        #hasta aquiiii
        #aqui esta datos del curso
        datos_x = 75
        datos_y = 295
        font_size = 11
        texto_curso = f"{datos[6]}\n\n{datos[7]}\n\n{datos[10]}\n"
        pagina.insert_text((datos_x, datos_y + 50), texto_curso, fontname="helv", fontsize=font_size)
    #---------------------------------------------
        #estos dos son los de la fecha
        datos_x = 267
        datos_y = 327
        font_size = 11
        inicio_con_espacios = '  '.join(c for c in str(datos[8]))
       
        texto_curso = f"{inicio_con_espacios}"
        pagina.insert_text((datos_x, datos_y + 50), texto_curso, fontname="helv", fontsize=font_size)
        
        datos_x = 415
        datos_y = 327
        font_size = 12 
        fin_con_espacios = '  '.join(c for c in str(datos[9]))
        texto_curso = f"{fin_con_espacios}"
        pagina.insert_text((datos_x, datos_y + 50), texto_curso, fontname="helv", fontsize=font_size)
#--------------------------------------------------------   
        # Guarda el archivo modificado
        pdf_document.save(output_path)
    
    pdf_document.close()

    # Abre el PDF modificado
    subprocess.run(["start", "", output_path], shell=True)


if __name__ == "__main__":
    # Obtén los valores del código del curso y la matrícula desde los argumentos de línea de comandos
    if len(sys.argv) != 3:
        sys.exit(1)

    curso = sys.argv[1]
    matricula = sys.argv[2]
    pdf_input_path = 'C:/Users/anton/Downloads/DC3/DC3.pdf'
    # Especifica la ruta del archivo PDF de salida (archivo modificado)
    marca_tiempo = datetime.datetime.now().strftime("%Y%m%d")
    pdf_output_path = f'C:/Users/anton/Downloads/DC3/DC3_{curso}_{matricula}.pdf'

    # Obtiene datos de la base de datos utilizando curso y matrícula
    datos = obtener_datos_desde_bd(curso, matricula)

    if datos:
        # Llama a la función para modificar el PDF
        modificar_pdf(pdf_input_path, pdf_output_path, datos)
    else:
        sys.exit(1)