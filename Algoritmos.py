import sys
import json
import ast
import struct
import copy

# QUANDO TIVER TEMPO REFATORAR

# Algoritmo FIFO, Porém funcionando como RR por causa do quantum 
def FIFO(tarefas, quantum, alpha):      
    return Escalonador(tarefas, quantum, alpha, False, algoritmoSelecionado=lambda prontas: prontas[0])
        
# Algoritmo SRTF, não é afetado pelo quantum
def SRTF(tarefas, quantum, alpha):
    return Escalonador(tarefas, quantum, alpha, True, algoritmoSelecionado= lambda prontas:PegarMenorDuracao(prontas))

# Algoritmo PrioP, não é afetado pelo quantum
def PrioP(tarefas, quantum, alpha):
   return Escalonador(tarefas, quantum, alpha, True, algoritmoSelecionado=lambda prontas: PegarMaiorPrioridade(prontas))

# Algoritmo PrioEnv, não é afetado pelo quantum
def PrioEnv(tarefas, quantum,alpha):    
    return Escalonador(tarefas, quantum, alpha, True, algoritmoSelecionado=lambda prontas: PegarMaiorPrioridadeEnv(prontas))

def Escalonador(tarefas, quantum, alpha, usarCopia, algoritmoSelecionado):  
    tarefasOriginais = copy.deepcopy(tarefas) # Cria uma copia profunda das tarefas para não alterar o conteudo original
    copiaTarefas = tarefas.copy() # Cria uma copia das tarefas para não alterar o conteudo original
    tempoAtual = 0 # Tempo usado para inserir nos detalhes do bloco e controlar o LOOP WHILE
    instrucoes = [] # Lista de instrucoes contento informações uteis para gerar o gráfico
    tarefasInativas = [] # Lista para guardar as instrucoes inativas
    tarefasProntas = [] # Lista de prontas para auxiliar e facilitar na manipulação do que deve ser selecionado
    ingressouNovo = False
    eventos = PegarEventos(copiaTarefas)
    mutexEmUso = [] # Lista para guardar os mutex que estão em uso
    tarefasProntas, ingressouNovo = PegarTarefasProntas(copiaTarefas, tarefasProntas,tempoAtual,eventos, mutexEmUso) # Procura por tarefas que já estão ingressadas e possuem duracao restante
    

    while VerificarDuracoesRestantes(copiaTarefas): # Loop para garantir que a lista de instrucao gerada tenha esvaziado as duracoes das tarefas        
        removido = False # Para previnir que uma tarefa seja removida duas vezes quando o quantum acaba e a tarefa é concluída ao mesmo tempo
        for i in range(quantum): # Loop para garantir o funcionamento do quantum, sempre que ele acaba é reiniciado o processo de seleção da proxima tarefa            
            if tarefasProntas != []:            
                tarefa = algoritmoSelecionado(tarefasProntas)
                instrucoes.append(tarefa) # Adiciona a tarefa na lista de instrucoes                
                tarefasInativas.extend(PegarTarefasInativas(copiaTarefas, tarefa, tempoAtual)) # Pega e adiciona todas as tarefas que ja estao ingressados no            
                tarefa['duracaoRestante'] -= 1 # Modifica a tarefa que foi 'processado' diminuido sua duracao           
                if tarefa['duracaoRestante'] == 0:
                    tarefasProntas = [t for t in tarefasProntas if t['duracaoRestante'] > 0] 
                    removido = True
            
            tempoAtual+=1 # Aumenta o tempo atual da simulação
            ControleDeEventos(copiaTarefas, eventos, mutexEmUso, tempoAtual) # Controla os eventos de IO e Mutex

            tarefasProntas, ingressouNovo = PegarTarefasProntas(copiaTarefas, tarefasProntas,tempoAtual, eventos, mutexEmUso) # Procura por novas tarefas prontas no tempo atual atualizado,
            if tarefasProntas == []:                
                instrucoes.append({'nome': 'OCIOSO', 'id': -1, 'cor': 0, 'ingressoTarefa': -1, 'ingressoTempo': tempoAtual, 'duracao': 0, 'duracaoRestante': 0, 'tempoRelativo': 0, 'prioridade': -1, 'estado': True, 'eventos': []})
                
            if tarefa and (ingressouNovo or removido):
                if alpha > 0:                    
                    EnvelhecerPrioridades(alpha, tarefasProntas, tarefa)
                    index = next((index for (index, d) in enumerate(copiaTarefas) if d["id"] == tarefa['id']))
                    tarefa['prioridade'] = tarefasOriginais[index]['prioridade'] # Reseta a prioridade da tarefa atual para o valor original
                    ingressouNovo = False
                    removido = False
                                    
            
        if not usarCopia and len(tarefasProntas) > 0 and not removido:
            tarefasProntas.pop(0) # Remove o primeiro da lista de prontos a tarefa quando o quantum dele acaba, impedindo que ele rode até o final

    return instrucoes, tarefasInativas

def VerificarDuracoesRestantes(tarefas):
    for tarefa in tarefas:
        if ChecarDuracaoRestante(tarefa):
           return True 
    return False

def EnvelhecerPrioridades(alpha,tarefasProntas, tarefasAtual):    
    for tarefa in tarefasProntas:
        if tarefa['id'] != tarefasAtual['id']:
            tarefa['prioridade'] += alpha

def ControleDeEventos(tarefas, eventos, mutexEmUso, tempoAtual):
    AtualizarDuracaoEventos(tarefas,eventos, tempoAtual) # Atualiza a duracao dos eventos em cada tarefa pronta
    for evento in eventos:
        tipo = evento[1]['tipo']
        tarefa = next((t for t in tarefas if t['id'] == evento[0]), None)
        if tarefa and ChecarIngresso(tarefa, tempoAtual):
            if tipo == 'ML' and evento[1]['duracao'] <= 0:
                idMutex = evento[1]['mutexID']
                mutexEmUso = AdicionarMutexEmUso(mutexEmUso, idMutex)
            if tipo == 'MU' and evento[1]['duracao'] <= 0:
                idMutex = evento[1]['mutexID']
                if idMutex in mutexEmUso:
                    mutexEmUso.remove(idMutex)
    

def PegarEventos(tarefas):
    eventos = []
    for tarefa in tarefas:
        if tarefa['eventos']:
            for evento in tarefa['eventos']:
                eventos.append((tarefa['id'],evento))
    return eventos

def AdicionarMutexEmUso(mutexEmUso, idMutex):
    if idMutex not in mutexEmUso:
        mutexEmUso.append(idMutex)
    return mutexEmUso

# Funcao para atualizar a duracao dos eventos em cada tarefa pronta
def AtualizarDuracaoEventos(tarefas,eventos, tempoAtual):    
    if eventos:
        for evento in eventos:
            tipo = evento[1]['tipo']
            tarefa = next((t for t in tarefas if t['id'] == evento[0]), None)
            if tarefa and ChecarIngresso(tarefa, tempoAtual):
                if tipo in ['ML','MU'] or (tipo == 'IO' and evento[1]['inicio'] <= 0):
                    evento[1]['duracao'] -= 1
                else:
                    evento[1]['inicio'] -= 1
                
def BloquearPorEventos(eventos, mutexEmUso, idTarefa):
    if eventos:
        for evento in eventos:    
            if evento[0] == idTarefa:
                tipo = evento[1]['tipo']
                if tipo == 'IO' and evento[1]['inicio'] <= 0 and evento[1]['duracao'] > 0:
                    return True # Bloqueia a tarefa
                elif tipo == 'ML':
                    return True if evento[1]['mutexID'] in mutexEmUso else False
    return False
    
        

# Funcao para buscar por tarefas ingressadas e contendo duracao restante
def PegarTarefasProntas(tarefas, tarefasProntas, tempoAtual, eventos=None, mutexEmUso=None):
    
    # Faz uma copia das tarefas prontas existente para não altera-la ao retornar,
    # Necessário para o funcionamento correto de uma FILA para o FIFO
    prontas = list(tarefasProntas)
    ingressouNovo = False
    # Condição para remover tarefas conlcuidas com duracao restante em 0
    # Necesssário para o funcionamento do SRTF e PrioP
    
    prontas = [t for t in prontas if t['duracaoRestante'] > 0]        
    idsProntas = [t['id'] for t in prontas] # Lista para guardar os IDs das tarefas já presentes na lista de prontas
    # Loop para buscar por tarefas ingressadas e com duracao restante, evitando também tarefas iguais
    for tarefa in tarefas:
        if tarefa['id'] not in idsProntas and ChecarIngresso(tarefa, tempoAtual) and tarefa['duracaoRestante'] > 0:
            if not BloquearPorEventos(eventos, mutexEmUso, tarefa['id']):                
                prontas.append(tarefa) # Adiciona a tarefa na lista de prontas caso passe nas condições
        if tarefa['ingressoTarefa'] == tempoAtual:
            ingressouNovo = True
    
    return prontas, ingressouNovo

# Funcao para buscar por tarefas no tempo atual mas inativas
def PegarTarefasInativas(tarefas, tarefaAtiva,tempoAtual):    
    instrucoesInativas = [] # variável para guardar uma lista das instrucoes inativas
    for tarefa in tarefas: # Percorre pela lista de tarefas
        if tempoAtual >= tarefa['ingressoTarefa']: # Verifica se ele já está ingressado
            if tarefa['id'] != tarefaAtiva['id']: # Verifica se ele não é a tarefa ativa atual
                if ChecarDuracaoRestante(tarefa): # Verifica se ele ainda tem duracao restante
                    copiaTarefa = tarefa.copy() # Faz uma copia da tarefa para evitar de modificar a original
                    copiaTarefa['ingressoTempo'] = tempoAtual # Modifica o seu tempo de ingresso para ser utilizado corretamente no desenho do bloco no gráfico
                    instrucoesInativas.append(copiaTarefa) # Adiciona ele na lista com a modificação feita
    return instrucoesInativas

# Funcao para pegar a tarefa de maior prioridade dentro de uma lista de tarefas prontas
def PegarMaiorPrioridade(tarefas):  
    maiorPrioridade = tarefas[0] # pega o primeiro para usar como comparação
        
    for tarefa in tarefas: # Loop para percorrer pela lista de prontos
        if ChecarDuracaoRestante(tarefa): # Verifica se ainda tem duracao restante
            maiorPrioridade = CompararMaiorPrioridade(tarefa, maiorPrioridade) # Atribui a tarefa de maior prioridade            
    return maiorPrioridade

def PegarMaiorPrioridadeEnv(tarefas):  
    maiorPrioridade = tarefas[0] # pega o primeiro para usar como comparação
        
    for tarefa in tarefas: # Loop para percorrer pela lista de prontos
        if ChecarDuracaoRestante(tarefa): # Verifica se ainda tem duracao restante
            maiorPrioridade = CompararMaiorPrioridade(tarefa, maiorPrioridade) # Atribui a tarefa de maior prioridade  
            t1,t2 = CompararIgualPrioridade(tarefa, maiorPrioridade)
            if t1 and t2:
                maiorPrioridade = DesempatePorID(t1, t2)

    return maiorPrioridade
# Funcao para pegar a tarefa de menor duracao restante dentro de uma lista de tarefas prontas
def PegarMenorDuracao(tarefas):
    menorDuracao = tarefas[0] # pega o primeiro para usar como comparação
    for tarefa in tarefas: # Loop para percorrer pela lista de prontos
        if ChecarDuracaoRestante(tarefa): # Verifica se ainda tem duracao restante
            menorDuracao = CompararMenorDuracao(tarefa, menorDuracao) # Atribui a tarefa de maior prioridade   
    return menorDuracao

# Funcao para retornar True ou False se ele tiver duracao restante
def ChecarDuracaoRestante(tarefa): 
    return tarefa['duracaoRestante'] > 0

# Funcao para retornar  True ou False se ele ja tiver ingressado em relação ao tempo atual
def ChecarIngresso(tarefa, tempoAtual):
    return tarefa['ingressoTarefa'] <= tempoAtual

# Funcao para devolver a tarefa contendo a menor duração
def CompararMenorDuracao(tarefa1, tarefa2):
    return tarefa1 if tarefa1['duracaoRestante'] < tarefa2['duracaoRestante'] else tarefa2

# Funcao para devolver a tarefa com maior prioridade
def CompararMaiorPrioridade(tarefa1, tarefa2):
    return tarefa1 if tarefa1['prioridade'] > tarefa2['prioridade'] else tarefa2

def CompararIgualPrioridade(tarefa1, tarefa2):
    return tarefa1,tarefa2 if tarefa1['prioridade'] == tarefa2['prioridade'] else None

def DesempatePorID(tarefa1, tarefa2):
    return tarefa1 if tarefa1['id'] > tarefa2['id'] else tarefa2