import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import messagebox, ttk
import random

# Datos del menú universitario
np.random.seed(42)
n_platos = 8
menu = pd.DataFrame({
    'Precio': np.random.randint(5, 11, size=n_platos),            # S/5 a S/10
    'Calorias': np.random.randint(200, 600, size=n_platos),       # 200 a 600 cal
    'Satisfaccion': np.random.randint(1, 11, size=n_platos)       # 1 a 10
})

# Evaluar una combinación
def evaluar(platos, menu):
    total_precio = np.sum(menu['Precio'].iloc[platos])
    total_calorias = np.sum(menu['Calorias'].iloc[platos])
    if total_precio > 20 or total_calorias > 1000:
        return 0
    return np.sum(menu['Satisfaccion'].iloc[platos])

# Generar combinación inicial válida
def generar_solucion_inicial(menu):
    while True:
        platos = np.random.choice(menu.index, size=3, replace=False)
        if evaluar(platos, menu) > 0:
            return platos

# Mutar solución (cambiar un plato por otro que no esté en la lista)
def mutar(solucion, menu):
    nueva = solucion.copy()
    fuera = list(set(menu.index) - set(solucion))
    cambiar_idx = np.random.randint(0, 3)
    nueva[cambiar_idx] = np.random.choice(fuera)
    return nueva

# Algoritmo Hill Climbing
def hill_climbing(menu, iteraciones=1000):
    actual = generar_solucion_inicial(menu)
    mejor = actual.copy()
    mejor_valor = evaluar(mejor, menu)

    for _ in range(iteraciones):
        vecino = mutar(actual, menu)
        valor_vecino = evaluar(vecino, menu)
        if valor_vecino > mejor_valor:
            actual = vecino
            mejor = vecino
            mejor_valor = valor_vecino

    return mejor, mejor_valor

# Mostrar menú
def mostrar_menu():
    ventana_menu = tk.Toplevel(ventana)
    ventana_menu.title("Menú Universitario")
    ventana_menu.geometry("400x300")
    ventana_menu.configure(bg="#fdfdfd")

    label = tk.Label(ventana_menu, text="Platos del Menú", font=("Helvetica", 12, "bold"), bg="#fdfdfd")
    label.pack(pady=10)

    tree = ttk.Treeview(ventana_menu, columns=("Precio", "Calorías", "Satisfacción"), show='headings')
    tree.heading("Precio", text="Precio (S/)")
    tree.heading("Calorías", text="Calorías")
    tree.heading("Satisfacción", text="Satisfacción")

    for i in range(len(menu)):
        tree.insert("", "end", values=(menu["Precio"][i], menu["Calorias"][i], menu["Satisfaccion"][i]))

    tree.pack(expand=True, fill="both", padx=10, pady=10)

# Mostrar resultado
def mostrar_resultados():
    seleccion, satisfaccion = hill_climbing(menu)
    platos = menu.iloc[seleccion]

    detalle = "\n".join([
        f"🍽️ Plato {i+1}: Precio S/{platos['Precio'].iloc[i]} | "
        f"{platos['Calorias'].iloc[i]} cal | Satisfacción: {platos['Satisfaccion'].iloc[i]}"
        for i in range(3)
    ])

    mensaje = (
        f"✅ Mejor combinación de platos:\n\n{detalle}\n\n"
        f"💰 Precio total: S/{platos['Precio'].sum()}\n"
        f"🔥 Calorías totales: {platos['Calorias'].sum()} cal\n"
        f"🎉 Satisfacción total: {satisfaccion}"
    )

    messagebox.showinfo("Resultado de Selección de Platos", mensaje)

# Interfaz principal
ventana = tk.Tk()
ventana.title("Selección Óptima de Platos")
ventana.geometry("500x300")
ventana.configure(bg="#fff8f0")

titulo = tk.Label(
    ventana, text="Menú Universitario - Optimización de Platos",
    font=("Helvetica", 16, "bold"), bg="#fff8f0", fg="#333"
)
titulo.pack(pady=20)

estilo_btn = {
    "font": ("Helvetica", 12),
    "bg": "#ff6600",
    "fg": "white",
    "activebackground": "#cc5200",
    "activeforeground": "white",
    "bd": 0,
    "relief": "ridge",
    "padx": 20,
    "pady": 10
}

btn1 = tk.Button(ventana, text="📋 Ver Menú", command=mostrar_menu, **estilo_btn)
btn1.pack(pady=10)

btn2 = tk.Button(ventana, text="🍛 Encontrar Mejor Combinación", command=mostrar_resultados, **estilo_btn)
btn2.pack(pady=10)

ventana.mainloop()
