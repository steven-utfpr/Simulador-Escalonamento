import tkinter as tk
import matplotlib.pyplot as plt

from collections import deque
from Funcoes import GerarInstrucoes, ResetarValores

cores = ['white', 'red', 'blue', 'green', 'yellow', 'purple', 'orange', 'pink', 'cyan', 'magenta', 'lime', 'teal',
          'lavender', 'brown', 'beige', 'maroon', 'navy', 'olive', 'coral', 'grey', 'black']

def GerarGrafico(canvasGantt, config, instrucoes, instrucoesInativas, maxTempo, maxTid, usarPasso, PegarInfoBarra=None):
    canvasGantt.delete("all")
    #ResetarValores(self)    
    CriarBordas(canvasGantt, config, maxTempo, maxTid)
    CriarEixos(canvasGantt, config, maxTempo, maxTid)
    if not usarPasso:
        for instrucao in instrucoes:
            CriarBarra(canvasGantt, config, instrucao['ingressoTempo'], maxTid, instrucao['id']-1, instrucao['cor'], PegarInfoBarra)
            for instrucaoInativa in instrucoesInativas:
                CriarBarra(canvasGantt, config, instrucaoInativa['ingressoTempo'], maxTid, instrucaoInativa['id']-1, instrucaoInativa['cor'], PegarInfoBarra)
            
                   

def ApagarBarra(canvasGantt, barra, tempoAtual):
    canvasGantt.delete(barra[tempoAtual]['barra'])
    canvasGantt.delete(barra[tempoAtual]['barraText'])
    del barra[tempoAtual]

def CriarBarra(canvasGantt,config, tempoAtual, maxTid, tidAtual, cor, PegarInfoBarra=None):
    escalaX = config['escalaX']
    escalaY = config['escalaY']
    xMin = escalaX * (tempoAtual+1) # Posição inicial no eixo X
    xMax = escalaX * (tempoAtual+1) + escalaX # Posição final no eixo X, fechando o retângulo criado no espaço de tempo
    yMin = (escalaY  * (maxTid - tidAtual)) + 5 # Posição inicial no eixo Y, utilizando id como multiplicador
    yMax = (escalaY  * (maxTid - tidAtual)) + escalaY  # Posição final no eixo Y, fechando o retângulo criado com a base inicial em yMin
    rectID = canvasGantt.create_rectangle(xMin, yMin, xMax, yMax, fill=cores[cor], outline="black")
    rectTextID = canvasGantt.create_text((xMin + xMax) / 2, (yMin + yMax) / 2, text=f"T{tidAtual+1}", fill="black")    
    
     # Função de destaque (hover)
    def on_enter(event):
        canvasGantt.itemconfig(rectID, width=3, outline="darkblue")  # destaca

    def on_leave(event):
        canvasGantt.itemconfig(rectID, width=1, outline="black")     # volta ao normal

    canvasGantt.tag_bind(rectID, "<Enter>", on_enter)
    canvasGantt.tag_bind(rectID, "<Leave>", on_leave)
    canvasGantt.tag_bind(rectTextID, "<Enter>", on_enter)
    canvasGantt.tag_bind(rectTextID, "<Leave>", on_leave)

    if PegarInfoBarra is not None:
        canvasGantt.tag_bind(rectID, "<Button-1>", lambda event: PegarInfoBarra(tid = tidAtual, tempo = tempoAtual))
        canvasGantt.tag_bind(rectTextID, "<Button-1>", lambda event: PegarInfoBarra(tid = tidAtual, tempo = tempoAtual))

    return rectID, rectTextID

def CriarBordas(canvasGantt, config, maxTempo, maxTid):
    escalaX = config['escalaX']
    escalaY = config['escalaY']
    canvasGantt.create_rectangle(escalaX, escalaY, (maxTempo+1) * escalaX, ((maxTid + 1) * escalaY) +15, width=2)
    # Desenha um retângulo ao redor do gráfico, simulando uma borda externa

def CriarEixos(canvasGantt, config, maxTempo, maxTid):
    
    maxEixoY = (maxTid+2) * config['escalaY']
    escalaX = config['escalaX']
    escalaY = config['escalaY']
    # Eixo X - tempo
    #self.canvasGantt.create_line( escalaX, maxEixoY -10, self.tempoMax * escalaX, maxEixoY-10, width=1)
    # Desenha a linha horizontal do eixo X (tempo), posicionada acima da parte inferior
    for t in range(maxTempo+1):
    # Loop para marcar cada instante de tempo no eixo X (0 até 7)
        x =  escalaX + t * escalaX
        # Calcula a posição X para o tempo 't'
        canvasGantt.create_text(x, maxEixoY +15, text=str(t), font=("Arial", 9))
        # Exibe o número do tempo abaixo da linha X
        canvasGantt.create_line(x, maxEixoY- 15, x, maxEixoY +5, width=2)
        # Desenha pequenas marcas verticais no eixo X
    # Eixo Y - Cria o eixo Vertical Y
    #self.canvasGantt.create_line(escalaX, escalaY , escalaX, maxEixoY , width=1)
    # Cria as linhas horizontais do eixo Y para indicar as tarefas
    for t in range(maxTid):
        canvasGantt.create_text(escalaX-25, (escalaY * (t +1))+15 , text="t"+str(maxTid-t) , font=("Arial", 9))
        canvasGantt.create_line(escalaX-10, (escalaY * (t +1))+15, escalaX, (escalaY * (t +1))+15, width=2)       


def diagramTeste():
    # Dados de exemplo
    tarefas = ['T1', 'T2', 'T3']
    inicio = [0, 2, 5]
    duracao = [3, 4, 2]
    cores = ['red', 'blue', 'green']

    # Gera gráfico
    plt.figure(figsize=(10, 4))
    plt.barh(tarefas, duracao, left=inicio, color=cores, edgecolor='black')
    plt.xlabel('Tempo')
    plt.title('Gráfico de Gantt')

    # Salva como imagem
    plt.savefig('gantt.png', dpi=150, bbox_inches='tight')
    plt.close()