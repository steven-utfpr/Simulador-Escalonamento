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
    
def GerarInstrucoes(algoritmo, tarefas, quantum):
    instrucoes = []
    instrucoesInativas = []
    count = quantum
    tempoMax = DuracaoTotal(tarefas)
    tarefas = sorted(tarefas, key=lambda x: x['ingressoTarefa'])
    algoritimos = {
        "FIFO": FIFO,
        "SRTF": SRTF,
        "PrioP": PrioP
    }
    for i in range(tempoMax):
        instrucao, listaInativos =algoritimos[algoritmo](tarefas, i)
        tarefas[PegarUltimaTarefa(tarefas,instrucao)]['duracaoRestante']-=1
        tarefas[PegarUltimaTarefa(tarefas,instrucao)]['ingressoTempo'] = i
        instrucoes.append(       
           CriarDadosInstrucao(instrucao, i,False)           
        )       
        
        if listaInativos:
            for u in range(len(listaInativos)):                
                    instrucoesInativas.append (
                    CriarDadosInstrucao(listaInativos[u], i,True)
                    )

    return instrucoes, instrucoesInativas


def CriarDadosInstrucao(instrucao, tempoIngresso, inativo):
    if inativo:
        cor = 0
        estado = False
    else:
        cor = instrucao['cor']  
        estado = True
    
    return{
        'nome': instrucao['nome'],
        'id': instrucao['id'], 
        'cor': cor, 
        'ingressoTarefa': instrucao['ingressoTarefa'], 
        'ingressoTempo': tempoIngresso, 
        'duracao': instrucao['duracao'], 
        'duracaoRestante': instrucao['duracaoRestante'], 
        'prioridade': instrucao['prioridade'], 
        'estado': estado,
        'eventos': instrucao['eventos']
        }

def DuracaoTotal(tarefas):
    count = 0
    for tarefa in tarefas:
        count += tarefa['duracao']
    return count

def PegarUltimaTarefa(tarefas, instrucao):
    for i in range(len(tarefas)):
        if instrucao['id'] == tarefas[i]['id']:
            return i
    return -1
    

def DefinirScrollGantt(canvasGantt, config, maxTempo, maxTid):
    largTotal = config['escalaX'] * (maxTempo + 2)
    altTotal = config['escalaY'] * (maxTid + 2)

    canvasGantt.config(scrollregion=(0,0 ,largTotal,altTotal))

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
                'cor': cor + 1,
                'ingressoTarefa': ingresso,
                'ingressoTempo' : 0,
                'duracao': duracao,
                'duracaoRestante': duracao,
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
