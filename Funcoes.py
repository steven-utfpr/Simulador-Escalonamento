import tkinter as tk
from tkinter import filedialog
import os

from Algoritmos import FIFO, SRTF, PrioP

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
def GerarInstrucoes(algoritmo, tarefas, quantum):
    instrucoes = [] # Variavel para armazenar as instrucoes para criar cada bloco
    instrucoesInativas = [] # Variavel para armazenar as instrucoes para criar os blocos representando as tarefas inativas
    tempoMax = DuracaoTotal(tarefas) # Calcula o tempo máximo da simulação a partir da lista de tarefas
    # Variavel para selecionar qual algoritimo usar
    algoritimos = {
        "FIFO": FIFO,
        "SRTF": SRTF,
        "PrioP": PrioP
    }  

    # instrucoesBrutas = contem as instrucoes selecionadas a partir da lista de tarefas, possuindo informações limitadas
    # listaInativos = contem as instrucoes das tarefas inativas, possuindo informações limitadas
    instrucoesBrutas, listaInativos = algoritimos[algoritmo](tarefas,tempoMax, quantum)   

    # Loop para gerar os detalhes das informações para cada instrucao da lista
    for i in range(len(instrucoesBrutas)):             
        instrucoes.append(CriarDadosInstrucao(instrucoesBrutas[i], i,False))

    if listaInativos: # Verifica se está vazia a lista
       for i in range(len(listaInativos)): # Loop para gerar os detalhes das informações para as instruções inativas  
           instrucoesInativas.append (CriarDadosInstrucao(listaInativos[i], listaInativos[i]['ingressoTempo'],True) )

    return instrucoes, instrucoesInativas

# Funcao para detalhar a instrucao
# Informações serão mostradas ao clicar no bloco gerado no gráfico
def CriarDadosInstrucao(instrucao, tempoIngresso, inativo):    
    if inativo:
        cor = 0 # Define a cor branca caso seja para representar uma tarefa inativa
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
        'prioridade': instrucao['prioridade'], 
        'estado': estado,
        'eventos': instrucao['eventos']
        }   

# Funcao para calcular o tempo total a partir das tarefas
def DuracaoTotal(tarefas):
    count = 0
    for tarefa in tarefas: # Loop para percorrer todas as tarefas da lista
        count += tarefa['duracao'] # Pega a duracao de cada tarefa e soma elas
    return count # Retorna a soma
   
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
    
    algoritmo, quantum = texto[0].split(';') # Pega os valores da primeira linha sobre o algoritimo e quantum
    quantum = int (quantum) # Converte para int

    # Lê as linhas seguintes contendo as informações de cada tarefa
    for linha in texto[1:]:
        linha = linha.strip()
        if not linha:
            continue
        partes = linha.split(';',6) # Separa os conteudos da linha onde tiver ';'
        nome = partes[0] # Guarda o nome da tarefa ex: t1, t2, t3
        id = int(nome[1:]) # Retira do nome o numero para utilizar como id em int
        cor =  int (partes[1]) # Guarda o valor da cor em int
        ingresso = int (partes[2]) # Guarda o tempo de ingresso da tarefa em int
        duracao = int (partes[3]) # Guarda a duracao em int
        prioridade = int (partes[4]) # Guarda a proridade em int
        eventos = partes[5] # PROJETO A: SEM USO

        # Une cada linha em uma lista com as informações retiradas em string
        tarefas.append (
            {
                'nome': nome,
                'id': id,
                'cor': cor + 1,
                'ingressoTarefa': ingresso,
                'ingressoTempo' : 0,
                'duracao': duracao,
                'duracaoRestante': duracao,
                'prioridade': prioridade,
                'eventos': eventos                
            }
        )
    return tarefas, algoritmo, quantum

# Funcao para atualizar o "Log do Bloco"
def AtualizarLog(logBox, mensagem):
    inicioMsg = logBox.index(tk.END) # Guardar onde vai ser 'focado' o texto 
    logBox.insert(tk.END, mensagem + "\n")
    logBox.see(inicioMsg) # Centraliza no topo a exibição do texto ao ser escrito

