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
    mutexEmUso = []
    tarefasProntas, ingressouNovo = PegarTarefasProntas(copiaTarefas, tarefasProntas,tempoAtual,mutexEmUso) # Procura por tarefas que já estão ingressadas e possuem duracao restante
    
    while VerificarDuracoesRestantes(copiaTarefas): # Loop para garantir que a lista de instrucao gerada tenha esvaziado as duracoes das tarefas        
        removido = False # Para previnir que uma tarefa seja removida duas vezes quando o quantum acaba e a tarefa é concluída ao mesmo tempo
        for i in range(quantum): # Loop para garantir o funcionamento do quantum, sempre que ele acaba é reiniciado o processo de seleção da proxima tarefa            
            if tarefasProntas != []: 
                # Reavaliar para remover tarefas que nao deveriam estar em prontas pois estao bloqueadas por IO ou MUTEX
                tarefasProntas = [t for t in tarefasProntas if not BloquearTarefa(t, mutexEmUso)]         
                # Seleciona a tarefa de acordo com o algoritmo selecionado
                tarefa = algoritmoSelecionado(tarefasProntas)
                                
                # Para fins de exibição ao clicar na barra no gráfico, e mostrar corretamente as informações
                tarefa['bloqueadoIO'] = False
                if mutexEmUso:
                    for mutex in mutexEmUso:
                        if mutex['tid'] == tarefa['id']:
                            tarefa['mutexID'] = mutex['mid']
                            break
                        else:
                            tarefa['mutedID'] = -1
                            

                instrucoes.append(copy.deepcopy((tarefa))) # Adiciona a tarefa na lista de instrucoes                
                tarefasInativas.extend(PegarTarefasInativas(copiaTarefas, tarefa, tempoAtual)) # Pega e adiciona todas as tarefas que ja estao ingressados no            
                tarefa['duracaoRestante'] -= 1 # Modifica a tarefa que foi 'processado' diminuido sua duracao           
                AtualizarEventosTarefa(tarefa, mutexEmUso)
                
                if tarefa['duracaoRestante'] == 0:
                    for mutex in mutexEmUso:                        
                        if mutex['tid'] == tarefa['id']:
                            # Remove o Mutex usado pela tarefa que concluiu
                            mutexEmUso = [(tid, mid) for tid, mid in mutexEmUso if tid == tarefa['id']]
                           
                    tarefasProntas = [t for t in tarefasProntas if t['duracaoRestante'] > 0]                     
                    removido = True

            tempoAtual+=1 # Aumenta o tempo atual da simulação
           
            tarefasProntas, ingressouNovo = PegarTarefasProntas(copiaTarefas, tarefasProntas,tempoAtual, mutexEmUso) # Procura por novas tarefas prontas no tempo atual atualizado,
            
            # Adiciona um campo vazio
            if tarefasProntas == []:                
                instrucoes.append({'nome': 'OCIOSO', 'id': -1, 'cor': 0, 'ingressoTarefa': -1, 'ingressoTempo': tempoAtual, 'duracao': 0, 'duracaoRestante': 0, 'tempoRelativo': 0, 'prioridade': -1, 'estado': True, 'eventos': [], 'mutexID': -1, 'bloqueadoIO': False})
                
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

# Funcao para buscar por tarefas ingressadas e contendo duracao restante
def PegarTarefasProntas(tarefas, tarefasProntas, tempoAtual, mutexEmUso):
    
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
            # Condição importante para previnir que uma tarefa entre nas prontas quando está bloqueada por IO ou MUTEX
            if not BloquearTarefa(tarefa, mutexEmUso):
                prontas.append(tarefa) # Adiciona a tarefa na lista de prontas caso passe nas condições
        if tarefa['ingressoTarefa'] == tempoAtual:
            ingressouNovo = True

    return prontas, ingressouNovo

# Usado para previnir que uma tarefa que esteja bloqueado possa entrar na lista de tarefasProntas
def BloquearTarefa(tarefa, mutexEmUso):      
    # Loop nos eventos presentes na tarefa
    for evento in tarefa['eventos']:
        tipo = evento['tipo'] # Para facilitar no codigo atribuir no tipo 
        # Verifica se for um evento de I/O se ele já está iniciado e rodando
        if tipo == 'IO' and evento['inicio'] == 0 and evento['duracao'] > 0: 
            evento['duracao'] -= 1 # Duracao é diminuida para fazer o controle e quando chegar a 0 eu sei que ele terminou o evento de IO
            tarefa['bloqueadoIO'] = True # Para fins de exibição ao clicar na barra no grafico
            return True  # Retorna verdadeiro para indicar que deve ser bloqueado
        elif tipo =='IO': # Para fins de exibição de informações ao clicar na barra no gráfico      
            tarefa['bloqueadoIO'] = False
            tarefa['eventos'] = [
                e for e in tarefa['eventos']
                if not (e['tipo'] == 'IO' and evento['inicio'] == 0 and e['duracao'] == 0)]
        # Verifica se há uma requisição de mutex quando a duracao dele está em 0
        if tipo == 'ML' and evento['duracao'] == 0:             
            mutexID = evento['mutexID']
            # Loop no mutexEmUso para buscar se há um mutexID já sendo utilizado
            for m in mutexEmUso:                
                if m['mid'] == mutexID and m['tid'] != tarefa['id']:
                    return True  # bloqueia se mutex ocupado por outro
    return False

# Funcao para atualizar o tempo de inicio e duracoes dos eventos relacionados a tarefa em execução
def AtualizarEventosTarefa(tarefa, mutexEmUso=None):
    # Loop em todos os eventos presentes na tarefa
    for evento in tarefa['eventos']:
        tipo = evento['tipo']
        # Diminui o inicio da IO para saber quando ele chegar em 0 iniciar o evento de IO
        if tipo == 'IO' and evento['inicio'] > 0:
            evento['inicio'] -=1 
        # Caso seja um mutex e a duracao dele está em 0, indicando requisição de mutex ou liberação senão apenas diminua sua duração
        if tipo in ['ML', 'MU'] and evento['duracao'] == 0:
            ControleMutex(tarefa, tipo, mutexEmUso, evento['mutexID'])      
        else:
            evento['duracao']-=1

# Funcao para controle do mutex
def ControleMutex(tarefa,tipo,mutexEmUso, mutexID):
    # Se for um MUTEXLOCK
    if tipo == 'ML':
        # Verifica se já não existe um mutex de mesmo id em uso
        if not any(m['mid'] == mutexID for m in mutexEmUso):
            # Adiciona numa lista para controle dos mutex em uso            
            mutexEmUso.append({'tid' : tarefa['id'], 'mid' : mutexID})               
            # Remove dos eventos da TAREFA o evento de ML após ele ser chamado para evitar erros
            tarefa['eventos'] = [
                e for e in tarefa['eventos']
                if not (e['tipo'] == 'ML' and e['duracao'] == 0)]     
    # Se for um MUTEXUNLOCK  
    elif tipo == 'MU':
        # remove o mutex da lista de mutex em uso
        mutexEmUso[:] = [m for m in mutexEmUso if m['mid'] != mutexID]
        # remove o evento da TAREFA
        tarefa['eventos'] = [
            e for e in tarefa['eventos']
            if not (e['tipo'] == 'MU' and e['duracao'] == 0)]
    
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

def EnvelhecerPrioridades(alpha,tarefasProntas, tarefasAtual):    
    for tarefa in tarefasProntas:
        if tarefa['id'] != tarefasAtual['id']:
            tarefa['prioridade'] += alpha

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

def VerificarDuracoesRestantes(tarefas):
    for tarefa in tarefas:
        if ChecarDuracaoRestante(tarefa):
           return True 
    return False
