import sys
import json
import ast
import struct

# INVERTER A LÓGICA: COMEÇAR GERANDO TAREFAS PRONTAS E ENVIAR PARA ANALISE PARA DETERMINAR QUAL A PROXIMA TAREFA
# ATUALMENTE: CRIA UMA LISTA PRONTA PARA GERAR AS BARRAS, PROBLEMAS COM ALGORITMOS PREEMPTIVOS

def FIFO(tarefas, tempoMax, quantum):  
    copiaTarefas = tarefas.copy()
    tempoAtual = 0
    instrucoes = []    
    tarefasInativas = []
    tarefasProntas = []
    tarefasProntas = PegarTarefasProntas(copiaTarefas, tarefasProntas,tempoAtual, False)      
    while (tempoAtual < tempoMax):                  
        for i in range(quantum):
            if ChecarDuracaoRestante(tarefasProntas[0]):                
                instrucoes.append(tarefasProntas[0])
                tarefasInativas.extend(PegarTarefasInativas(copiaTarefas, tarefasProntas[0], tempoAtual))                
                tarefasProntas[0]['duracaoRestante'] -= 1     
                tempoAtual+=1
                tarefasProntas = PegarTarefasProntas(copiaTarefas, tarefasProntas,tempoAtual, False)      
                for i in range(len(tarefasProntas)):
                    print(tarefasProntas[i])
                print("-------------")
            
        tarefasProntas.pop(0)

    return instrucoes, tarefasInativas
        

def SRTF(tarefas, tempoMax, quantum):
    copiaTarefas = tarefas.copy()
    tempoAtual = 0
    instrucoes = []
    tarefasProntas = []
    tarefasProntas = PegarTarefasProntas(copiaTarefas, tarefasProntas,tempoAtual, True)  
    tarefasInativas = []
    while tempoAtual < tempoMax:        
        for q in range(quantum):            
            menorDuracao = PegarMenorDuracao(tarefasProntas)            
            instrucoes.append(menorDuracao)       
            tarefasInativas.extend(PegarTarefasInativas(copiaTarefas, menorDuracao, tempoAtual))
            menorDuracao['duracaoRestante'] -= 1
            tempoAtual +=1
            tarefasProntas = PegarTarefasProntas(copiaTarefas, tarefasProntas,tempoAtual, True)    

    return instrucoes, tarefasInativas


def PrioP(tarefas, tempoMax, quantum):
    copiaTarefas = tarefas.copy()
    tempoAtual = 0
    instrucoes = []
    tarefasProntas = []
    tarefasProntas = PegarTarefasProntas(copiaTarefas, tarefasProntas,tempoAtual, True)  
    tarefasInativas = []
    while tempoAtual < tempoMax:
        for q in range(quantum):                  
            maiorPrio = PegarMaiorPrioridade(tarefasProntas)
            instrucoes.append(maiorPrio)
            tarefasInativas.extend(PegarTarefasInativas(copiaTarefas, maiorPrio, tempoAtual))
            maiorPrio['duracaoRestante'] -= 1
            tempoAtual +=1
            tarefasProntas = PegarTarefasProntas(copiaTarefas, tarefasProntas, tempoAtual, True)
            
    return instrucoes, tarefasInativas

def PegarTarefasProntas(tarefas, tarefasProntas, tempoAtual, apagarConcluidas):
    prontas = tarefasProntas.copy()
    if apagarConcluidas:
        prontas = [t for t in prontas if t['duracaoRestante'] != 0]  # Remove tarefas que já foram concluídas
    idsProntas = {tarefa['id'] for tarefa in prontas}

    for i in range (len(tarefas)):
        if ChecarIngresso(tarefas[i], tempoAtual) and ChecarDuracaoRestante(tarefas[i]) and tarefas[i]['id'] not in idsProntas:
            prontas.append(tarefas[i])

   
    return prontas

def PegarTarefasInativas(tarefas, tarefaAtiva,tempoAtual):
    tarefasInativa = []
    for tarefa in tarefas:
        if tempoAtual >= tarefa['ingressoTarefa']  :
            if tarefa['id'] != tarefaAtiva['id']:
                if ChecarDuracaoRestante(tarefa):
                    copiaTarefa = tarefa.copy()
                    copiaTarefa['ingressoTempo'] = tempoAtual
                    tarefasInativa.append(copiaTarefa)
    return tarefasInativa

def PegarMaiorPrioridade(tarefas):  
    maiorPrioridade = tarefas[0]
    for tarefa in tarefas:     
        if ChecarDuracaoRestante(tarefa):              
            maiorPrioridade = CompararPrioridade(tarefa, maiorPrioridade)    

    return maiorPrioridade

def PegarMenorDuracao(tarefas):
    menorDuracao = tarefas[0]
    for tarefa in tarefas:    
        if ChecarDuracaoRestante(tarefa):
            menorDuracao = CompararDuracao(tarefa, menorDuracao)    
    return menorDuracao

def ChecarQuantum(instrucaoAnterior):
    return True if instrucaoAnterior['quantumRestante'] > 0 else False

def ChecarDuracaoRestante(tarefa):    
    return tarefa['duracaoRestante'] > 0

def ChecarIngresso(tarefa, tempoAtual):
    return tarefa['ingressoTarefa'] <= tempoAtual

def PegarMenorIngresso(tarefa1, tarefa2):
    return tarefa1 if tarefa1['ingressoTarefa'] < tarefa2['ingressoTarefa'] else tarefa2

def CompararDuracao(tarefa1, tarefa2):
    return tarefa1 if tarefa1['duracaoRestante'] < tarefa2['duracaoRestante'] else tarefa2


def CompararPrioridade(tarefa1, tarefa2):
    return tarefa1 if tarefa1['prioridade'] > tarefa2['prioridade'] else tarefa2



