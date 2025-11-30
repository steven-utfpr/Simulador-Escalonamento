import tkinter as tk
import os

from Funcoes import WriteLockBox, Salvar

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
    btnEditar = tk.Button(frame, text="Editar", command=self.AbrirJanelaEdicao, font=("Arial", 12)) # Botão para procurar por um arquivo contendo as informações para simular 
        
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
    btnProcurar.grid(row=5, column=0, padx=1, pady=5, sticky="w") 
    btnEditar.grid(row=5, column=0, padx=1, pady=5, sticky="e") 

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


    
# Funcao para abrir a janela de edições e montar sua interface
def AbrirEdicao(root, caminho, tarefas, algoritmo, quantum, alpha):

    # Atribuindo a variavel da janela para facilitar atribução de frame e blocos
    edJanela = tk.Toplevel(root)
    edJanela.title("Edição de Tarefas") # Nome da nova janela
    edJanela.geometry("550x600") # Tamanho da nova janela
    frameArquivo = tk.Frame(edJanela, padx=10, pady=10, relief="groove", bd=1) # Primeiro retângulo no topo
    frameArquivo.pack(fill="x", padx=10, pady=(10, 5)) 

    # Verificação para definir o nome inicial que vai estar escrito na barra
    if caminho:
        nomeArquivo = os.path.basename(caminho) # Utiliza o nome do arquivo + extensão
    else:
        nomeArquivo = "Novo Arquivo.txt" # Escreve automaticamente esse nome no campo

    # Titulo do retângulo segurando as informações iniciais de algoritmo, quantum , alpha e nome do arquivo
    tk.Label(frameArquivo, text="Configuração Geral", font=("Arial", 10, "bold")).pack(anchor="w")


    linha = tk.Frame(frameArquivo)
    linha.pack(fill="x", pady=5)

    # Linha para nome do arquivo
    retanguloArq = tk.Frame(frameArquivo)
    retanguloArq.pack(fill="x", pady=5)

    tk.Label(retanguloArq, text="Salvar como:", width=12, anchor="w").pack(side="left")
    nomeArqText = tk.StringVar(value=nomeArquivo)
    entryArq = tk.Entry(retanguloArq, textvariable=nomeArqText, width=30)
    entryArq.pack(side="left", padx=5)    

    # Interface para o campo Algoritmo 
    algoritmoTextEntry = tk.StringVar(value=algoritmo)  # ← valor inicial aqui funciona!
    algoritmosMenu = tk.OptionMenu(linha, algoritmoTextEntry, "FIFO", "SRTF", "PrioP", "PrioEnv") # Cria um dropbox para selecionar o tipo de algoritmo
    algoritmosMenu.config(width=8)  # ajusta largura (aprox. 8 chars)
    algoritmosMenu.pack(side="left", padx=5)

    # Interface para o campo  Quantum
    tk.Label(linha, text="Quantum:", width=8, anchor="w").pack(side="left")
    quantumTextEntry  = tk.IntVar(value=quantum)
    tk.Spinbox(linha, from_=1, to=100, textvariable=quantumTextEntry , width=5).pack(side="left", padx=5)

    #  Interface para o campo Alpha (para envelhecimento)
    tk.Label(linha, text="Alpha:", width=6, anchor="w").pack(side="left")
    alphaTextEntry  = tk.IntVar(value=alpha)
    tk.Spinbox(linha, from_=0, to=10, textvariable=alphaTextEntry , width=5).pack(side="left", padx=5)
    
    # Scroll principal para caso os blocos das tarefas fique muito grande 
    canvas = tk.Canvas(edJanela) # Area de desenho onde o scroll vai rolar
    scrollbar = tk.Scrollbar(edJanela, orient="vertical", command=canvas.yview) # Barra de rolagem
    frameEdicao = tk.Frame(canvas) # Container para rolar a tela quando se tem muitos blocos
    frameEdicao.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    # Lista para guardar referências aos frames de tarefas
    blocosTarefa = []
    # Frame para botões (acima dos blocos)
    frameBotoes = tk.Frame(edJanela)
    frameBotoes.pack(fill="x", padx=10, pady=(10, 5))

    # Botão de Adicionar Nova Tarefa
    btnAdd = tk.Button(frameBotoes, text="Nova Tarefa",
                        command=lambda: CriarBlocoTarefa(frameEdicao, blocosTarefa, None),
                        bg="#4CAF50", fg="white", font=("Arial", 10), width=18)
    btnAdd.pack(side="left", padx=5)
    
    # Criando e atribuindo a funcionalidade do botao de Salvar() com os parâmetros
    btnSalvar = tk.Button(
    frameBotoes,
    text="Salvar",
    command=lambda: Salvar(
        blocosTarefa,
        algoritmoTextEntry.get(),   
        quantumTextEntry.get(),
        alphaTextEntry.get(),
        nomeArqText.get(),
        caminho            
    ),
    bg="#2196F3", fg="white", font=("Arial", 10), width=10
    )
    btnSalvar.pack(side="left", padx=5)
        
    canvas.create_window((0, 0), window=frameEdicao, anchor="nw") # Coloca o frameEdicao dentro do canvas
    canvas.configure(yscrollcommand=scrollbar.set) # Para atualizar a posição do scrollvar

    canvas.pack(side="left", fill="both", expand=True, padx=10, pady=5)
    scrollbar.pack(side="right", fill="y")

    # Loop para popular automaticamente os blocos quando é entregue um arquivo valido contendo
    # as tarefas
    for tarefa in tarefas:
        CriarBlocoTarefa(frameEdicao, blocosTarefa, tarefa)

    # Retorna a janela para guardar sua referencia e evitar poder ficar abrindo mais janelas
    return edJanela

# === Função interna: criar bloco de tarefa ===
def CriarBlocoTarefa(root, blocosTarefa, tarefa=None):
    # Bloco de interface para uma tarefa
    frameTarefa = tk.Frame(root, bd=2, relief="solid", padx=10, pady=8)
    frameTarefa.pack(fill="x", pady=8)

    # Se tarefa foi fornecida
    if tarefa:
        nome = tarefa['nome']
        cor = tarefa['cor']
        ingresso = tarefa['ingressoTarefa']
        duracao = tarefa['duracao']
        prioridade = tarefa['prioridade']
        eventos = tarefa['eventos']
    else:
        # Determina nome padrão baseado na quantidade de blocos já criados
        proximo_id = len(blocosTarefa) + 1
        nome = f"T{proximo_id}"
        cor = "#FF0000"
        ingresso = 0
        duracao = 1
        prioridade = 1
        eventos = []

    # Variáveis que serao utilizada na hora de salvar, por ser tk. é necessario fazer um .get()
    # Para pegar o valor contido neles
    nomeTextEntry = tk.StringVar(value=nome)
    corTextEntry = tk.StringVar(value=cor)
    ingressoTextEntry = tk.IntVar(value=ingresso)
    duracaoTextEntry = tk.IntVar(value=duracao)
    prioTextEntry = tk.IntVar(value=prioridade)

    # Informacoes principais contidas no frame para ter mais controle de posicionamento
    infosPrincipais = tk.Frame(frameTarefa)
    infosPrincipais.pack(fill="x")
    
    # APENAS PARA MELHORAR A INTERFACE ================================================
    # Função para atualizar a cor do frame
    def atualizarCorBloco(*_):
        valor = corTextEntry.get().strip()
        # Normaliza: aceita FFF, #FFF, fff, #ff0011, etc.
        if valor.startswith('#'):
            hex_cor = valor
        else:
            hex_cor = '#' + valor

        # Validação simples de HEX e tem 3 ou 6 dígitos após #
        if len(hex_cor) in (4, 7) and all(c in '0123456789abcdefABCDEF' for c in hex_cor[1:]):
            try:
                frameTarefa.configure(bg=hex_cor)
                # Também atualiza o fundo do cabeçalho e eventos (opcional)
                infosPrincipais.configure(bg=hex_cor)
                # frameEventos.configure(bg=hex_cor + "33")  # mais claro (só se quiser)
            except tk.TclError:
                frameTarefa.configure(bg="lightgray")  # fallback
        else:
            frameTarefa.configure(bg="lightgray")  # inválido → cinza

    # Vincula a atualização ao campo de cor
    corTextEntry.trace_add("write", atualizarCorBloco)
    
     # Chama a funcao para garantir que seja colorido o bloco quando é ele preenchido automaticamente
    atualizarCorBloco()
    # ===========================================================================

    # Nome
    tk.Label(infosPrincipais, text="Nome:").pack(side="left")
    tk.Entry(infosPrincipais, textvariable=nomeTextEntry, width=6).pack(side="left", padx=5)
    # Cor
    tk.Label(infosPrincipais, text="Cor:").pack(side="left")
    tk.Entry(infosPrincipais, textvariable=corTextEntry, width=7).pack(side="left", padx=5)
    # Ingresso
    tk.Label(infosPrincipais, text="Ingr.:").pack(side="left")
    tk.Spinbox(infosPrincipais, from_=0, to=999, textvariable=ingressoTextEntry, width=5).pack(side="left", padx=5)
    # Duracao
    tk.Label(infosPrincipais, text="Dur.:").pack(side="left")
    tk.Spinbox(infosPrincipais, from_=1, to=999, textvariable=duracaoTextEntry, width=5).pack(side="left", padx=5)
    # Prioridade
    tk.Label(infosPrincipais, text="Prio.:").pack(side="left")
    tk.Spinbox(infosPrincipais, from_=1, to=100, textvariable=prioTextEntry, width=5).pack(side="left", padx=5)
    # Botao para excluir o bloco de tarefa
    tk.Button(infosPrincipais, text="X", command=frameTarefa.destroy, width=2).pack(side="right")

    # Bloco especifico contido no bloco de Tarefa, serve para
    # Controlar melhor o seu posicionamento ao criar novos eventos para a tarefa
    frameEventos = tk.Frame(frameTarefa, padx=10, pady=5)
    frameEventos.pack(fill="x", pady=(6, 0))
    tk.Label(frameEventos, text="Eventos:", font=("Arial", 9, "bold")).pack(anchor="w")

    # Variavel para armazenar os eventos relacionado a tarefa em que ele está contido
    eventosLocais = []
    
    # Adiciona eventos iniciais mo bloco da tarefa caso ele tenha
    # Apenas para auto-popular os campos caso seja entregue um arquivo valido
    for ev in eventos:
        AddEvento(frameEventos, eventosLocais, ev)

    # Botão para adicionar novo evento 
    # Sendo atrelado a função do botao e entrega de parametros
    tk.Button(frameEventos, text="Novo Evento",
              command=lambda: AddEvento(frameEventos, eventosLocais),
              padx=5).pack(anchor="w", pady=4)

    # Salva referências
    frameTarefa.dados = {
        'nome': nomeTextEntry,        
        'cor': corTextEntry,          
        'ingresso': ingressoTextEntry,
        'duracao': duracaoTextEntry,  
        'prioridade': prioTextEntry,  
        'eventos': eventosLocais
    }
    
    # Adiciona na lista para ser tratado mais tarde na hora de escrever no arquivo
    blocosTarefa.append(frameTarefa)

# Funcao atribuida ao botao do "Novo Evento"
def AddEvento(frame_eventos, eventosLista, evento=None):
    # Bloco de interface para uma evento contido dentro do bloco de tarefas
    eventoFrame = tk.Frame(frame_eventos)
    eventoFrame.pack(fill="x", pady=2)

    # Define todas as variáveis iniciais para evitar erros quando nao se tem um evento
    inicioTextEntry = tk.IntVar(value=0)
    duracaoTextEntry = tk.IntVar(value=1)
    mutexTextEntry = tk.IntVar(value=1)
    instanteTextEntry = tk.IntVar(value=0)
    
    # Define o tipo inicial para evitar problemas quando o evento é vazio
    tipoInicial = evento['tipo'] if evento else "IO"
    tipoTextEntry = tk.StringVar(value=tipoInicial)  # ← essencial!

    # Serve para auto-popular os campos quando for dado um evento não vazio na função
    if evento:
        if tipoInicial == 'IO':
            inicioTextEntry.set(evento.get('inicio', 0))
            duracaoTextEntry.set(evento.get('duracao', 1))
        else:  # 'ML' ou 'MU'
            mutexTextEntry.set(evento.get('mutexID', 1))
            instanteTextEntry.set(evento.get('duracao', 0))
    
    # Botão remover o proprio evento, deletando ele mesmo e da lista de eventos
    btnRemover = tk.Button(
        eventoFrame,
        text="X",
        width=2,
        command=lambda: RemoverEvento(eventoFrame, eventosLista, eventoInfo)
    )
    btnRemover.pack(side="right")

    # Menu para os tipo de evento
    tk.OptionMenu(eventoFrame, tipoTextEntry, "IO", "ML", "MU").pack(side="left")

    # Widgets para IO
    ioWidgets = [
        tk.Label(eventoFrame, text=" início="),
        tk.Spinbox(eventoFrame, from_=0, to=999, textvariable=inicioTextEntry, width=4),
        tk.Label(eventoFrame, text=", duração="),
        tk.Spinbox(eventoFrame, from_=1, to=999, textvariable=duracaoTextEntry, width=4)
    ]

    # Widgets para ML/MU
    mutexWidgets = [
        tk.Label(eventoFrame, text=" mutexID: "),
        tk.Spinbox(eventoFrame, from_=1, to=50, textvariable=mutexTextEntry, width=3),
        tk.Label(eventoFrame, text=", instante="),
        tk.Spinbox(eventoFrame, from_=0, to=999, textvariable=instanteTextEntry, width=4)
    ]

    # Função para atualizar entre o widgets do IO com o ML,MU dependendo da seleção
    def AtualizarTipo(*_):
        # Remove todos os widgets
        for w in ioWidgets + mutexWidgets:
            w.pack_forget()
        # Mostra os corretos
        if tipoTextEntry.get() == "IO":
            for w in ioWidgets:
                w.pack(side="left")
        else:
            for w in mutexWidgets:
                w.pack(side="left")

    # Vincula a atualização a mudança do tipo
    tipoTextEntry.trace_add("write", AtualizarTipo)
    AtualizarTipo()  # inicializa

    # Cria estrutura de dados do evento    
    eventoInfo = {
        'tipo': tipoTextEntry,       
        'inicio': inicioTextEntry,    
        'duracao': duracaoTextEntry,  
        'mutex': mutexTextEntry,      
        'instante': instanteTextEntry 
    }

    # Adiciona a lista fornecida 
    eventosLista.append(eventoInfo)

# Função auxiliar interna (opcional, só para encapsular remoção)
def RemoverEvento(frame, lista, info):
    frame.destroy()
    if info in lista:
        lista.remove(info)