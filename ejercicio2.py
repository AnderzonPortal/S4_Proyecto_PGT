import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import messagebox, ttk

# Datos de franjas horarias
np.random.seed(42)
n_franjas = 10
data = {
    'Duracion': np.random.randint(1, 5, size=n_franjas),
    'Productividad': np.random.randint(1, 11, size=n_franjas)
}
franjas = pd.DataFrame(data)

# Funciones de algoritmo
def evaluar(solucion, franjas, max_horas=15):
    duracion_total = np.sum(franjas['Duracion'] * solucion)
    if duracion_total > max_horas:
        return 0
    productividad_total = np.sum(franjas['Productividad'] * solucion)
    return productividad_total

def generar_solucion_inicial(franjas, max_horas=15):
    while True:
        solucion = np.random.randint(0, 2, size=len(franjas))
        if np.sum(franjas['Duracion'] * solucion) <= max_horas:
            return solucion

def mutar(solucion):
    vecino = solucion.copy()
    idx = np.random.randint(0, len(solucion))
    vecino[idx] = 1 - vecino[idx]
    return vecino

def hill_climbing(franjas, iteraciones=1000):
    actual = generar_solucion_inicial(franjas)
    mejor = actual.copy()
    mejor_valor = evaluar(mejor, franjas)
    for _ in range(iteraciones):
        vecino = mutar(actual)
        valor_vecino = evaluar(vecino, franjas)
        if valor_vecino > mejor_valor:
            actual = vecino
            mejor = vecino
            mejor_valor = valor_vecino
    return mejor, mejor_valor

# Interfaz avanzada
def mostrar_franjas():
    ventana_franjas = tk.Toplevel(ventana)
    ventana_franjas.title("Tabla de Franjas Horarias")
    ventana_franjas.geometry("400x300")
    ventana_franjas.configure(bg="#f0f0f0")

    label = tk.Label(ventana_franjas, text="Franjas Horarias (Duración / Productividad)", font=("Helvetica", 12, "bold"), bg="#f0f0f0")
    label.pack(pady=10)

    tree = ttk.Treeview(ventana_franjas, columns=("Duracion", "Productividad"), show='headings')
    tree.heading("Duracion", text="Duración (h)")
    tree.heading("Productividad", text="Productividad")
    for i in range(len(franjas)):
        tree.insert("", "end", values=(franjas["Duracion"][i], franjas["Productividad"][i]))
    tree.pack(expand=True, fill="both", padx=10, pady=10)

def mostrar_resultados():
    mejor_solucion, productividad = hill_climbing(franjas)
    horas_totales = np.sum(franjas['Duracion'] * mejor_solucion)

    detalle_sol = "\n".join(
        [f"Franja {i+1}: {'✅ Seleccionada' if mejor_solucion[i] else '❌ Omitida'} | "
         f"{franjas['Duracion'][i]} h - Prod: {franjas['Productividad'][i]}"
         for i in range(len(mejor_solucion))]
    )

    mensaje = (
        f"🔍 Mejor solución encontrada:\n\n{detalle_sol}\n\n"
        f"⏳ Total de horas: {horas_totales} h\n"
        f"📈 Productividad total: {productividad}"
    )

    messagebox.showinfo("Resultado de Optimización", mensaje)

# Ventana principal
ventana = tk.Tk()
ventana.title("Optimizador de Horarios - Algoritmos Evolutivos")
ventana.geometry("500x300")
ventana.configure(bg="#e6f2ff")

# Título
titulo = tk.Label(
    ventana, text="Optimización del Horario de Estudio",
    font=("Helvetica", 16, "bold"), bg="#e6f2ff", fg="#003366"
)
titulo.pack(pady=20)

# Botones decorados
estilo_btn = {
    "font": ("Helvetica", 12),
    "bg": "#007acc",
    "fg": "white",
    "activebackground": "#005f99",
    "activeforeground": "white",
    "bd": 0,
    "relief": "ridge",
    "padx": 20,
    "pady": 10
}

btn1 = tk.Button(ventana, text="📋 Ver Franjas Horarias", command=mostrar_franjas, **estilo_btn)
btn1.pack(pady=10)

btn2 = tk.Button(ventana, text="🚀 Ejecutar Optimización", command=mostrar_resultados, **estilo_btn)
btn2.pack(pady=10)

ventana.mainloop()
