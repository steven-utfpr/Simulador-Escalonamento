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

""" def FIFO(tarefas):
    instrucoes = []
    ordenarIngresso = sorted(tarefas, key=lambda x: x['ingressoTarefa'])
    contador = 0
    duracaoOriginal = 0
    for tarefa in ordenarIngresso:          
        duracaoOriginal = tarefa['duracao']
        for i in range(tarefa['duracao']):
            tarefa['duracao']-=1
            instrucoes.append(AdicionarInstrucao(tarefa, contador,duracaoOriginal,False))
            contador+=1    
    #for i in range(len(instrucoes)):
        #print(instrucoes[i])
    for i in range(len(tarefas)):
        print(tarefas[i])
    return instrucoes """

def SRTF(tarefas, tarefasProntas):
    instrucoes = []
    contador = 0
    duracaoOriginal = 0
    ordenarIngresso = sorted(tarefas, key=lambda x: x['ingressoTarefa'])    
    for tarefa in ordenarIngresso:          
        duracaoOriginal = tarefa['duracao']
        for i in range(tarefa['duracao']):
            return 0
    return instrucoes  

def PrioP(tarefas, tarefasProntas):
    print("Executando PrioP")

def AdicionarInstrucao(tarefa, contador, duracaoOriginal, usarCorBranca):
    if usarCorBranca:
        i = 0
    else: 
        i =tarefa['cor']
    return {
            'nome': tarefa['nome'],
            'id': tarefa['id'],
            'cor': i,
            'ingressoTempo': contador,
            'tempoRestante': tarefa['duracao'],
            'duracao': duracaoOriginal,
            'prioridade': tarefa['prioridade'],
            'eventos': tarefa['eventos']
            }

def Ordenar(tipo, tarefas):
    if tipo == "prioridade":
        return sorted(tarefas, key=lambda x: x['prioridade'], reverse=True)
    elif tipo == "duracao":
        return sorted(tarefas, key=lambda x: x['duracao'])
    elif tipo == "ingresso":
        return sorted(tarefas, key=lambda x: x['ingresso'])

def ChecarDuracao(tarefa):    
    return tarefa['duracaoRestante'] > 0

def TemIngressoIguais(tarefas, tempo):
    cont = [0] * len(tarefas)
    for tarefa in tarefas:
        cont[tarefa['ingressoTarefa']-1]+=1
        
    if cont[tempo] > 1:
        return True
    return False       

def PegarTarefasInativas(tarefas, tarefaAtiva,tempoAtual):
    tarefasInativa = []
    for tarefa in tarefas:
        if tempoAtual >= tarefa['ingressoTarefa']  :
            if tarefa['id'] != tarefaAtiva['id']:
                if ChecarDuracao(tarefa):
                    tarefasInativa.append(tarefa)
    return tarefasInativa


def SelecionarTarefa(tarefas, itemComparar, pegarMaior):    
    var = tarefas[0][itemComparar]
    print(var)
    for tarefa in tarefas:
        if pegarMaior:
            if var > tarefa[itemComparar]:
                var = tarefa
        else:
            if var < tarefa[itemComparar]:
                var = tarefa
    return tarefa
