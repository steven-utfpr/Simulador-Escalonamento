#+----------------------+----------------------------------+
#|  [CONFIGURAÇÕES]     |                                  |
#|                      |                                  |
#|  Algoritmo: [▼]      |                                  |
#|  Arquivo:   [_____]  |                                  |
#|  [ Iniciar]        |       ÁREA DO GRÁFICO DE        |
#|                      |            GANTT                 |
#|                      |                                  |
#|                      |                                  |
#+----------------------+----------------------------------+
#|                   LOG DA SIMULAÇÃO                      |
#|  - Iniciado...                                          |
#|  - Tarefa 1 executou...                                 |
#+----------------------------------------------------------+
#. COMENTAR O CÓDIGO E FAZER DOCUMENTAÇÃO

import matplotlib.pyplot as plt
import tkinter as tk
from Janelas import CriarInterface
from Funcoes import LerArquivo, SelArquivo, WriteLockBox, GerarInstrucoes,ProcessarDados, AtualizarLog,DefinirScrollGantt
from Grafico import GerarGrafico, CriarBarra, ApagarBarra, cores


# Main
class SimulEscal:
    def __init__(self):
        self.usarPasso = False # Variável para controlar o modo passo a passo
        self.barraID = [] # Variável para armazenar os IDs das barras criadas no gráfico, utilizado no modo passo a passo para apagar as barras
        self.caminhoArq = None # Variável para armazenar o caminho do arquivo de configuração
        self.tempoAtual = 0 # Variável para armazenar o tempo atual da simulação, utilizado no modo passo a passo
       
        # Configurações para definir o tamanho das barras e do gráfico
        self.graficoConfig = {
            'escalaX': 50, # Define a largura de cada unidade de tempo no eixo X
            'escalaY': 25, # Define a altura de cada barra de tarefa no gráfico de preferencia colocar escalaX/2
        }
        # Criação da interface gráfica
        # root = janela principal
        # frameInfo = painel inferior de logs
        # logBox = caixa de texto para exibir logs
        # frameConfig = painel esquerdo de configurações
        # frameGantt = painel direito do gráfico de Gantt
        # canvasGantt = área onde o gráfico de Gantt será desenhado
        # tempoAtualEntry = campo de texto para exibir o tempo atual, no modo passo a passo
        # arqAtualEntry = campo de texto para exibir o nome do arquivo selecionado
        self.root, self.frameInfo, self.logBox, self.frameConfig, self.frameGantt, self.canvasGantt, self.tempoAtualEntry,  self.arqAtualEntry = CriarInterface(self)
                    
        # Inicia o loop principal da interface gráfica
        if self.root:            
            self.root.mainloop()

    # Função para iniciar a simulação
    def IniciarSimulacao(self):        
        
        # tarefas = lista de tarefas a serem simuladas
        # algoritmo = algoritmo de escalonamento selecionado
        # quantum = valor do quantum para algoritmos

        # Verifica se um arquivo .txt de configuração foi selecionado
        if self.caminhoArq is not None:
            texto = LerArquivo(self.caminhoArq) # Lê o conteúdo do arquivo selecionado
            self.tarefas, self.algoritmo, self.quantum = ProcessarDados(texto) # Processa os dados do arquivo para obter as tarefas, algoritmo e quantum
        # Caso nenhum arquivo tenha sido selecionado, utiliza uma configuração padrão
        else:
            self.tarefas, self.algoritmo, self.quantum = self.UsarConfigPadrao() # Usa configuração padrão        

        # instruções = lista contendo o passo a passo para gerar no gráfico de Gantt        
        # maxTempo = duração total da simulação, utilizado para definir o tamanho horizontal do gráfico e o scroll caso necessário
        # maxTid = número máximo de tarefas, utilizado para definir o tamanho vertical do gráfico e o scroll
        self.instrucoes, self.instrucoesInativos = GerarInstrucoes(self.algoritmo, self.tarefas, self.quantum) # Gera as instruções de simulação com base nas tarefas, algoritmo e quantum selecionados
        self.maxTempo = len(self.instrucoes) 
        self.maxTid = len(self.tarefas)
        DefinirScrollGantt(self.canvasGantt, self.graficoConfig, self.maxTempo, self.maxTid) # Define as configurações de scroll para o gráfico de Gantt
        
        # Gera o gráfico de Gantt com as instruções geradas
        GerarGrafico(self.canvasGantt, self.graficoConfig, self.instrucoes, self.instrucoesInativos, self.maxTempo, self.maxTid, self.usarPasso, self.PegarInfoBarra)
        
        # Atualiza as informações exibidas no painel de "configurações"
        self.AtualizarInfos()

    def AtualizarInfos(self):
        self.infoAlgo.set(f"Algoritmo: {self.algoritmo}") # Atualiza o nome do algoritmo utilziado
        self.infoQuantum.set(f"Quantum: {self.quantum}") # Atualiza o valor do quantum utilizado

    # Função contendo as configurações padrão, caso não seja selecionado um .txt para simular
    def UsarConfigPadrao(self):
        tarefas = [] # Variável para armazenar o conteudos das tarefas: prioridade, duracao, ingresso
        configPadrao = 'SRTF;2\n', 't01;0;0;5;2;\n', 't02;1;0;2;3;\n', 't03;2;1;4;1;\n', 't04;3;3;1;4;\n', 't05;4;5;2;5;\n' # String contendo as configurações padrão
        # OBS: os valores são os mesmo presente no Capítulo 6 do pdf do Carlos Maziero, Página 73
        tarefas, algoritmo, quantum = ProcessarDados(configPadrao)
       
        return tarefas, algoritmo, quantum

    # Pega o caminho onde está localizado o arquivo .txt utilizando uma função em Funcoes.py
    def PegarCaminho(self):
        self.caminhoArq = SelArquivo(self.arqAtualEntry)

    # Função utilizada para controlar quando o usuário marcar o checkbox para usar passo a passo
    def CheckPasso(self):
        self.usarPasso = not self.usarPasso
        self.tempoAtual=0 # Reseta o tempo atual para o inicio 
        self.IniciarSimulacao() # Inicia uma nova simulação para definir o estado inicial do gráfico, vazia ou já montada dependendo do usarPasso

    # Função para montar os detalhes em texto de cada bloco e exibi-los no "log do bloco"
    def PegarInfoBarra(self,instrucao):        
        # Verifica se ele é um bloco de tarefa Inativa
        if instrucao['estado']:
            estado = "Em Execução" 
        else:
            estado = "Inativo"

        # String contendo a formatação das informações
        info = f"""\
   DETALHES DA TAREFA
────────────────────────────
Tarefa: T{instrucao['id'] + 1}| Algoritmo: {self.algoritmo} | Quantum: {self.quantum} | Estado: {estado} 
Tempo Ingresso: {instrucao['ingressoTempo']} | Tempo Processado: {instrucao['duracaoRestante']}
Duração Total: {instrucao['duracao']} | Prioridade: {instrucao['prioridade']} | Cor (índice): {instrucao['cor']}
────────────────────────────
"""
        # Atualiza o bloco de texto
        AtualizarLog(self.logBox, info)
    
    # Função atrelado ao botão (>) para avançar um tempo ao utilizar o passo a passo
    def AvancarPasso(self):       
        if self.tarefas and self.usarPasso: # Verifica se existe elementos na lista tarefas e o usarPasso estiver marcado
            if(self.tempoAtual < len(self.instrucoes)): # Condição para previnir que o tempo ultrapasse o permitido da simulação permitido
                self.CriarBarras() # Função para desenhar a barra/bloco de acordo com o tempo atual
                self.tempoAtual += 1 # Avança o tempo da simulação
                WriteLockBox(self.tempoAtualEntry, self.tempoAtual) # Desbloqueia para escrever e bloqueia novamente o campo de texto e atualizar na tela
                # Referente ao campo entre os dois botões de avançar e voltar
    
    # Função atrelado ao botão (<) para voltar um tempo ao utilizar o passo a passo
    def VoltarPasso(self):
        if self.tarefas and self.usarPasso: # Verifica se existe elementos na lista tarefas e o usarPasso estiver marcado
            if(self.tempoAtual > 0): # Condição para previnir que o tempo fique negativo                    
                for i in range(len(self.barraID)): # Loop para remover todas as barras pertencentes a um tempo atual
                    if self.barraID[i]['tempo'] == self.tempoAtual-1:                    
                        ApagarBarra(self.canvasGantt,self.barraID[i]['barra'], self.barraID[i]['barraText']) # Função para apagar efetivamente do grafíco a barra

                self.barraID = [t for t in self.barraID if t['tempo'] != self.tempoAtual-1] # remove os elementos da lista que contem o tempo atual
                
                self.tempoAtual -=1  # Volta o tempo em 1
                WriteLockBox(self.tempoAtualEntry, self.tempoAtual) # Desbloqueia para escrever e bloqueia novamente o campo de texto e atualizar na tela

    # Função para criar as todas as barras referentes a um único tempo, as inativas e ativas
    def CriarBarras(self):
        # barra = para armazer o id do retangulo
        # barraText = para armazenar o id do texto que está contido dentro da barra

        self.barra, self.barraText = CriarBarra(
                    self.canvasGantt, 
                    self.graficoConfig, 
                    self.instrucoes[self.tempoAtual], 
                    self.maxTid, 
                    self.PegarInfoBarra)
        # barraID = lista contendo um conjunto de dados e o tempoAtual da simulação passo a passo, 
        # usado para conseguir identificar quais barras apagar ao "voltar"
        self.barraID.append(
            {
                'barra' : self.barra,
                'barraText' : self.barraText,
                'tempo' : self.tempoAtual
            }
        )

        # Loop para criar as barras inativas no tempo atual
        for i in range(len(self.instrucoesInativos)):
            if self.instrucoesInativos[i]['ingressoTempo'] == self.tempoAtual:
                self.barra, self.barraText = CriarBarra(
                    self.canvasGantt, 
                    self.graficoConfig, 
                    self.instrucoesInativos[i], 
                    self.maxTid, 

                    self.PegarInfoBarra)
                
                self.barraID.append(
                    {
                        'barra' : self.barra,
                        'barraText' : self.barraText,
                        'tempo' : self.tempoAtual
                    }
                )

    # Função para gerar um .png do gráfico gantt, OBS: UTILIZA A BIBLIOTECA matplotlib
    def SalvarDiagrama(self):
        self.IniciarSimulacao() # Inicia a simulação caso ela não tenha sido iniciada, dependendo parâmetros inicial selecionados
        self.instrucoesUnidas = self.instrucoes + self.instrucoesInativos # Une as instrucoes dos blocos inativos com os ativos
        
        tarefas = [] # Define onde em Y cada bloco vai ficar
        inicio = [] # Define onde cada bloco deve ser desenhado inicialmente
        duracao = [] # Define o quão largo cada bloco será, a princípio será do tamanho de uma unidade de tempo
        tCores = [] # Define a cor de cada bloco

        totalTarefas = len(self.tarefas) # Define o tamanho
        tempoMax = len(self.instrucoes)

        self.instrucoesUnidas = sorted(self.instrucoesUnidas, key=lambda x:x['id'])

        # Loop para incluir cada instrucao nas suas devidas listas
        for i in range(len(self.instrucoesUnidas)):
            tarefas.append(f"T{self.instrucoesUnidas[i]['id']}")
            duracao.append(1)
            inicio.append(self.instrucoesUnidas[i]['ingressoTempo'])
            tCores.append(cores[self.instrucoesUnidas[i]['cor']])
        
        fig, ax = plt.subplots(figsize=(tempoMax, totalTarefas)) # Para facilitar o controle dos conteudos em ax

        # Gera gráfico efetivamente  de acordo com o conteudo das listas em ordem
        ax.barh(tarefas, duracao, left=inicio, color=tCores, edgecolor='black')
        
        # Loop para escrever em cada 'bloco' um texto para reforçar qual tarefa pertence
        for i in range(len(tarefas)):
            ax.text(inicio[i] + duracao[i]/2, tarefas[i], f"T{self.instrucoesUnidas[i]['id']}", va='center', ha='center', color='black', fontweight='bold', fontsize=9)
                
        plt.xlim(0,tempoMax) # Remove o vão que ficaria na geração da imagem no último tempo
        plt.xticks(range(0,tempoMax+1)) # Faz com que o gráfico mostre todos os números no eixo do tempo ao invés de 2 em 2
        plt.xlabel('Tempo') # Titulo do eixo X
        plt.title(f"Gráfico de Gantt: {self.algoritmo}") # Titulo do gráfico

        # Salva como imagem
        plt.savefig('gantt.png', dpi=150, bbox_inches='tight') 
        plt.close()

simulador = SimulEscal()
        

        

