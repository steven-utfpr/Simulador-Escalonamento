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
#. COMENTAR O CÓDIGO E FAZER DOCUMENTAÇÃO
import sys
import json
import ast
import struct

import matplotlib.pyplot as plt
import tkinter as tk
from Janelas import CriarInterface
from Funcoes import LerArquivo, SelArquivo, WriteLockBox, GerarInstrucoes,ProcessarDados, AtualizarLog,DefinirScrollGantt
from Grafico import GerarGrafico, CriarBarra, ApagarBarra, cores
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

        self.instrucoes, self.instrucoesInativos = GerarInstrucoes(self.algoritmo, self.tarefas, self.quantum)
        self.maxTempo = len(self.instrucoes) 
        self.maxTid = len(self.tarefas)
        DefinirScrollGantt(self.canvasGantt, self.graficoConfig, self.maxTempo, self.maxTid)
        
        GerarGrafico(self.canvasGantt, self.graficoConfig, self.instrucoes, self.instrucoesInativos, self.maxTempo, self.maxTid, self.usarPasso, self.PegarInfoBarra)
        
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

    def PegarInfoBarra(self,instrucao):
        
        if instrucao['estado']:
            estado = "Em Execução"
        else:
            estado = "Inativo"

        info = f"""\
   DETALHES DA TAREFA
────────────────────────────
Tarefa: T{instrucao['id'] + 1}| Algoritmo: {self.algoritmo} | Quantum: {self.quantum} | Estado: {estado} 
Tempo Ingresso: {instrucao['ingressoTempo']} | Tempo Processado: {instrucao['duracaoRestante']} | Quantum Restante: {instrucao['quantumRestante']}
Duração Total: {instrucao['duracao']} | Prioridade: {instrucao['prioridade']} | Cor (índice): {instrucao['cor']}
────────────────────────────
"""
        AtualizarLog(self.logBox, info)
    
    def AvancarPasso(self):       
        if self.tarefas and self.usarPasso:    
            if(self.tempoAtual < len(self.instrucoes)): 
                self.CriarBarras()
                self.tempoAtual += 1                                
                self.infoTempoAtual.set(f"Tempo: {self.tempoAtual}" )
                WriteLockBox(self.tempoAtualEntry, self.tempoAtual)
                
    def CriarBarras(self):
        
        self.barra, self.barraText = CriarBarra(
                    self.canvasGantt, 
                    self.graficoConfig, 
                    self.instrucoes[self.tempoAtual], 
                    self.maxTid, 

                    self.PegarInfoBarra)
        self.barraID.append(
            {
                'barra' : self.barra,
                'barraText' : self.barraText,
                'tempo' : self.tempoAtual
            }
        )

        for i in range(len(self.instrucoesInativos)):
            if self.instrucoesInativos[i]['ingressoTempo'] == self.tempoAtual:
                self.barra, self.barraText = CriarBarra(
                    self.canvasGantt, 
                    self.graficoConfig, 
                    self.instrucoesInativos[i], 
                    self.maxTid, 

                    self.PegarInfoBarra)
                
                self.barraID.append(
                    {
                        'barra' : self.barra,
                        'barraText' : self.barraText,
                        'tempo' : self.tempoAtual
                    }
                )

    def ApagarBarras():
        return 0

    def VoltarPasso(self):
        if self.tarefas and self.usarPasso:
            if(self.tempoAtual > 0):       
                    
                for i in range(len(self.barraID)):                    
                    if self.barraID[i]['tempo'] == self.tempoAtual-1:                    
                        ApagarBarra(self.canvasGantt,self.barraID[i]['barra'], self.barraID[i]['barraText'])

                self.barraID = [t for t in self.barraID if t['tempo'] != self.tempoAtual-1]
                
                self.tempoAtual -=1  
                self.infoTempoAtual.set(f"Tempo: {self.tempoAtual}" )
                WriteLockBox(self.tempoAtualEntry, self.tempoAtual) 
    
    def SalvarDiagrama(self):
        self.IniciarSimulacao()
        self.instrucoesUnidas = self.instrucoes + self.instrucoesInativos
        # Dados de exemplo
        tarefas = []
        inicio = []
        duracao = []
        tCores = []

        totalTarefas = len(self.tarefas)
        tempoMax = len(self.instrucoes)

        self.instrucoesUnidas = sorted(self.instrucoesUnidas, key=lambda x:x['id'])

        for i in range(len(self.instrucoesUnidas)):
            tarefas.append(f"T{self.instrucoesUnidas[i]['id']}")
            duracao.append(1)
            inicio.append(self.instrucoesUnidas[i]['ingressoTempo'])
            tCores.append(cores[self.instrucoesUnidas[i]['cor']])
        
        fig, ax = plt.subplots(figsize=(tempoMax, totalTarefas))

        # Gera gráfico
        ax.barh(tarefas, duracao, left=inicio, color=tCores, edgecolor='black')
        
        for i in range(len(tarefas)):
            ax.text(inicio[i] + duracao[i]/2, tarefas[i], f"T{self.instrucoesUnidas[i]['id']}", va='center', ha='center', color='black', fontweight='bold', fontsize=9)
        
        plt.xlim(0,tempoMax) # Remove o vão que ficaria na geração da imagem no último tempo
        plt.xticks(range(0,tempoMax+1)) # Faz com que o gráfico mostre todos os números no eixo do tempo ao invés de 2 em 2
        plt.xlabel('Tempo')
        plt.title(f"Gráfico de Gantt: {self.algoritmo}")

        # Salva como imagem
        plt.savefig('gantt.png', dpi=150, bbox_inches='tight')
        plt.close()

simulador = SimulEscal()
        

        

