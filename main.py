import tkinter as tk
from tkinter import filedialog, messagebox
import random
import csv
import heapq
import os
from pathlib import Path


def load_names_from_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return [line.strip() for line in file]
    except FileNotFoundError:
        messagebox.showerror("Błąd", "Nie znaleziono pliku imiona_polskie.csv!")
        return ["Jan", "Anna", "Piotr", "Maria", "Krzysztof", "Agnieszka"]


# Generowanie danych z wykorzystaniem generatora
def generate_data_generator(file_path, num_lines):
    names = load_names_from_file("imiona_polskie.csv")
    surnames = ["Kowalski", "Nowak", "Wiśniewski", "Dąbrowski", "Lewandowski"]
    delivery_methods = ["Kurier", "Paczkomat", "Odbiór osobisty", "Poczta", "Dostawa express"]
    items = ["Laptop", "Koszula", "Książka", "Piłka", "Mikser"]

    def data_generator():
        for _ in range(num_lines):
            yield f"{random.choice(names)};{random.choice(surnames)};{random.choice(delivery_methods)};{random.choice(items)};{random.randint(10, 1000)}"

    with open(file_path, 'w', newline='') as file:
        for line in data_generator():
            file.write(line + "\n")


# Generowanie danych z wykorzystaniem listy
def generate_data_list(file_path, num_lines):
    names = load_names_from_file("imiona_polskie.csv")
    surnames = ["Kowalski", "Nowak", "Wiśniewski", "Dąbrowski", "Lewandowski"]
    delivery_methods = ["Kurier", "Paczkomat", "Odbiór osobisty", "Poczta", "Dostawa express"]
    items = ["Laptop", "Koszula", "Książka", "Piłka", "Mikser"]

    data = [f"{random.choice(names)};{random.choice(surnames)};{random.choice(delivery_methods)};{random.choice(items)};{random.randint(10, 1000)}" for _ in range(num_lines)]

    with open(file_path, 'w', newline='') as file:
        file.write("\n".join(data) + "\n")


def search_data(input_file, output_file, keyword, filter_gender):
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        for line in infile:
            columns = line.strip().split(";")
            if (not keyword or keyword.lower() in line.lower()):
                if filter_gender and not columns[0].endswith("a"):
                    continue
                outfile.write(line)


def external_sort(input_file, column, descending):
    sorted_chunks = []

    def chunk_iterator():
        chunk_size = 1000  # Można dostosować do pamięci
        with open(input_file, 'r') as infile:
            chunk = []
            for line in infile:
                chunk.append(line.strip().split(";"))
                if len(chunk) >= chunk_size:
                    yield chunk
                    chunk = []
            if chunk:
                yield chunk

    for chunk in chunk_iterator():
        chunk.sort(key=lambda x: (x[column] if column != 4 else float(x[column])), reverse=descending)
        sorted_chunks.append(chunk)

    # Łączenie posortowanych kawałków
    return heapq.merge(*sorted_chunks, key=lambda x: (x[column] if column != 4 else float(x[column])), reverse=descending)


def sort_data(input_file, output_file, column, descending):
    sorted_data = external_sort(input_file, column, descending)

    with open(output_file, 'w', newline='') as outfile:
        for row in sorted_data:
            outfile.write(";".join(row) + "\n")


def browse_file(entry):
    file_path = filedialog.askopenfilename()
    if file_path:
        entry.delete(0, tk.END)
        entry.insert(0, file_path)


def generate_action():
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if file_path:
        try:
            num_lines = int(lines_entry.get())
            if use_list_var.get():
                generate_data_list(file_path, num_lines)
            else:
                generate_data_generator(file_path, num_lines)
            input_entry.delete(0, tk.END)
            input_entry.insert(0, file_path)
            messagebox.showinfo("Sukces", "Dane wygenerowane pomyślnie!")
        except ValueError:
            messagebox.showerror("Błąd", "Podaj poprawną liczbę wierszy!")


def search_action():
    input_file = input_entry.get()
    output_file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    keyword = search_entry.get()
    if Path(input_file).suffix != ".csv":
        messagebox.showinfo("Błąd","Wybrano zły plik.")
    else:
        if input_file and output_file:
            search_data(input_file, output_file, keyword, gender_var.get())
            messagebox.showinfo("Sukces", "Wyniki zapisane!")


def sort_action():
    input_file = input_entry.get()
    output_file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    column = sort_options.index(sort_column.get())
    descending = order_var.get()
    if Path(input_file).suffix != ".csv":
        messagebox.showinfo("Błąd", "Wybrano zły plik.")
    else:
        if input_file and output_file:
            sort_data(input_file, output_file, column, descending)
            messagebox.showinfo("Sukces", "Dane posortowane!")


root = tk.Tk()
root.title("Generator i Analizator CSV")

# Generowanie pliku
lines_label = tk.Label(root, text="Liczba wierszy:")
lines_label.pack()
lines_entry = tk.Entry(root)
lines_entry.pack()

use_list_var = tk.BooleanVar()
use_list_checkbox = tk.Checkbutton(root, text="Użyj listy zamiast generatora", variable=use_list_var)
use_list_checkbox.pack()

generate_button = tk.Button(root, text="Generuj CSV", command=generate_action)
generate_button.pack()

# Wybór pliku wejściowego
input_label = tk.Label(root, text="Plik CSV:")
input_label.pack()
input_entry = tk.Entry(root, width=50)
input_entry.pack()
browse_button = tk.Button(root, text="Przeglądaj", command=lambda: browse_file(input_entry))
browse_button.pack()

# Szukanie
search_label = tk.Label(root, text="Szukaj:")
search_label.pack()
search_entry = tk.Entry(root)
search_entry.pack()

gender_var = tk.BooleanVar()
gender_checkbox = tk.Checkbutton(root, text="Tylko imiona żeńskie", variable=gender_var)
gender_checkbox.pack()

search_button = tk.Button(root, text="Szukaj", command=search_action)
search_button.pack()

# Sortowanie
sort_options = ["Imię", "Nazwisko", "Forma dostawy", "Przedmiot", "Cena"]
sort_label = tk.Label(root, text="Sortuj wg:")
sort_label.pack()
sort_column = tk.StringVar(value=sort_options[4])
sort_dropdown = tk.OptionMenu(root, sort_column, *sort_options)
sort_dropdown.pack()

order_var = tk.BooleanVar()
order_checkbox = tk.Checkbutton(root, text="Malejąco", variable=order_var)
order_checkbox.pack()

sort_button = tk.Button(root, text="Sortuj", command=sort_action)
sort_button.pack()

root.mainloop()
