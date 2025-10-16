import sys
import json
import ast
import struct

# INVERTER A LÓGICA: COMEÇAR GERANDO TAREFAS PRONTAS E ENVIAR PARA ANALISE PARA DETERMINAR QUAL A PROXIMA TAREFA
# ATUALMENTE: CRIA UMA LISTA PRONTA PARA GERAR AS BARRAS, PROBLEMAS COM ALGORITMOS PREEMPTIVOS

def FIFO(tarefas, tempoAtual):
    for i in range(len(tarefas)):
        tarefasInativas = PegarTarefasInativas(tarefas, tarefas[i], tempoAtual)   
        if ChecarDuracao(tarefas[i]):
            return tarefas[i], tarefasInativas

def SRTF(tarefas, tempoAtual):
    ingressados = []
    for i in range(len(tarefas)):                  
        if ChecarIngresso(tarefas[i], tempoAtual) and ChecarDuracao(tarefas[i]):        
            ingressados.append(tarefas[i]) 
        
    menorDuracao = PegarMenorDuracao(ingressados)        
    tarefasInativas = PegarTarefasInativas(tarefas, menorDuracao, tempoAtual)

    return menorDuracao, tarefasInativas


def PrioP(tarefas, tempoAtual):
    ingressados = []
    for i in range(len(tarefas)):                  
        if ChecarIngresso(tarefas[i], tempoAtual) and ChecarDuracao(tarefas[i]):        
            ingressados.append(tarefas[i])     
        
        
    maiorPrioridade = PegarMaiorPrioridade(ingressados)
    tarefasInativas = PegarTarefasInativas(tarefas, maiorPrioridade, tempoAtual)
    
    return maiorPrioridade, tarefasInativas

def ChecarDuracao(tarefa):    
    return tarefa['duracaoRestante'] > 0

def ChecarIngresso(tarefa, tempoAtual):
    return tarefa['ingressoTarefa'] <= tempoAtual

def CompararDuracao(tarefa1, tarefa2):
    return tarefa1 if tarefa1['duracaoRestante'] < tarefa2['duracaoRestante'] else tarefa2

def CompararPrioridade(tarefa1, tarefa2):
    return tarefa1 if tarefa1['prioridade'] > tarefa2['prioridade'] else tarefa2

def PegarMaiorPrioridade(tarefas):  
    maiorPrioridade = tarefas[0]
    for tarefa in tarefas:                   
        maiorPrioridade = CompararPrioridade(tarefa, maiorPrioridade)
    return maiorPrioridade

def PegarMenorDuracao(tarefas):
    menorDuracao = tarefas[0]
    for tarefa in tarefas:                   
        menorDuracao = CompararDuracao(tarefa, menorDuracao)
    return menorDuracao

def PegarTarefasInativas(tarefas, tarefaAtiva,tempoAtual):
    tarefasInativa = []
    for tarefa in tarefas:
        if tempoAtual >= tarefa['ingressoTarefa']  :
            if tarefa['id'] != tarefaAtiva['id']:
                if ChecarDuracao(tarefa):
                    tarefasInativa.append(tarefa)
                    
    return tarefasInativa

