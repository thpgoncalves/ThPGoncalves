import pygame
import sys

# Configurações do jogo
largura_janela = 800
altura_janela = 600
tamanho_celula = 40 

# Cores do jogo
cor_parede = (0, 0, 0)
cor_caminho = (255, 255, 255)
cor_jogador = (0, 128, 255)

pygame.font.init()
fonte = pygame.font.SysFont(None, 40)

def carregar_labirinto(arquivo_labirinto):
    with open(arquivo_labirinto, 'r') as file:
        labirinto = [list(line.strip()) for line in file]
    return labirinto

def desenhar_labirinto(screen, labirinto):
    for row_index, row in enumerate(labirinto):
        for col_index, cell in enumerate(row):
            cor = cor_parede if cell == '#' else cor_caminho
            pygame.draw.rect(screen, cor, (col_index * tamanho_celula, row_index * tamanho_celula, tamanho_celula, tamanho_celula))
            if cell == 'E':
                pygame.draw.rect(screen, (255, 0, 0), (col_index * tamanho_celula, row_index * tamanho_celula, tamanho_celula, tamanho_celula))

def desenhar_jogador(screen, jogador):
    pygame.draw.rect(screen, cor_jogador, jogador)

def desenhar_temporizador(screen, tempo_restante):
    texto_temporizador = fonte.render(f"Tempo Restante: {tempo_restante} s", True, (0, 255, 0))
    screen.blit(texto_temporizador, (10, 10))

def exibir_mensagem(screen, mensagem):
    texto = fonte.render(mensagem, True, (255, 255, 255))
    screen.blit(texto, ((largura_janela - texto.get_width()) // 2, (altura_janela - texto.get_height()) // 2))
    pygame.display.flip()
    pygame.time.delay(2000)  # Aguarda 2000 milissegundos (2 segundos)

def proximo_nivel(nivel):
    if nivel < 5:
        return nivel + 1
    else:
        return None
    
def main(nivel):
    global tamanho_celula  # Torna a variável global

    pygame.init()
    screen = pygame.display.set_mode((largura_janela, altura_janela))
    pygame.display.set_caption("Scape the Maze")

    clock = pygame.time.Clock()

    while nivel is not None:
        labirinto = carregar_labirinto(f"C:\\Users\\user\\Desktop\\Estudos Desenvolvimento\\Python\\Projetos\\labirinto{nivel}.txt")
        if nivel >= 3:
            tamanho_celula = 17
        
        jogador = pygame.Rect(2 * tamanho_celula, 2 * tamanho_celula, 0.84999 * tamanho_celula, 0.84999 * tamanho_celula)
        tempo_total = 30
        tempo_restante = tempo_total
        tempo_ultimo_segundo = pygame.time.get_ticks()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - tempo_ultimo_segundo >= 1000:
                tempo_restante -= 1
                tempo_ultimo_segundo = tempo_atual

            keys = pygame.key.get_pressed()

            velocidade_horizontal = tamanho_celula // 5.5
            velocidade_vertical = tamanho_celula // 5.5

            if keys[pygame.K_UP] and jogador.top - velocidade_vertical >= 0 and labirinto[int((jogador.top - velocidade_vertical) / tamanho_celula)][int(jogador.left / tamanho_celula)] != '#':
             jogador.top -= velocidade_vertical

            if keys[pygame.K_DOWN] and jogador.bottom < altura_janela and labirinto[int((jogador.bottom + velocidade_vertical) / tamanho_celula)][int(jogador.left / tamanho_celula)] != '#':
                jogador.top += velocidade_vertical

            if keys[pygame.K_LEFT] and jogador.left - velocidade_horizontal >= 0 and labirinto[int(jogador.top / tamanho_celula)][int((jogador.left - velocidade_horizontal) / tamanho_celula)] != '#':
                jogador.left -= velocidade_horizontal

            if keys[pygame.K_RIGHT] and jogador.right < largura_janela and labirinto[int(jogador.top / tamanho_celula)][int((jogador.right + velocidade_horizontal) / tamanho_celula)] != '#':
                jogador.left += velocidade_horizontal

            if labirinto[jogador.top // tamanho_celula][jogador.left // tamanho_celula] == 'E':
                exibir_mensagem(screen, f"Parabéns! Você concluiu o Nível {nivel}.")
                nivel = proximo_nivel(nivel)
                break

            screen.fill((0, 0, 0))
            desenhar_labirinto(screen, labirinto)
            desenhar_jogador(screen, jogador)
            desenhar_temporizador(screen, tempo_restante)

            if tempo_restante <= 0:
                exibir_mensagem(screen, "Tempo esgotado! Fim de Jogo.")
                nivel = None
                break

            pygame.display.flip()
            clock.tick(30)

if __name__ == "__main__":
    main(1)
