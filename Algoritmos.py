import sys
import json
import ast
import struct
import copy

# QUANDO TIVER TEMPO REFATORAR

# Algoritmo FIFO, Porém funcionando como RR por causa do quantum 
def FIFO(tarefas, tempoMax, quantum, alpha):  
    copiaTarefas = tarefas.copy() # Cria uma copia das tarefas para não alterar o conteudo original
    tempoAtual = 0 # Tempo usado para inserir nos detalhes do bloco e controlar o LOOP WHILE
    instrucoes = [] # Lista de instrucoes contento informações uteis para gerar o gráfico
    tarefasInativas = [] # Lista para guardar as instrucoes inativas
    tarefasProntas = [] # Lista de prontas para auxiliar e facilitar na manipulação do que deve ser selecionado
    tarefasProntas = PegarTarefasProntas(copiaTarefas, tarefasProntas,tempoAtual, False) # Procura por tarefas que já estão ingressadas e possuem duracao restante
    while tempoAtual < tempoMax: # Loop para garantir que a lista de instrucao gerada tenha esvaziado as duracoes das tarefas
        for i in range(quantum): # Loop para garantir o funcionamento do quantum, sempre que ele acaba é reiniciado o processo de seleção da proxima tarefa
            if ChecarDuracaoRestante(tarefasProntas[0]): # Verifica se primeira tarefa na fila de prontas ainda tem duracao restante
                instrucoes.append(tarefasProntas[0]) # Adiciona a tarefa na lista de instrucoes
                tarefasInativas.extend(PegarTarefasInativas(copiaTarefas, tarefasProntas[0], tempoAtual)) # Pega e adiciona todas as tarefas que ja estao ingressados no tempo atual mas inativos
                tarefasProntas[0]['duracaoRestante'] -= 1 # Modifica a tarefa que foi 'processado' diminuido sua duracao
                tempoAtual+=1 # Aumenta o tempo atual da simulação
                
                # Procura por novas tarefas prontas no tempo atual atualizado, 
                # impede que seja removida copias para que .pop(0) funcione corretamente.    
                tarefasProntas = PegarTarefasProntas(copiaTarefas, tarefasProntas,tempoAtual, False) 
                            
        tarefasProntas.pop(0) # Remove o primeiro da lista de prontos a tarefa quando o quantum dele acaba, impedindo que ele rode até o final

    return instrucoes, tarefasInativas
        
# Algoritmo SRTF, não é afetado pelo quantum
def SRTF(tarefas, tempoMax, quantum, alpha):
    copiaTarefas = tarefas.copy() # Cria uma copia das tarefas para não alterar o conteudo original
    tempoAtual = 0 # Tempo usado para inserir nos detalhes do bloco e controlar o LOOP WHILE
    instrucoes = [] # Lista de instrucoes contento informações uteis para gerar o gráfico
    tarefasInativas = [] # Lista para guardar as instrucoes inativas
    tarefasProntas = [] # Lista de prontas para auxiliar e facilitar na manipulação do que deve ser selecionado
    tarefasProntas = PegarTarefasProntas(copiaTarefas, tarefasProntas,tempoAtual, True) # Procura por tarefas que já estão ingressadas e possuem duracao restante
    
    while tempoAtual < tempoMax: # Loop para garantir que a lista de instrucao gerada tenha esvaziado as duracoes das tarefas
        for q in range(quantum): # Loop para garantir o funcionamento do quantum
            menorDuracao = PegarMenorDuracao(tarefasProntas) # Procura e guarda a tarefa de menor duracao restante
            instrucoes.append(menorDuracao) # Adiciona ele na lista de instrucoes
            tarefasInativas.extend(PegarTarefasInativas(copiaTarefas, menorDuracao, tempoAtual)) # Pega e adiciona todas as tarefas que ja estao ingressados no tempo atual mas inativos
            menorDuracao['duracaoRestante'] -= 1 # Modifica a tarefa que foi 'processado' diminuido sua duracao
            tempoAtual +=1 # Aumenta o tempo atual da simulação
            tarefasProntas = PegarTarefasProntas(copiaTarefas, tarefasProntas,tempoAtual, True) # Procura por novas tarefas prontas no tempo atual atualizado, permite remoção de copias.  

    return instrucoes, tarefasInativas

# Algoritmo PrioP, não é afetado pelo quantum
def PrioP(tarefas, tempoMax, quantum, alpha):
    copiaTarefas = tarefas.copy() # Cria uma copia das tarefas para não alterar o conteudo original
    tempoAtual = 0 # Tempo usado para inserir nos detalhes do bloco e controlar o LOOP WHILE
    instrucoes = [] # Lista de instrucoes contento informações uteis para gerar o gráfico
    tarefasInativas = [] # Lista para guardar as instrucoes inativas
    tarefasProntas = [] # Lista de prontas para auxiliar e facilitar na manipulação do que deve ser selecionado
    tarefasProntas = PegarTarefasProntas(copiaTarefas, tarefasProntas,tempoAtual, True) # Procura por tarefas que já estão ingressadas e possuem duracao restante
    
    while tempoAtual < tempoMax: # Loop para garantir que a lista de instrucao gerada tenha esvaziado as duracoes das tarefas
        for q in range(quantum): # Loop para garantir o funcionamento do quantum           
            maiorPrio = PegarMaiorPrioridade(tarefasProntas) # Procura e guarda a tarefa de maior prioridade
            instrucoes.append(maiorPrio) # Adiciona ele na lista de instrucoes
            tarefasInativas.extend(PegarTarefasInativas(copiaTarefas, maiorPrio, tempoAtual)) # Pega e adiciona todas as tarefas que ja estao ingressados no tempo atual mas inativos
            maiorPrio['duracaoRestante'] -= 1 # Modifica a tarefa que foi 'processado' diminuido sua duracao
            tempoAtual +=1 # Aumenta o tempo atual da simulação
            tarefasProntas = PegarTarefasProntas(copiaTarefas, tarefasProntas, tempoAtual, True) # Procura por novas tarefas prontas no tempo atual atualizado, permite remoção de copias.  
            
    return instrucoes, tarefasInativas

# Algoritmo PrioEnv, não é afetado pelo quantum
def PrioEnv(tarefas, tempoMax, quantum,alpha):
    tarefasOriginais = copy.deepcopy(tarefas) # Cria uma copia profunda das tarefas para não alterar o conteudo original
    copiaTarefas = tarefas.copy() # Cria uma copia das tarefas para não alterar o conteudo original
    tempoAtual = 0 # Tempo usado para inserir nos detalhes do bloco e controlar o LOOP WHILE
    instrucoes = [] # Lista de instrucoes contento informações uteis para gerar o gráfico
    tarefasInativas = [] # Lista para guardar as instrucoes inativas
    tarefasProntas = [] # Lista de prontas para auxiliar e facilitar na manipulação do que deve ser selecionado
    tarefasProntas = PegarTarefasProntas(copiaTarefas, tarefasProntas,tempoAtual, True) # Procura por tarefas que já estão ingressadas e possuem duracao restante
    tarefaAnteriorID = -1
    concluida = False

    while tempoAtual < tempoMax: # Loop para garantir que a lista de instrucao gerada tenha esvaziado as duracoes das tarefas
        for q in range(quantum): # Loop para garantir o funcionamento do quantum           
            maiorPrio = PegarMaiorPrioridade(tarefasProntas) # Procura e guarda a tarefa de maior prioridade       
            instrucoes.append(maiorPrio) # Adiciona ele na lista de instrucoes
            maiorPrio['duracaoRestante'] -= 1 # Modifica a tarefa que foi 'processado' diminuido sua duracao
            concluida = EnvelhecerPrioridades(alpha, tarefasProntas, maiorPrio, tarefasOriginais, tempoAtual, tarefaAnteriorID, concluida) # Envelhece as prioridades das tarefas prontas
            tarefaAnteriorID = maiorPrio['id']
            tarefasInativas.extend(PegarTarefasInativas(copiaTarefas, maiorPrio, tempoAtual)) # Pega e adiciona todas as tarefas que ja estao ingressados no tempo atual mas inativos
            tempoAtual +=1 # Aumenta o tempo atual da simulação
            tarefasProntas = PegarTarefasProntas(copiaTarefas, tarefasProntas, tempoAtual, True) # Procura por novas tarefas prontas no tempo atual atualizado, permite remoção de copias.  
            
    
    return instrucoes, tarefasInativas

def EnvelhecerPrioridades(alpha,tarefasProntas, tarefasAtual, tarefasOriginais, tempoAtual, tarefaAnteriorID, concluida):    
    
    envelhecer = False
    if concluida:
        envelhecer = True
        concluida = False
    print("Tempo:", tempoAtual)
    # Procura por tarefas que:
    # ingressaram no tempo atual,
    # foi concluida
    for tarefa in tarefasProntas:
        if (tarefa['ingressoTarefa'] == tempoAtual):
            envelhecer = True
            print("entrou novo", tempoAtual)
        if tarefa['duracaoRestante'] == 0:
            concluida = True
            print("concluida", tempoAtual)
    

    if envelhecer:
        for tarefa in tarefasProntas:            
            tarefa['prioridade'] += alpha  # Aumenta a prioridade da tarefa (envelhece)
            print(f"Tarefa {tarefa['id']} envelheceu para prioridade {tarefa['prioridade']} no tempo {tempoAtual}")
        print("----")
    
    if tarefaAnteriorID != -1 and tarefasAtual['id'] != tarefaAnteriorID:        
        indice = next((i for i, t in enumerate(tarefasOriginais) if t['id'] == tarefasAtual['id']), None)    
        tarefasAtual['prioridade'] = tarefasOriginais[indice]['prioridade'] 
        print(tarefasAtual['id'], " prioridade resetada para ", tarefasAtual['prioridade'], " no tempo ", tempoAtual)        

    print("=====")
    return concluida

# Funcao para buscar por tarefas ingressadas e contendo duracao restante
def PegarTarefasProntas(tarefas, tarefasProntas, tempoAtual, apagarConcluidas):
    # Faz uma copia das tarefas prontas existente para não altera-la ao retornar,
    # Necessário para o funcionamento correto de uma FILA para o FIFO
    prontas = tarefasProntas.copy() 
    envelhecer = False
    # Condição para remover tarefas conlcuidas com duracao restante em 0
    # Necesssário para o funcionamento do SRTF e PrioP
    if apagarConcluidas: 
        prontas = [t for t in prontas if t['duracaoRestante'] != 0]  # Remove tarefas que já foram concluídas        
        envelhecer = True
    idsProntas = {tarefa['id'] for tarefa in prontas}

    # Loop para buscar por tarefas ingressadas e com duracao restante, evitando também tarefas iguais
    for i in range (len(tarefas)):
        if ChecarIngresso(tarefas[i], tempoAtual) and ChecarDuracaoRestante(tarefas[i]) and tarefas[i]['id'] not in idsProntas:
            prontas.append(tarefas[i])
    
    return prontas

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



