from tkinter import messagebox, simpledialog
import tkinter as tk
import json

def get_hours():
    try:
        horas_input = simpledialog.askstring("Ingresar horas", "Ingrese las horas de impresión:")
        return int(horas_input) if horas_input else 0
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese un número válido para las horas.")
        return get_hours()

def get_minutes():
    try:
        minutos_input = simpledialog.askstring("Ingresar minutos", "Ingrese los minutos de impresión:")
        return int(minutos_input) if minutos_input else 0
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese un número válido para los minutos.")
        return get_minutes()

def get_price():
    try:
        price_input = simpledialog.askstring("Ingresar precio", "Ingrese el precio de cura:")
        return float(price_input) if price_input else 0.0
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese un número válido para el precio.")
        return get_price()

def convert_to_minutes(horas, minutos):
    return horas * 60 + minutos

def show_result(neto, total):
    neto = round(neto, 2)
    total = round(total, 2)
    messagebox.showinfo("Resultado", f"El precio de la impresión Neto es de {neto}\n  el valor total con IVA es de {total}")

def desgaste_precio(total_minutos, desgaste):
    return round(total_minutos * desgaste, 3)

def not_material_cost(average_cost, total_minutos):
    return round(average_cost * total_minutos, 2)

def total_luz(total_minutos, costo_x_min):
    return round(total_minutos * costo_x_min, 2)

def main():
    root = tk.Tk()
    root.withdraw()

    try:
        with open('config.json') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        messagebox.showerror("Error", "Error al cargar el archivo de configuración.")
        return

    desgaste = data.get('desgaste', 0.0)
    prom_MxM = data.get('promedio_MxM', 0.0)
    per_material = data.get('porcentaje_material', 0.0)
    cost_x_min = data.get('costo_por_minuto', 0.0)
    option = simpledialog.askstring("Seleccionar opción", "Seleccione una opción: (bajo, medio, alto)")
    if option == "bajo":
        desgaste = data.get('desgaste_bajo', 0.0)
        prom_MxM = data.get('promedio_MxM_bajo', 0.0)
        per_material = data.get('porcentaje_material_bajo', 0.0)
        cost_x_min = data.get('costo_por_minuto_bajo', 0.0)
    elif option == "medio":
        desgaste = data.get('desgaste_medio', 0.0)
        prom_MxM = data.get('promedio_MxM_medio', 0.0)
        per_material = data.get('porcentaje_material_medio', 0.0)
        cost_x_min = data.get('costo_por_minuto_medio', 0.0)
    elif option == "alto":
        desgaste = data.get('desgaste_alto', 0.0)
        prom_MxM = data.get('promedio_MxM_alto', 0.0)
        per_material = data.get('porcentaje_material_alto', 0.0)
        cost_x_min = data.get('costo_por_minuto_alto', 0.0)
    else:
        messagebox.showerror("Error", "Opción inválida.")
        return

    horas = get_hours()
    minutos = get_minutes()
    material = get_price()
    total_minutos = convert_to_minutes(horas, minutos)
    precio_desgaste = desgaste_precio(total_minutos, desgaste)
    costo_sin_material = not_material_cost(prom_MxM, total_minutos)
    costo_luz = total_luz(total_minutos, cost_x_min)
    IVA = data.get("IVA", 0.0) / 100
    margen = data.get("margen", 0.0)
    cost_operacional = data.get("costo_operacional", 0.0)

    cost_indirecto = precio_desgaste + costo_luz
    costo_final = material * (1 + (per_material/100)) + cost_indirecto + cost_operacional + costo_sin_material
    net_price = costo_final  / (1 - (margen/100))
    final_price = net_price * 1.19
    show_result(net_price, final_price)

    root.destroy()

if __name__ == "__main__":
    main()
