import tkinter as tk
from tkinter import *
import ply.lex as lex

tokens = ['DELIMITADOR','ERROR','RESERVADO','NUMERO','OPERADOR','IDENTIFICADOR','DATATIPO','CADENA']

def t_DELIMITADOR(t):
    r'[\(\)\{\}\[\];]'
    return t

def t_OPERADOR(t):
    r'(\+|\-|=|\*|\/|\+\+)+'
    return t

def t_IDENTIFICADOR(t):
    r'\b(?!int|double|decimal|float|str|char|for|do|while|else|if|main|read|printf|end|static|void|public\b)[A-Za-z0-9]+\b'
    t.type = 'IDENTIFICADOR'
    t.value = t.value.strip()
    return t

def t_CADENA(t):
    r'"([^"]+)"'
    t.type = 'CADENA'
    t.value = t.value.strip()
    return t

def t_DATATIPO(t):
    r'\b(int|double|decimal|float|str|char)\b'
    t.type = 'DATATIPO'
    t.value = t.value.strip()
    return t  

def t_RESERVADO(t):
    r'\b(for|do|while|else|if|main|read|printf|end|static|void|public)\b'
    t.type = 'RESERVADO'
    t.value = t.value.strip()
    return t

def t_NUMERO(t):
    r'(\d+)(\.?\d*)'
    t.value = float(t.value)
    return t

def t_error(t):
    error_texto.insert(tk.END, f"Carácter no válido: '{t.value[0]}'\n")
    t.lexer.skip(1)

lexer = lex.lex()

class Lexer:
    def __init__(self, data):
        self.lexer = lex.lex()
        self.lexer.input(data)
        self.total_tokens = 0
        self.token_counts = {"DELIMITADOR": 0, "ERROR": 0, "RESERVADO": 0, "NUMERO": 0, "OPERADOR": 0, "IDENTIFICADOR": 0, "DATATIPO": 0, "CADENA": 0}

    def reset(self, line):
        line = line.strip()
        self.lexer.input(line)
        self.total_tokens = 0

    def count_tokens(self, token):
        self.total_tokens += 1
        self.token_counts[token.type] += 1


def analizar():
    borrar_resultados()
    lexer = Lexer(entrada_texto.get("1.0", "end-1c"))
    line_number = 1
    total_tokens = 0
    token_counts = {}

    for linea in entrada_texto.get("1.0", "end-1c").splitlines():
        lexer.reset(linea)
        while True:
            token = lexer.lexer.token()
            if not token:
                break      # No more input
            resultado_token.insert(tk.END, f"{token.type}\n")
            resultado_lexema.insert(tk.END, f"{token.value}\n")
            if token.type == 'ERROR':
                error_texto.insert(tk.END, f"Carácter no válido: '{token.value[0]}' en la línea {line_number}\n")
            total_tokens += 1

            # Update the token count dictionary
            if token.type not in token_counts:
                token_counts[token.type] = 1
            else:
                token_counts[token.type] += 1
        line_number += 1

    # Display the total token count
    resultado_total_tokens.insert(tk.END, f"Total tokens: {total_tokens}\n")

    # Display the token type counts
    for token_type, count in token_counts.items():
        resultado_total_token_types.insert(tk.END, f"{token_type} tokens: {count}\n")


def borrar_resultados():
    resultado_token.delete("1.0", tk.END)
    resultado_lexema.delete("1.0", tk.END)
    error_texto.delete("1.0", tk.END)

def borrar():
    entrada_texto.delete("1.0", tk.END)
    borrar_resultados()

ventana = tk.Tk()
ventana.geometry("845x480")
ventana.resizable(width=False, height=False)
ventana.title ("Analizador Lexico")
ventana.config(bg="#A5A09F")

##Entrada de texto

entrada_texto = tk.Text(ventana, font=("Arial",12), bg="white", fg="black", height=10, width=40)
entrada_texto.place(x=40, y=60, width = 350, height=380)
entrada_texto.configure(insertbackground="black")

##Etiquetas para marcar columnas de resultados

reja_token = tk.Label(ventana, text= "Token", font=("Arial",12), bg="white", fg="black")
reja_token.place (x=420, y=60, width = 180, height=15)

reja_lex = tk.Label(ventana, text= "Lexema", font=("Arial",12), bg="white", fg="black")
reja_lex.place (x=610, y=60, width = 180, height=15)

##Resultados

resultado_token = tk.Text(ventana, font=("Arial",10), bg="white", fg="black", height=10, width=40)
resultado_token.place(x=420, y=77, width = 180, height=200)

resultado_lexema = tk.Text(ventana, font=("Arial",10), bg="white", fg="black", height=10, width=40)
resultado_lexema.place(x=610, y=77, width = 180, height=200)

##Totales

reja_totales = tk.Label(ventana, text= "Totales", justify= ["left"], font=("Arial",12), bg="white", fg="black")
reja_totales.place (x=420, y=280, width = 370, height=23)

resultado_total_tokens = tk.Text(ventana, font=("Arial",10), bg="white", fg="black")
resultado_total_tokens.place(x=420, y=305, width = 185, height=50)

resultado_total_token_types = tk.Text(ventana, font=("Arial",10), bg="white", fg="black")
resultado_total_token_types.place(x=610, y=305, width = 180, height=50)

##Errores

reja_error = tk.Label(ventana, text= "Errores", justify= ["left"], font=("Arial",12), bg="white", fg="black")
reja_error.place (x=420, y=360, width = 370, height=23)

error_texto = tk.Text(ventana, font=("Arial",10), bg="white", fg="black")
error_texto.place(x=420, y=385, width = 370, height=50)

##Botones

boton_analizar = tk.Button(ventana, text="Analizar", font=("Arial",12),bg="#EAB488",fg="black",command=analizar)
boton_analizar.place(x=40, y=15)

boton_borrar = tk.Button(ventana, text="Borrar", font=("Arial",12),bg="#EAB488",fg="black",command = borrar)
boton_borrar.place(x=420, y=15)

ventana.mainloop()