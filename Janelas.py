import tkinter as tk
from tkinter import filedialog

import Grafico
from Funcoes import WriteLockBox

def CriarInterface(self):
    # Objeto janela
    janelaPrincipal = tk.Tk()
    # Titulo da janela
    janelaPrincipal.title("Simulador SO") 
    # Definindo o tamanho 
    janelaPrincipal.geometry ("800x600")

    frameInfo, logBox = CriarTelaInfos(janelaPrincipal)
    frameConfig, tempoAtualEntry, arqAtualEntry = CriarTelaConfig(self,janelaPrincipal)
    frameGantt, canvasGantt = CriarTelaGantt(janelaPrincipal)

    return janelaPrincipal, frameInfo, logBox, frameConfig, frameGantt, canvasGantt, tempoAtualEntry, arqAtualEntry

def CriarTelaConfig(self,root):
    
    frame = tk.Frame(root, width=200, height=600, bg="lightgray", padx=10, pady=10)
    frame.pack(side="left", fill="y")
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)
    
    # Conteúdo do painel esquerdo
    tituloConfig = tk.Label(frame, text="Configurações", font=("Arial", 12), bg="lightgray")
    btnIniciar = tk.Button(frame, text="Iniciar", command= self.IniciarSimulacao, bg="green", fg="white", width=10, height=2)
    tituloArqSel = tk.Label(frame, text="Arquivo Selecionado:", bg="lightgray")
    
    arqAtualEntry = tk.Entry(frame, width=20)
    WriteLockBox(arqAtualEntry, "config.txt")
        
    btnProcurar = tk.Button(frame, text="Procurar", command= self.PegarCaminho, font=("Arial", 12))      
        
    checkboxPasso = tk.Checkbutton(frame, text="Passo a Passo", command=lambda: self.CheckPasso())
    btnAvanc = tk.Button(frame, text=">", command=lambda: self.AvancarPasso(), bg="green", fg="white", width=3)
    btnVolta = tk.Button(frame, text="<", command=lambda: self.VoltarPasso(), bg="green", fg="white", width=3)        
    
    campoTempoAtual = tk.Entry(frame, width=5)
    campoTempoAtual.insert(0,"0")
    
    
    self.infoAlgo = tk.StringVar()
    self.infoAlgo.set("Algoritmo:")
    self.infoQuantum = tk.StringVar()
    self.infoQuantum.set("Quantum:")
    self.infoTempoAtual = tk.StringVar()
    self.infoTempoAtual.set(f"Tempo: {self.tempoAtual}" )
    
    infoAlgo = tk.Label(frame, textvariable=self.infoAlgo, font=("Arial", 12), bg="lightgray")
    infoQuantum = tk.Label(frame, textvariable=self.infoQuantum, font=("Arial", 12), bg="lightgray")
    infoTempoAtual = tk.Label(frame, textvariable=self.infoTempoAtual, font=("Arial", 12), bg="lightgray")

    tituloConfig.grid(row=0, column=0, padx=2, pady=5)
    btnIniciar.grid(row=1, column=0, padx=2, pady=5, )
    tituloArqSel.grid(row=2, column=0, padx=2, pady=5)
    arqAtualEntry.grid(row=3, column=0, padx=2, pady=5)
    btnProcurar.grid(row=4, column=0, padx=1, pady=5) 

    btnAvanc.grid(row=5, column=0, padx=2, pady=5, sticky="e")
    btnVolta.grid(row=5, column=0, padx=2, pady=5, sticky="w")
    campoTempoAtual.grid(row=5, column=0, padx=2, pady=5)    
    checkboxPasso.grid(row=6, column=0, padx=2, pady=5)

    infoAlgo.grid(row=7, column=0, padx=2, pady=5)
    infoQuantum.grid(row=8, column=0, padx=2, pady=5)
    infoTempoAtual.grid(row=9, column=0, padx=2, pady=5)    

    return frame, campoTempoAtual, arqAtualEntry

def CriarTelaGantt(root):
    """Cria o painel direito com gráfico de Gantt com borda externa (como no exemplo)"""
    frame = tk.Frame(root, width=600, height=400, bg="lightgray", padx=10, pady=10)
    frame.pack(side="right", fill="both", expand=True)

    tk.Label(frame, text="Gráfico de Gantt", font=("Arial", 12),bg="lightgray").pack()

    canvas = tk.Canvas(frame, bg="white", height=400)
    canvas.pack(fill="both", expand=True)
    
    return frame, canvas

def CriarTelaInfos(root):
    """Cria o painel inferior para logs"""
    frame = tk.Frame(root, height=100, bg="black", padx=10, pady=10)
    frame.pack(side="bottom", fill="x")

    tk.Label(frame, text="Log da Simulação", fg="white", bg="black").pack()

    log = tk.Text(frame, height=4, bg="black", fg="lime", font=("Courier", 10))
    log.pack(fill="both", expand=True)

    scroll = tk.Scrollbar(log, orient="vertical", command=log.yview)
    scroll.pack(side="right", fill="y")
    log.config(yscrollcommand=scroll.set)

    return root, log

def CriarTelaTarefas(root):
    return 0

