import tkinter as tk
from tkinter import filedialog
import os

from Algoritmos import FIFO, SRTF, PrioP, PrioEnv

# Função para pegar o caminho do arquivo selecionado
def SelArquivo(arqSel):        
    # caminho = contem o em string o caminho
    caminho = filedialog.askopenfilename(
        title="Selecione o arquivo de configuração",
        filetypes=[("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*")]
    )

    if caminho: # Verifica se foi selecionado um caminho
        nomeArquivo = os.path.basename(caminho) # Pega o nome do arquivo
        WriteLockBox(arqSel, nomeArquivo) # Escreve o nome do arquivo no campo de texto e bloqueia novamente
        return caminho # Retorna o caminho
    
# Funcao para gerar as instrucoes utilizadas para montar o gráfico
def GerarInstrucoes(algoritmo, tarefas, quantum, alpha):
    instrucoes = [] # Variavel para armazenar as instrucoes para criar cada bloco
    instrucoesInativas = [] # Variavel para armazenar as instrucoes para criar os blocos representando as tarefas inativas
   
    # Variavel para selecionar qual algoritimo usar
    algoritimos = {
        "FIFO": FIFO,
        "SRTF": SRTF,
        "PrioP": PrioP,
        "PrioEnv": PrioEnv
    }  

    # instrucoesBrutas = contem as instrucoes selecionadas a partir da lista de tarefas, possuindo informações limitadas
    # listaInativos = contem as instrucoes das tarefas inativas, possuindo informações limitadas
    instrucoesBrutas, listaInativos = algoritimos[algoritmo](tarefas, quantum, alpha)   

    # Loop para gerar os detalhes das informações para cada instrucao da lista
    for i in range(len(instrucoesBrutas)):         
        instrucoes.append(CriarDadosInstrucao(instrucoesBrutas[i], i,False))

    if listaInativos: # Verifica se está vazia a lista
       for i in range(len(listaInativos)): # Loop para gerar os detalhes das informações para as instruções inativas  
           instrucoesInativas.append (CriarDadosInstrucao(listaInativos[i], listaInativos[i]['ingressoTempo'],True) )
    
    if instrucoes[len(instrucoes)-1]['id'] == -1: # Verifica se a ultima instrução é ociosidade
        instrucoes.pop() # Remove a ultima instrução de ociosidade

    return instrucoes, instrucoesInativas

# Funcao para detalhar a instrucao
# Informações serão mostradas ao clicar no bloco gerado no gráfico
def CriarDadosInstrucao(instrucao, tempoIngresso, inativo):    
    if inativo:
        cor = "#FFFFFF" # Define a cor branca caso seja para representar uma tarefa inativa
        estado = False # Usado para determinar se deve ser escrito que o bloco esta inativo
        instrucao['duracaoRestante'] = "---" # Restante que seria mostrado nas informações de um bloco inativo
    else:
        cor = instrucao['cor'] # Para escrever qual indice da cor foi utilizado
        estado = True # Usado para determinar se deve ser escrito que o bloco esta inativo
        instrucao['duracaoRestante'] += 1 # Definir o tempo total processado da tarefa    
    # Retorna um bloco de informações para salvar em um campo da lista
    return{
        'nome': instrucao['nome'],
        'id': instrucao['id'], 
        'cor': cor, 
        'ingressoTarefa': instrucao['ingressoTarefa'], 
        'ingressoTempo': tempoIngresso, # Valor importante usado para definir em que tempo o bloco vai ser desenhado
        'duracao': instrucao['duracao'], 
        'duracaoRestante': instrucao['duracaoRestante'], 
        'tempoRelativo': 0,
        'prioridade': instrucao['prioridade'], 
        'estado': estado,
        'eventos': instrucao['eventos'],
        'mutexID': instrucao['mutexID'],
        'bloqueadoIO': instrucao['bloqueadoIO']
        }   
   
# Funcao para definir as configurações do scroll
def DefinirScrollGantt(canvasGantt, config, maxTempo, maxTid):
    largTotal = config['escalaX'] * (maxTempo + 2) # Define o scroll horizontal, se o tempoMax for muito longo
    altTotal = config['escalaY'] * (maxTid + 2) # Define o scroll vertical, se o tiver varias tarefas

    canvasGantt.config(scrollregion=(0,0 ,largTotal,altTotal)) # Aplica as mudanças efetivamente na inteface do scroll

# Funcao para escrever em bloco de texto editavel mas mante-los bloqueados
def WriteLockBox(entryBox, texto):
    entryBox.config(state="normal") # Habilita a escrita no campo de texto
    entryBox.delete(0, tk.END) # Apaga o texto contido nele
    entryBox.insert(0,texto) # Escreve o novo texto no campo
    entryBox.config(state="readonly") # Bloqueia edição no campo

# Funcao para pegar o texto no arquivo selecioado
def LerArquivo(caminho):
    with open(caminho, 'r') as f: 
        texto = f.readlines() # Salva o texto contido no arquivo na variavel texto
        return texto

# Organiza as informações do arquivo
def ProcessarDados(texto):
    tarefas = []
    
    algoritmo, quantum, alpha = texto[0].split(';') # Pega os valores da primeira linha sobre o algoritimo e quantum
    quantum = int (quantum) # Converte para int
    alpha = int (alpha) # Converte para int
    # Lê as linhas seguintes contendo as informações de cada tarefa
    for linha in texto[1:]:
        linha = linha.strip()
        if not linha:
            continue
        partes = linha.split(';') # Separa os conteudos da linha onde tiver ';'
        nome = partes[0] # Guarda o nome da tarefa ex: t1, t2, t3
        id = int(nome[1:]) # Retira do nome o numero para utilizar como id em int
        cor = partes[1] # Guarda o valor da cor em int
        ingresso = int (partes[2]) # Guarda o tempo de ingresso da tarefa em int
        duracaoT = int (partes[3]) # Guarda a duracao em int
        prioridade = int (partes[4]) # Guarda a proridade em int
        eventos = []

        # Verifica se existem há pelo menos 6 partes na linha (evento é opcional)
        # Verifica também se não está vazia de partes em branco
        if len(partes) > 5 and partes[5].strip():
            for eventoStr in partes[5:]:
                eventoStr = eventoStr.strip() # Remove espaços em branco
                if eventoStr.startswith('IO:'): # IO:XX-YY, xx é o tempo de inicioRelativo e yy duracao
                    dadosIO = eventoStr[3:].split('-')                    
                    tipo = 'IO'
                    inicio = int(dadosIO[0])
                    duracao = int(dadosIO[1])
                    eventos.append({'tipo': tipo, 'inicio': inicio, 'duracao': duracao})                    
                elif eventoStr.startswith('ML'): # MLxx:00;  xx é o numero do mutex, 00 instante de tempo em que acontece
                    dadosML = eventoStr[2:].split(':', 1)                    
                    tipo = 'ML'
                    mutexID = int(dadosML[0])
                    instante = int(dadosML[1]) # Instante RELATIVO AO INICIO DA TAREFA
                    eventos.append({'tipo': tipo, 'mutexID': mutexID, 'duracao': instante})
                elif eventoStr.startswith('MU'): # MUxx:00;  xx é o numero do mutex, 00 instante de tempo em que acontece
                    dadosMU = eventoStr[2:].split(':', 1)                    
                    tipo = 'MU'
                    mutexID = int(dadosMU[0])
                    instante = int(dadosMU[1]) # Instante RELATIVO AO INICIO DA TAREFA
                    eventos.append({'tipo': tipo, 'mutexID': mutexID, 'duracao': instante})
            
        # IO: operação de I/O em algum dispoisivo externo 
        # ML: mutex lock   
        # MU: mutex unlock 
        # Todos os instantes de tempo indicados nas ações são sempre relativos ao início da tarefa.

        # Une cada linha em uma lista com as informações retiradas em string
        tarefas.append (
            {
                'nome': nome,
                'id': id,
                'cor': cor,
                'ingressoTarefa': ingresso,
                'ingressoTempo' : 0,
                'duracao': duracaoT,
                'duracaoRestante': duracaoT,
                'prioridade': prioridade,
                'eventos': eventos,
                'mutexID': -1,
                'bloqueadoIO': False                    
            }
        )
        
    return tarefas, algoritmo, quantum, alpha

# Funcao para atualizar o "Log do Bloco"
def AtualizarLog(logBox, mensagem):
    inicioMsg = logBox.index(tk.END) # Guardar onde vai ser 'focado' o texto 
    logBox.insert(tk.END, mensagem + "\n")
    logBox.see(inicioMsg) # Centraliza no topo a exibição do texto ao ser escrito

# Funcao para salvar os dados editados na janela Edição
def Salvar(blocosTarefa, algoritmo, quantum, alpha, nomeArquivo, caminhoOriginal):
    # Verifica se o nome do arquivo tem a extensão .txt para adicionar
    if not nomeArquivo.endswith('.txt'):
        nomeArquivo += '.txt'

    # Para garantir que o local seja salvo na mesma pasta onde esta o app
    dirSaida = os.path.dirname(caminhoOriginal) if caminhoOriginal else os.getcwd()
    caminhoSaida = os.path.join(dirSaida, nomeArquivo)

    # Primeira linha contendo o algortimo, quantum e alpha para envelhecimento
    linhas = [f"{algoritmo};{quantum};{alpha}"]
    
    # Para cada bloco criado na edição, escrever eles em linhas diferentes
    for bloco in blocosTarefa:
        if not bloco.winfo_exists(): # Garante que blocos deletado durante a edição nao sejam pegos
            continue
        d = bloco.dados
        # Pega as informações contidas nos campos de TextEntry para escrever a linha
        linha = f"{d['nome'].get()};{d['cor'].get()};{d['ingresso'].get()};{d['duracao'].get()};{d['prioridade'].get()}"
        
        # Adiciona os eventos relacionados a tarefa na mesma linha
        # O tipo de informações não são os valores direto e sim o campo de tk das variaveis de TextEntry
        # Necessitando usar .get() e outras chamadas
        evs = []
        for ev in d['eventos']:
            t = ev['tipo'].get().strip().upper()
            if t == "IO":
                evs.append(f"IO:{ev['inicio'].get()}-{ev['duracao'].get()}")
            elif t in ("ML", "MU"):
                evs.append(f"{t}{ev['mutex'].get()}:{ev['instante'].get()}")

        # Adiciona efetivamente as linhas contendo os eventos junto a linha contendo as informações iniciais da tarefa
        if evs:
            linha += ";" + ";".join(evs)
        
        # Adiciona a uma lista a linha para ser escreti tudo de uma vez
        linhas.append(linha)

    # Faz a escrita das linhas no arquivo:
    with open(caminhoSaida, 'w', encoding='utf-8') as f:
        f.write("\n".join(linhas))