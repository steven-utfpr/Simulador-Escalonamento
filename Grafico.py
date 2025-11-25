
# Lista de cores para pegar a partir de um indice
cores = ['white', 'red', 'blue', 'green', 'yellow', 'purple', 'orange', 'pink', 'cyan', 'magenta', 'lime', 'teal',
          'lavender', 'brown', 'beige', 'maroon', 'navy', 'olive', 'coral', 'grey', 'black']

# Funcao para gerar o gráfico
def GerarGrafico(canvasGantt, config, instrucoes, instrucoesInativas, maxTempo, maxTid, usarPasso, PegarInfoBarra=None):
    canvasGantt.delete("all") # Apaga todo o conteudo do gráfico, para garantir que desenhos passado não afetem a atual
    
    CriarBordas(canvasGantt, config, maxTempo, maxTid) # Desenha as bordas do gráfico
    CriarEixos(canvasGantt, config, maxTempo, maxTid) # Desenha os eixos indicando onde está cada tempo e tarefa
    if not usarPasso: # Condição para verificar se está usando o passo a passo    
        # Loop para gerar os blocos das tarefas ativas
        for instrucao in instrucoes:
            if instrucao['id'] != -1:
                CriarBarra(canvasGantt, config, instrucao, maxTid, PegarInfoBarra)
        # Loop para gerar os blocos indicando a tarefa inativa
        for instrucaoInativa in instrucoesInativas:
            CriarBarra(canvasGantt, config, instrucaoInativa, maxTid, PegarInfoBarra)
               
# Funcao para apagar uma barra de acordo com seu "ID", utilizado no passo a passo
def ApagarBarra(canvasGantt, barra, barraText):
    canvasGantt.delete(barra) # Apaga o retangulo/bloco
    canvasGantt.delete(barraText) # Apaga o texto em cima dele

# Cria uma barra
def CriarBarra(canvasGantt,config, instrucao, maxTid, PegarInfoBarra=None):
    escalaX = config['escalaX']
    escalaY = config['escalaY']
    tempoAtual = instrucao['ingressoTempo']
    tidAtual = instrucao['id']-1
    cor = instrucao['cor']

    xMin = escalaX * (tempoAtual+1) # Posição inicial no eixo X
    xMax = escalaX * (tempoAtual+1) + escalaX # Posição final no eixo X, fechando o retângulo criado no espaço de tempo
    yMin = (escalaY  * (maxTid - tidAtual)) + 5 # Posição inicial no eixo Y, utilizando id como multiplicador
    yMax = (escalaY  * (maxTid - tidAtual)) + escalaY  # Posição final no eixo Y, fechando o retângulo criado com a base inicial em yMin
    rectID = canvasGantt.create_rectangle(xMin, yMin, xMax, yMax, fill=cores[cor], outline="black") # Cria efetivamente o retangulo
    rectTextID = canvasGantt.create_text((xMin + xMax) / 2, (yMin + yMax) / 2, text=f"T{tidAtual+1}", fill="black") # Cria efetivamente o texto
    
    # Função de destaque (hover)
    def on_enter(event):
        canvasGantt.itemconfig(rectID, width=3, outline="darkblue")  # destaca
    
    def on_leave(event):
        canvasGantt.itemconfig(rectID, width=1, outline="black") # volta ao normal
    
    # Associa a funcao criada anteriormente para funcionar o highlight ao dar hover
    canvasGantt.tag_bind(rectID, "<Enter>", on_enter)
    canvasGantt.tag_bind(rectID, "<Leave>", on_leave)
    canvasGantt.tag_bind(rectTextID, "<Enter>", on_enter)
    canvasGantt.tag_bind(rectTextID, "<Leave>", on_leave)
    
    if PegarInfoBarra is not None: # Verifica se foi entregue as informações relacionados a barra/bloco
        # Associa o bloco a uma função em SimulEscal.py, para exibir as informações do bloco no "Log do bloco"
        canvasGantt.tag_bind(rectID, "<Button-1>", lambda event, i=instrucao: PegarInfoBarra(i))
        canvasGantt.tag_bind(rectTextID, "<Button-1>", lambda event, i=instrucao: PegarInfoBarra(i))

    return rectID, rectTextID

# Funcao para criar as bordas do grafico
def CriarBordas(canvasGantt, config, maxTempo, maxTid):
    escalaX = config['escalaX']
    escalaY = config['escalaY']
    # Desenha um retângulo ao redor do gráfico, simulando uma borda externa
    canvasGantt.create_rectangle(escalaX, escalaY, (maxTempo+1) * escalaX, ((maxTid + 1) * escalaY) +15, width=2)    
    # OBS: retangulo é reaproveitado para ser usado os eixos X e Y

# Funcao para criar os eixos X do tempo e Y das tarefas
def CriarEixos(canvasGantt, config, maxTempo, maxTid):
    
    maxEixoY = (maxTid+2) * config['escalaY'] # definir o tamanho maximo do eixo Vertical
    escalaX = config['escalaX']
    escalaY = config['escalaY']

    # Eixo X - Cria o eixo Horizontal X do tempo
    # Loop para marcar cada instante de tempo no eixo X com um |
    for t in range(maxTempo+1):   
        x =  escalaX + t * escalaX # Calcula a posição X para o tempo 't'        
        canvasGantt.create_text(x, maxEixoY +15, text=str(t), font=("Arial", 9)) # Exibe o número do tempo abaixo da linha do eixo X        
        canvasGantt.create_line(x, maxEixoY- 15, x, maxEixoY +5, width=2)  # Desenha pequenas marcas verticais no eixo X
    # Eixo Y - Cria o eixo Vertical Y das tarefas
    # Loop para marcar cada tarefa no eixo Y com -
    for t in range(maxTid):
        canvasGantt.create_text(escalaX-25, (escalaY * (t +1))+15 , text="t"+str(maxTid-t) , font=("Arial", 9)) # Exibe o nome da tarefa
        canvasGantt.create_line(escalaX-10, (escalaY * (t +1))+15, escalaX, (escalaY * (t +1))+15, width=2) # Cria a linha para marcar a quem pertence a tarefa


