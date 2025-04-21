import locale
import tkinter as tk
from tkinter import Tk, Entry, Label, filedialog
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from datetime import date
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import PhotoImage
from tkinter import ttk
from PIL import Image, ImageTk
import os
import webbrowser

#prueba de commit
# Ventana principal (menú)
class VentanaMenu(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Menú Principal")
        self.geometry("400x300")

        ttk.Label(self, text="Menú Principal", font=("Arial", 16)).pack(pady=20)
        ttk.Button(self, text="Abrir Carta Recomendación", command=self.abrir_carta).pack(pady=10)
        ttk.Button(self, text="Salir", command=self.quit).pack(pady=10)

    def abrir_carta(self):
        self.destroy()  # Cierra la ventana del Menú
       
        VentanaCarta(self.master)  # Abre la ventana de Carta de Recomendación

     

    def abrir_Cartalaboral(self):
    
        VentanaCartaLaboral(self)  # Llamamos la otra ventana
  
    


# Ventana para la carta
class VentanaCarta(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Carta de Recomendación")
        self.geometry("400x400")
        self.config(bg="white")

        ttk.Label(self, text="Datos del recomendado").pack(pady=5)
        ttk.Label(self, text="Nombre del recomendado:").pack(pady=5)
        self.txt_nombrerec = ttk.Entry(self)
        self.txt_nombrerec.pack(pady=5)

        ttk.Label(self, text="Datos de quien recomienda:").pack(pady=5)
        ttk.Label(self, text="Nombre recomendador:").pack(pady=5)
        self.txt_nombrerecomienda = ttk.Entry(self)
        self.txt_nombrerecomienda.pack(pady=5)

        ttk.Label(self, text="Dirección:").pack(pady=5)
        self.txt_Direccion = ttk.Entry(self)
        self.txt_Direccion.pack(pady=5)

        ttk.Label(self, text="Telefono:").pack(pady=5)
        self.txt_telefono = ttk.Entry(self)
        self.txt_telefono.pack(pady=5)

        ttk.Label(self, text="Años Conociéndose:").pack(pady=5)
        self.txt_anos = ttk.Entry(self)
        self.txt_anos.pack(pady=5)

        # Combo para seleccionar tipo de carta
        ttk.Label(self, text="Selecciona el tipo de carta:").pack(pady=5)
        self.combo = ttk.Combobox(self, values=["CARTA 1", "CARTA 2", "CARTA 3"])
        self.combo.pack(pady=5)
        self.combo.current(0)  # Opción por defecto

        # Etiqueta para mostrar el resultado
        
        self.etiqueta_resultado = tk.Label(self, text="", font=("Arial", 10))

        self.etiqueta_resultado.pack(pady=10)

        ttk.Button(self, text="Generar PDF", command=self.generar_pdfcarta).pack(pady=20)
        ttk.Button(self, text="LIMPIAR", command=self.Borrar).pack(pady=20)
        ttk.Button(self, text="MENU", command=self.abrir_menu).pack(pady=20)
        self.protocol("WM_DELETE_WINDOW", self.cerrar_todas_las_ventanas)


    def generar_pdfcarta(self):
        nombre = self.txt_nombrerec.get()
        nombre_rec = self.txt_nombrerecomienda.get()
        direccion = self.txt_Direccion.get()
        telefono = self.txt_telefono.get()
        anos = self.txt_anos.get()

        if not all([nombre, nombre_rec, direccion, telefono, anos]):
            self.etiqueta_resultado.config(text="⚠️ Por favor, completa todos los campos", foreground="orange")
            return

        hoy = date.today()
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if file_path:
            try:
                doc = SimpleDocTemplate(file_path, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
                styles = getSampleStyleSheet()

                header_style = ParagraphStyle(
                    "HeaderStyle", parent=styles["Normal"],
                    fontName="Helvetica", fontSize=12, alignment=2, spaceAfter=20
                )
                body_style = ParagraphStyle(
                    "BodyStyle", parent=styles["Normal"],
                    fontName="Helvetica", fontSize=12, leading=15, alignment=4, spaceAfter=12
                )
                signature_style = ParagraphStyle(
                    "SignatureStyle", parent=styles["Normal"],
                    fontName="Helvetica-Bold", fontSize=12, leading=15, alignment=1, spaceBefore=20
                )

                story = [
                    Paragraph(f"Puerto Vallarta, Jal. {hoy.strftime('%d de %B de %Y')}", header_style),
                    Spacer(1, 24),
                    Paragraph("A QUIEN CORRESPONDA:", body_style),
                    Spacer(1, 12),
                    Paragraph(
                        f"Me permito informarle que conozco amplia y detalladamente a <b>{nombre}</b> y puedo asegurar que es una persona íntegra, estable, totalmente responsable y competente para cualquier actividad que se le encomiende, ya que lo llevo conociendo durante <b>{anos}</b> años.",
                        body_style),
                    Spacer(1, 12),
                    Paragraph(
                        "Por lo anterior, no tengo inconveniente alguno en recomendarlo, agradeciendo de antemano la atención y facilidades que le puedan brindar. Se extiende la presente para los efectos legales que a la interesada convenga.",
                        body_style),
                    Spacer(1, 48),
                    Paragraph("ATENTAMENTE", signature_style),
                    Spacer(1, 24),
                    Paragraph("______________________________", signature_style),
                    Spacer(1, 12),
                    Paragraph(f"{nombre_rec}", signature_style),
                    Paragraph(f"{direccion}", signature_style),
                    Paragraph(f"Tel. {telefono}", signature_style)
                ]

                story2 = [
                    Paragraph(f"Puerto Vallarta, Jal. {hoy.strftime('%d de %B de %Y')}", header_style),
                    Spacer(1, 24),
                    Paragraph("A QUIEN CORRESPONDA:", body_style),
                    Spacer(1, 12),
                    Paragraph(
                        f"Me permito recomendar a  <b>{nombre}</b> quien conozco desde hace <b>{anos}</b> años, tiempo en el que puedo destacar que es una persona de ética, responsable, puntual y capaz de realizar cualquier actividad de la mejor manera.",
                        body_style),
                    Spacer(1, 12),
                    Paragraph(
                        "Por lo que no tengo inconveniente en recomendarlo ya que lo conozco ampliamente, agradeciendo de antemano las facilidades que le puedan brindar.",
                        body_style),
                    Spacer(1, 48),
                    Paragraph("ATENTAMENTE", signature_style),
                    Spacer(1, 24),
                    Paragraph("______________________________", signature_style),
                    Spacer(1, 12),
                    Paragraph(f"{nombre_rec}", signature_style),
                    Paragraph(f"{direccion}", signature_style),
                    Paragraph(f"Tel. {telefono}", signature_style)
                ]

                story3 = [
                    Paragraph(f"Puerto Vallarta, Jal. {hoy.strftime('%d de %B de %Y')}", header_style),
                    Spacer(1, 24),
                    Paragraph("A QUIEN CORRESPONDA:", body_style),
                    Spacer(1, 12),
                    Paragraph(
                        f"El presente tiene como finalidad recomendar a <b>{nombre}</b>, a quien conozco desde hace <b>{anos}</b> años. Con seguridad puedo destacar sus aptitudes personales, su gran esfuerzo laboral y trabajo en equipo. Es una persona responsable, puntual y respetuosa con una moral excepcional, y que puede realizar los encargos y cometidos que se le asignen.",
                        body_style),
                    Spacer(1, 12),
                    Paragraph(
                        "Por lo anterior no tengo inconveniente en recomendarlo ampliamente, agradeciendo de antemano la atención y facilidades que le puedan brindar. Quedo a sus órdenes para cualquier aclaración o duda.",
                        body_style),
                    Spacer(1, 48),
                    Paragraph("ATENTAMENTE", signature_style),
                    Spacer(1, 24),
                    Paragraph("______________________________", signature_style),
                    Spacer(1, 12),
                    Paragraph(f"{nombre_rec}", signature_style),
                    Paragraph(f"{direccion}", signature_style),
                    Paragraph(f"Tel. {telefono}", signature_style)
                ]

                opcion = self.combo.get()  # Asegúrate de que el combo esté definido como self.combo
                match opcion:
                    case "CARTA 1":
                        doc.build(story)
                        self.etiqueta_resultado.config(text="✅ PDF generado exitosamente.", fg="green")
                    case "CARTA 2":
                        doc.build(story2)
                        self.etiqueta_resultado.config(text="✅ PDF generado exitosamente.", fg="green")
                    case "CARTA 3":
                        doc.build(story3)
                        self.etiqueta_resultado.config(text="✅ PDF generado exitosamente.", fg="green")
                    case _:
                        self.etiqueta_resultado.config(text="❌ Operación no válida.", fg="red")

            except Exception as e:
                self.etiqueta_resultado.config(text=f"❌ Error al guardar el PDF: {str(e)}", fg="red")


    def Borrar(self):
        self.txt_nombrerec.delete(0, tk.END)  # Borra todo el contenido de text1
        self.txt_nombrerecomienda.delete(0, tk.END)  # Borra todo el contenido de text1
        self.txt_Direccion.delete(0, tk.END)  # Borra todo el contenido de text2
        self.txt_telefono.delete(0, tk.END)  # Borra todo el contenido de text2
        self.txt_anos.delete(0, tk.END)  # Borra todo el contenido de text2
    
    
  
    def abrir_menu(self):
        self.destroy()  # Cierra la ventana de Carta de Recomendación
        if not hasattr(self.master, "ventana_menu"):
            self.master.ventana_menu = VentanaMenu(self.master)  # Abre la ventana de Menú si no está abierta
    def cerrar_todas_las_ventanas(self):
        self.destroy()  # Cierra la ventana de Carta de Recomendación
        self.master.quit()  # Cierra todas las ventanas (incluyendo la ventana de Menú)

# Ventana para la carta laboral
class VentanaCartaLaboral(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Carta Recomendación Laboral")
        self.geometry("400x400")
        self.config(bg="white")

        ttk.Label(self, text="Datos del recomendado").pack(pady=5)
        ttk.Label(self, text="Nombre del recomendado:").pack(pady=5)
        self.txt_nombrerec = ttk.Entry(self)
        self.txt_nombrerec.pack(pady=5)

        ttk.Label(self, text="Datos de quien recomienda:").pack(pady=5)
        ttk.Label(self, text="Nombre recomendador:").pack(pady=5)
        self.txt_nombrerecomienda = ttk.Entry(self)
        self.txt_nombrerecomienda.pack(pady=5)

        ttk.Label(self, text="Dirección:").pack(pady=5)
        self.txt_Direccion = ttk.Entry(self)
        self.txt_Direccion.pack(pady=5)

        ttk.Label(self, text="Telefono:").pack(pady=5)
        self.txt_telefono = ttk.Entry(self)
        self.txt_telefono.pack(pady=5)

        ttk.Label(self, text="Años Conociéndose:").pack(pady=5)
        self.txt_anos = ttk.Entry(self)
        self.txt_anos.pack(pady=5)

        ttk.Button(self, text="Generar PDF", command=self.generar_pdf).pack(pady=20)

    def generar_pdf(self):
        nombre = self.txt_nombrerec.get()
        nombre_rec = self.txt_nombrerecomienda.get()
        direccion = self.txt_Direccion.get()
        telefono = self.txt_telefono.get()
        anos = self.txt_anos.get()

        if not all([nombre, nombre_rec, direccion, telefono, anos]):
            ttk.Label(self, text="⚠️ Por favor, completa todos los campos", foreground="orange").pack(pady=5)
            return
        # Aquí iría la lógica para generar el PDF...
        print("Generando PDF de carta laboral...")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal
    VentanaMenu(root)  # Abre el Menú al inicio
    root.mainloop()
