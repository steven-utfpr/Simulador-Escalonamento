import sys
import json
import ast
import struct

def FIFO(tarefas):
    instrucoes = []
    ordenarIngresso = sorted(tarefas, key=lambda x: x['ingresso'])
    contador = 0
    duracaoOriginal = 0
    for tarefa in ordenarIngresso:          
        duracaoOriginal = tarefa['duracao']
        for i in range(tarefa['duracao']):
            tarefa['duracao']-=1
            instrucoes.append (
            {
                'nome': tarefa['nome'],
                'id': tarefa['id'],
                'cor': tarefa['cor'],
                'ingressoTempo': contador,
                'tempoRestante': tarefa['duracao'],
                'duracao': duracaoOriginal,
                'prioridade': tarefa['prioridade'],
                'eventos': tarefa['eventos']
            }
            )
            contador+=1    
    #for i in range(len(instrucoes)):
        #print(instrucoes[i])
    return instrucoes

def SRTF(self, tarefas):
    print("Executando SRTF")

def PrioP(self, tarefas):
    print("Executando PrioP")

def SelCondicao(tipo, tarefas):
    if tipo == "prioridade":
        return 0
    elif tipo == "duracao":
        return 1
    elif tipo == "restante":
        return 2
    