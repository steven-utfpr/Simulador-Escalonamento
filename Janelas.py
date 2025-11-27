import tkinter as tk

from Funcoes import WriteLockBox

# Funcao principal para criar toda a interface
def CriarInterface(self):
    # Objeto janela
    janelaPrincipal = tk.Tk() # Definir a janela principal
    # Titulo da janela
    janelaPrincipal.title("Simulador SO") # Dá um nome para a janela
    # Definindo o tamanho 
    janelaPrincipal.geometry ("1280x720") # Define o tamanho inicial da janela

    # frameInfo = guarda o painel contendo os elementos criados relacionado ao log do bloco
    # frameGantt = guarda o painel contendo os elementos relacionados ao desenho do gráfico    
    # frameConfig = guarda o painel contendo os elementos relacionado as configurações

    # logBox = guarda o objeto da caixa de texto onde é escrito os logs
    # tempoAtualEntry = guarda o objeto do campo de escrita do tempo atual (entre os botões de avançar e voltar)
    # arqAtualEntry = guarda o objeto do campo de escrita do nome do arquivo    
    # canvasGantt = guarda o canvas onde é desenha o gráfico

    frameInfo, logBox = CriarTelaInfos(janelaPrincipal) # Cria a parte contendo as o "Log do bloco" para exibir detalhes
    frameConfig, tempoAtualEntry, arqAtualEntry = CriarTelaConfig(self,janelaPrincipal) # Cria a parte contendo as configurações e botões de interação
    frameGantt, canvasGantt = CriarTelaGantt(janelaPrincipal) # Cria a parte onde será desenhada o gráfico

    return janelaPrincipal, frameInfo, logBox, frameConfig, frameGantt, canvasGantt, tempoAtualEntry, arqAtualEntry

# Cria o painel Esquerdo contendo as configurações e informações basicas
def CriarTelaConfig(self,root):
    
    # Defini as configurações iniciais do painel
    frame = tk.Frame(root, width=200, height=600, bg="lightgray", padx=10, pady=10)
    frame.pack(side="left", fill="y") # Trava ele na esquerda da janela principal e preenche ele na vertical
    # Configura as grids para facilitar o controle e posicionamento dos elementos
    frame.grid_columnconfigure(0, weight=1) 
    frame.grid_columnconfigure(1, weight=1)
    
    # Conteúdo do painel esquerdo
    tituloConfig = tk.Label(frame, text="Configurações", font=("Arial", 12), bg="lightgray") # Texto do painel
    btnIniciar = tk.Button(frame, text="Iniciar", command= self.IniciarSimulacao, bg="green", fg="white", width=10, height=2) # Botão para iniciar a simulação
    btnGerar = tk.Button(frame, text="Gerar IMG", command= self.SalvarDiagrama, bg="green", fg="white", width=10, height=2) # Botão para gerar um png da simulação
    tituloArqSel = tk.Label(frame, text="Arquivo Selecionado:", bg="lightgray") # Texto do arqAtualEntry, para indicando o que é o campo onde o nome do arquivo selecionado é exibido
    
    arqAtualEntry = tk.Entry(frame, width=20) # Campo onde é escrito o arquivo selecionado
    WriteLockBox(arqAtualEntry, "config.txt") # Escreve e trava ele com um texto inicial
        
    btnProcurar = tk.Button(frame, text="Procurar", command= self.PegarCaminho, font=("Arial", 12)) # Botão para procurar por um arquivo contendo as informações para simular 
        
    checkboxPasso = tk.Checkbutton(frame, text="Passo a Passo", command=lambda: self.CheckPasso()) # Checkbox para definir se quer usar o passo a passo
    btnAvanc = tk.Button(frame, text=">", command=lambda: self.AvancarPasso(), bg="green", fg="white", width=3) # Botão de Avançar uma etapa no passo a passo
    btnVolta = tk.Button(frame, text="<", command=lambda: self.VoltarPasso(), bg="green", fg="white", width=3) # Botão para voltar uma etapa no passo a passo
    
    campoTempoAtual = tk.Entry(frame, width=5) # Campo onde será escrito o tempo atual da simulação passo a passo
    campoTempoAtual.insert(0,"0") # Inicia ele com o texto em 0
        
    # Define uma variável para controlar as mudanças em texto relaciona ao algoritmo atual e quantum atual
    self.infoAlgo = tk.StringVar() 
    self.infoAlgo.set("Algoritmo:")
    self.infoQuantum = tk.StringVar()
    self.infoQuantum.set("Quantum:")
        
    infoAlgo = tk.Label(frame, textvariable=self.infoAlgo, font=("Arial", 12), bg="lightgray") # Cria o texto onde será escrito o algoritmo usado
    infoQuantum = tk.Label(frame, textvariable=self.infoQuantum, font=("Arial", 12), bg="lightgray") # Cria o texto onde será escrito o quantu,
    labelTempo = tk.Label(frame, text="Tempo", font=("Arial", 10), bg="lightgray") # Cria um pequeno titulo indicar a que se refere o campoTempoAtual na interface
    infoExtra = tk.Label(frame, text="Clique na Barra\n para ver mais\n Informações\n \\\\\\\\ = Mutex \n ////= IO", font=("Arial", 12), bg="lightgray") # Cria um texto para mostrar que dá para clicar nos blocos

    # Configuração da grid para posicionar cada elemento dentro do painel de Configurações
    tituloConfig.grid(row=0, column=0, padx=2, pady=5)
    btnIniciar.grid(row=1, column=0, padx=2, pady=5, )
    btnGerar.grid(row=2, column=0, padx=2, pady=5, )
    tituloArqSel.grid(row=3, column=0, padx=2, pady=5)
    arqAtualEntry.grid(row=4, column=0, padx=2, pady=5)
    btnProcurar.grid(row=5, column=0, padx=1, pady=5) 

    labelTempo.grid(row=6, column=0, padx=2, pady=1)  
    btnAvanc.grid(row=7, column=0, padx=2, pady=5, sticky="e")
    btnVolta.grid(row=7, column=0, padx=2, pady=5, sticky="w")    
    campoTempoAtual.grid(row=7, column=0, padx=2, pady=1)        
    checkboxPasso.grid(row=8, column=0, padx=2, pady=5)

    infoAlgo.grid(row=9, column=0, padx=2, pady=5)
    infoQuantum.grid(row=10, column=0, padx=2, pady=5)      
    infoExtra.grid(row=11, column=0, padx=2, pady=5)  

    return frame, campoTempoAtual, arqAtualEntry

# Função para criar o painel direito onde será desenhada o gráfico
def CriarTelaGantt(root):
    
    # Configurações iniciais do painel
    frame = tk.Frame(root, width=600, height=250, bg="lightgray", padx=10, pady=10) 
    frame.pack(side="right", fill="both", expand=True) # trava ele na janela

    # Texto para indicar que o campo será onde vai ser desenhado o gráfico
    tk.Label(frame, text="Gráfico de Gantt", font=("Arial", 12),bg="lightgray").pack()

    # Cria um canvas, um campo onde será feito efetivamente o desenho do gráfico
    canvas = tk.Canvas(frame, bg="white", height=250)
    canvas.pack(fill="both", expand=True) # trava ele em relação ao painel
    
    # Configura o scroll Vertical para caso tenho muitas tarefas para exibir
    vScroll = tk.Scrollbar(canvas, orient="vertical", command=canvas.yview)
    vScroll.pack(side="right", fill="y") # Preenche o lado direito do painel com o scroll vertical

    # Configura o scroll para caso tenha um tempo maximo muito alto
    hScroll = tk.Scrollbar(canvas, orient="horizontal", command=canvas.xview)
    hScroll.pack(side="bottom", fill="x", padx=10) # Preenche a parte de baixo do painel com o scroll horizontal

    canvas.config(yscrollcommand=vScroll.set, xscrollcommand=hScroll.set) # Configuração de controle para o quanto o scroll pode ir e mover o canvas
    
    return frame, canvas

# Função para criar o painel debaixo onde será exibida informações adicionais
def CriarTelaInfos(root):

    # Configurações iniciais do painel
    frame = tk.Frame(root, height=200, bg="black", padx=10, pady=25)
    frame.pack(side="bottom", fill="x") # Trava o painel na parte de baixo da janela
    frame.pack_propagate(False) # Permite que o height em frame seja utilizado corretamente
    tk.Label(frame, text="Logs do Bloco", fg="white", bg="black").pack() # Texto para indicar para que serve o painel

    # Configuração inicial do bloco de texto onde será escrito as informações
    log = tk.Text(frame, height=40, bg="black", fg="lime", font=("Courier", 10), pady=15)
    log.pack(fill="both", expand=True) # Preenche ele dentro do proprio painel

    # Cria um scroll vertical para navegar no bloco de texto quando é clicado vários blocos
    scroll = tk.Scrollbar(log, orient="vertical", command=log.yview) 
    scroll.pack(side="right", fill="y") # Preenche o lado direito do painel com o scroll vertical
    log.config(yscrollcommand=scroll.set) # Configuração de controle para o quanto o scroll pode ir e mover no bloco de texto

    return root, log
