import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import messagebox, ttk
import random

# ----------------------------
# Datos simulados
# ----------------------------
np.random.seed(42)
n_cursos = 10
df = pd.DataFrame({
    'Curso': [f'Curso {i+1}' for i in range(n_cursos)],
    'Horas': np.random.randint(2, 6, size=n_cursos),
    'Interes': np.random.randint(1, 11, size=n_cursos),
    'Facilidad': np.round(np.random.uniform(5.0, 10.0, size=n_cursos), 2)
})

# ----------------------------
# Lógica de optimización
# ----------------------------
def evaluar(cursos, df):
    total_horas = df['Horas'].iloc[cursos].sum()
    if total_horas > 12:
        return 0
    return df['Interes'].iloc[cursos].sum()

def generar_solucion_inicial(df):
    while True:
        cursos = np.random.choice(df.index, size=3, replace=False)
        if evaluar(cursos, df) > 0:
            return cursos

def mutar(solucion, df):
    nueva = solucion.copy()
    fuera = list(set(df.index) - set(solucion))
    cambiar_idx = np.random.randint(0, 3)
    nueva[cambiar_idx] = np.random.choice(fuera)
    return nueva

def hill_climbing(df, iteraciones=1000):
    actual = generar_solucion_inicial(df)
    mejor = actual.copy()
    mejor_valor = evaluar(mejor, df)

    for _ in range(iteraciones):
        vecino = mutar(actual, df)
        valor_vecino = evaluar(vecino, df)
        if valor_vecino > mejor_valor:
            actual = vecino
            mejor = vecino
            mejor_valor = valor_vecino

    return mejor, mejor_valor

# ----------------------------
# Interfaz gráfica
# ----------------------------
def mostrar_cursos():
    ventana_cursos = tk.Toplevel(ventana)
    ventana_cursos.title("📚 Cursos Disponibles")
    ventana_cursos.geometry("600x350")
    ventana_cursos.configure(bg="#f7f9fc")

    label = tk.Label(ventana_cursos, text="📖 Lista de Cursos Electivos", font=("Segoe UI", 14, "bold"), bg="#f7f9fc", fg="#333")
    label.pack(pady=10)

    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"), foreground="#333")
    style.configure("Treeview", font=("Segoe UI", 10), rowheight=25)

    tree = ttk.Treeview(ventana_cursos, columns=("Curso", "Horas", "Interes", "Facilidad"), show='headings')
    tree.heading("Curso", text="Curso")
    tree.heading("Horas", text="Horas")
    tree.heading("Interes", text="Interés")
    tree.heading("Facilidad", text="Facilidad")

    for i in range(len(df)):
        tree.insert("", "end", values=(df["Curso"][i], df["Horas"][i], df["Interes"][i], df["Facilidad"][i]))

    tree.pack(expand=True, fill="both", padx=20, pady=10)

def mostrar_resultados():
    seleccion, interes_total = hill_climbing(df)
    cursos = df.iloc[seleccion]

    detalle = "\n".join([
        f"📘 {cursos['Curso'].iloc[i]} → {cursos['Horas'].iloc[i]}h/sem, "
        f"Interés: {cursos['Interes'].iloc[i]}, Facilidad: {cursos['Facilidad'].iloc[i]}"
        for i in range(3)
    ])

    mensaje = (
        f"✅ Mejor combinación de cursos:\n\n{detalle}\n\n"
        f"🎯 Interés total: {interes_total}\n"
        f"⏱️ Carga horaria total: {cursos['Horas'].sum()}h"
    )

    messagebox.showinfo("Resultado Óptimo", mensaje)

# ----------------------------
# Ventana Principal
# ----------------------------
ventana = tk.Tk()
ventana.title("🎓 Optimizador de Cursos Electivos")
ventana.geometry("600x400")
ventana.configure(bg="#ecf3f9")

# ----------------------------
# Título
# ----------------------------
titulo = tk.Label(
    ventana,
    text="🔍 Selección Óptima de Cursos Electivos",
    font=("Segoe UI", 18, "bold"),
    bg="#ecf3f9",
    fg="#222"
)
titulo.pack(pady=25)

# ----------------------------
# Estilo botones
# ----------------------------
def hover_in(e):
    e.widget.config(bg="#2a7ab9")

def hover_out(e):
    e.widget.config(bg="#3498db")

estilo_btn = {
    "font": ("Segoe UI", 12),
    "bg": "#3498db",
    "fg": "white",
    "activebackground": "#2a7ab9",
    "activeforeground": "white",
    "bd": 0,
    "relief": "ridge",
    "padx": 25,
    "pady": 12,
    "cursor": "hand2"
}

btn1 = tk.Button(ventana, text="📋 Ver Cursos", command=mostrar_cursos, **estilo_btn)
btn1.pack(pady=10)
btn1.bind("<Enter>", hover_in)
btn1.bind("<Leave>", hover_out)

btn2 = tk.Button(ventana, text="✅ Encontrar Mejor Combinación", command=mostrar_resultados, **estilo_btn)
btn2.pack(pady=10)
btn2.bind("<Enter>", hover_in)
btn2.bind("<Leave>", hover_out)

# ----------------------------
# Créditos
# ----------------------------
creditos = tk.Label(
    ventana,
    text="© 2025 • Optimizador Académico",
    font=("Segoe UI", 9),
    bg="#ecf3f9",
    fg="#888"
)
creditos.pack(side="bottom", pady=15)

ventana.mainloop()
