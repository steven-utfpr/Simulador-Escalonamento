#+----------------------+----------------------------------+
#|  [CONFIGURAÇÕES]     |                                  |
#|                      |                                  |
#|  Algoritmo: [▼]      |                                  |
#|  Arquivo:   [_____]  |                                  |
#|  [ Iniciar]        |       ÁREA DO GRÁFICO DE        |
#|                      |            GANTT                 |
#|                      |                                  |
#|                      |                                  |
#+----------------------+----------------------------------+
#|                   LOG DA SIMULAÇÃO                      |
#|  - Iniciado...                                          |
#|  - Tarefa 1 executou...                                 |
#+----------------------------------------------------------+
import sys
import json
import ast
import struct

import tkinter as tk
from Janelas import CriarInterface
from Funcoes import LerArquivo, SelArquivo, WriteLockBox, GerarInstrucoes,ProcessarDados, AtualizarLog,DefinirScrollGantt
from Grafico import GerarGrafico, CriarBarra, ApagarBarra
from Algoritmos import FIFO, SRTF, PrioP

class SimulEscal:
    def __init__(self):
        self.usarPasso = False
        self.barraID = []
        self.caminhoArq = None  
        self.maxTempo = 0
        self.tempoAtual = 0
       
        self.graficoConfig = {
            'escalaX': 50, # Define a largura de cada unidade de tempo no eixo X
            'escalaY': 25, # Define a altura de cada barra de tarefa no gráfico de preferencia colocar escalaX/2
        }

        self.root, self.frameInfo, self.logBox, self.frameConfig, self.frameGantt, self.canvasGantt, self.tempoAtualEntry,  self.arqAtualEntry = CriarInterface(self)
        
            
        if self.root:            
            self.root.mainloop()

    def IniciarSimulacao(self):        
               
        if self.caminhoArq is not None:
            texto = LerArquivo(self.caminhoArq)
            self.tarefas, self.algoritmo, self.quantum = ProcessarDados(texto)
            
        else:
            self.tarefas, self.algoritmo, self.quantum = self.UsarConfigPadrao()            

        self.instrucoes, self.instrucoesInativos = GerarInstrucoes(self.algoritmo, self.tarefas)
        self.maxTempo = len(self.instrucoes) 
        self.maxTid = len(self.tarefas)
        DefinirScrollGantt(self.canvasGantt, self.graficoConfig, self.maxTempo, self.maxTid)
        
        GerarGrafico(self.canvasGantt, self.graficoConfig, self.instrucoes, self.instrucoesInativos, self.maxTempo, self.maxTid, self.usarPasso,self.PegarInfoBarra)
        self.AtualizarInfos()

    def AtualizarInfos(self):
        self.infoAlgo.set(f"Algoritmo: {self.algoritmo}")
        self.infoQuantum.set(f"Quantum: {self.quantum}")

    def UsarConfigPadrao(self):
        tarefas = []
        configPadrao = 'FIFO;2\n', 't01;0;0;5;2;\n', 't02;1;0;2;3;\n', 't03;2;1;4;1;\n', 't04;3;3;1;4;\n', 't05;4;5;2;5;\n'
        tarefas, algoritmo, quantum = ProcessarDados(configPadrao)
       
        return tarefas, algoritmo, quantum

    def PegarCaminho(self):
        self.caminhoArq = SelArquivo(self.arqAtualEntry)

    def CheckPasso(self):
        self.usarPasso = not self.usarPasso
        self.tempoAtual=0
        self.IniciarSimulacao()

    def PegarInfoBarra(self,tid, tempo):
        info = f"""\
   DETALHES DA TAREFA
────────────────────────────
Tarefa: T{tid + 1}| Algoritmo: {self.algoritmo} | Quantum: {self.quantum}
Estado: {self.instrucoes[tempo]['estado']} 
Tempo Ingresso: {self.instrucoes[tempo]['ingressoTempo']} | Tempo Restante: {self.instrucoes[tempo]['duracaoRestante']}
Duração Total: {self.instrucoes[tempo]['duracao']} | Prioridade: {self.instrucoes[tempo]['prioridade']} | Cor (índice): {self.instrucoes[tempo]['cor']}
────────────────────────────
"""
        AtualizarLog(self.logBox, info)
    
    def AvancarPasso(self):       
        if self.tarefas and self.usarPasso:    
            if(self.tempoAtual < len(self.instrucoes)): 
                self.barra, self.barraText = CriarBarra(
                    self.canvasGantt, 
                    self.graficoConfig, 
                    self.tempoAtual, 
                    self.maxTid, 
                    self.instrucoes[self.tempoAtual]['id']-1, 
                    self.instrucoes[self.tempoAtual]['cor']+1, 
                    self.PegarInfoBarra)
                self.barraID.append(
                    {
                        'barra' : self.barra,
                        'barraText' : self.barraText
                    }
                )                
                self.tempoAtual += 1                                
                self.infoTempoAtual.set(f"Tempo: {self.tempoAtual}" )
                WriteLockBox(self.tempoAtualEntry, self.tempoAtual)
                
    
    def VoltarPasso(self):
        if self.tarefas and self.usarPasso:
            if(self.tempoAtual > 0):                               
                ApagarBarra(self.canvasGantt,self.barraID, self.tempoAtual-1)   
                self.tempoAtual -=1  
                self.infoTempoAtual.set(f"Tempo: {self.tempoAtual}" )
                WriteLockBox(self.tempoAtualEntry, self.tempoAtual) 
    
simulador = SimulEscal()
        

        

