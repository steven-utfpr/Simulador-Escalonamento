import sys
import json
import ast
import struct

# INVERTER A LÓGICA: COMEÇAR GERANDO TAREFAS PRONTAS E ENVIAR PARA ANALISE PARA DETERMINAR QUAL A PROXIMA TAREFA
# ATUALMENTE: CRIA UMA LISTA PRONTA PARA GERAR AS BARRAS, PROBLEMAS COM ALGORITMOS PREEMPTIVOS

def FIFO(tarefas, tempoAtual):
    for i in range(len(tarefas)):
        if ChecarDuracao(tarefas[i]):            
            tarefasInativas = PegarTarefasInativas(tarefas, tarefas[i], tempoAtual)            
            return tarefas[i], tarefasInativas

def SRTF(tarefas, tempoAtual):
    ingressados = []
    for i in range(len(tarefas)):
        if ChecarIngresso(tarefas[i], tempoAtual) and ChecarDuracao(tarefas[i]):
            tarefasInativas = PegarTarefasInativas(tarefas, tarefas[i], tempoAtual) 
            ingressados.append(tarefas[i])    

    return PegarMenorDuracao(ingressados), tarefasInativas


def PrioP(tarefas, tarefasProntas):
    print("Executando PrioP")

def ChecarDuracao(tarefa):    
    return tarefa['duracaoRestante'] > 0

def ChecarIngresso(tarefa, tempoAtual):
    return tarefa['ingressoTarefa'] <= tempoAtual

def PegarDuracao(tarefa1, tarefa2):
    return tarefa1 if tarefa1['duracaoRestante'] < tarefa2['duracaoRestante'] else tarefa2

def PegarMenorDuracao(tarefas):
    menorDuracao = tarefas[0]
    for tarefa in tarefas:                   
        menorDuracao = PegarDuracao(tarefa, menorDuracao)
    return menorDuracao

def PegarTarefasInativas(tarefas, tarefaAtiva,tempoAtual):
    tarefasInativa = []
    for tarefa in tarefas:
        if tempoAtual >= tarefa['ingressoTarefa']  :
            if tarefa['id'] != tarefaAtiva['id']:
                if ChecarDuracao(tarefa):
                    tarefasInativa.append(tarefa)
    return tarefasInativa

