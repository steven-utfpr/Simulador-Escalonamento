import tkinter as tk
from tkinter import filedialog
import os

from Algoritmos import FIFO, SRTF, PrioP

def SelArquivo(arqSel):        
    caminho = filedialog.askopenfilename(
        title="Selecione o arquivo de configuração",
        filetypes=[("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*")]
    )
    if caminho:
        nomeArquivo = os.path.basename(caminho)
        WriteLockBox(arqSel, nomeArquivo)
        return caminho
    
def GerarInstrucoes(algoritmo, tarefas):
    algoritimos = {
        "FIFO": FIFO,
        "SRTF": SRTF,
        "PrioP": PrioP
    }
    instrucoes = algoritimos[algoritmo](tarefas)
    return instrucoes

def WriteLockBox(entryBox, texto):
    entryBox.config(state="normal")
    entryBox.delete(0, tk.END)
    entryBox.insert(0,texto)
    entryBox.config(state="readonly")

def LerArquivo(caminho):
    with open(caminho, 'r') as f:
        texto = f.readlines()
        return texto
    
def ProcessarDados(texto):
    tarefas = []
    
    algoritmo, quantum = texto[0].split(';')
    quantum = int (quantum)

    for linha in texto[1:]:
        linha = linha.strip()
        if not linha:
            continue
        partes = linha.split(';',6)
        nome = partes[0]
        id = int(nome[1:])
        cor =  int (partes[1])
        ingresso = int (partes[2])
        duracao = int (partes[3])
        prioridade = int (partes[4])
        eventos = partes[5]

        tarefas.append (
            {
                'nome': nome,
                'id': id,
                'cor': cor,
                'ingresso': ingresso,
                'duracao': duracao,
                'prioridade': prioridade,
                'eventos': eventos
            }
        )
    return tarefas, algoritmo, quantum

def AtualizarLog(logBox, mensagem):
    logBox.insert(tk.END, mensagem + "\n")
    logBox.see(tk.END)

def ResetarValores(self):
    self.tempoMax = 1
    self.tempoAtual = 1    
    self.blocoId = []
    self.bordasId = None
    self.eixosId = []
    self.intrucoes = []
