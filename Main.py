import pyautogui
import time
import os
import keyboard  # Certifique-se de instalar o módulo: pip install keyboard

# Configurações globais
IMAGES_FOLDER = 'assets'
CONFIDENCE = 0.7  # Reduzida para melhorar a detecção
SEARCH_REGION = (0, 0, 1920, 1080)  # Ajuste conforme sua tela (x, y, largura, altura)
REFRESH_INTERVAL = 10  # Segundos entre atualizações (refresh da página)
d
def refresh_page():
    """Atualiza a página pressionando F5 com delays adequados"""
    pyautogui.press('f5')
    time.sleep(3)  # Tempo para a página recarregar

def play_music():
    """Toca a música de alerta"""
    try:
        os.startfile(os.path.join(IMAGES_FOLDER, 'music.mp3'))
    except Exception as e:
        print(f"Erro ao tocar música: {e}")

def find_image(image_name):
    """Procura imagem na tela com tratamento de erros"""
    try:
        return pyautogui.locateCenterOnScreen(
            os.path.join(IMAGES_FOLDER, image_name),
            confidence=CONFIDENCE,
            region=SEARCH_REGION
        )
    except Exception as e:
        print(f"Erro ao procurar {image_name}: {e}")
        return None

def main():
    # Exibe alerta e espera que o usuário clique em OK
    pyautogui.alert('Agora o computador está sendo controlado')
    
    # Após fechar o alerta, realiza o alt+tab para mudar a janela
    pyautogui.hotkey('alt', 'tab')
    time.sleep(2)  # Tempo para garantir a mudança de janela

    last_refresh = time.time()

    while True:
        # Verifica se a tecla ESC foi pressionada para interromper a execução
        if keyboard.is_pressed('esc'):
            resposta = pyautogui.confirm("Você deseja parar a execução?", buttons=["Sim", "Não"])
            if resposta == "Sim":
                print("Execução parada pelo usuário.")
                break
        
        # Busca a imagem task.png em tempo real
        target = find_image('task.png')

        if target:
            print("Imagem 'task.png' encontrada! Clicando...")
            pyautogui.click(target)
            time.sleep(3)  # Tempo para o efeito do clique

            # Após o clique, verifica em tempo real se a imagem no_tasks.png desapareceu
            start_check = time.time()
            no_tasks_disappeared = False
            while time.time() - start_check < 5:
                if keyboard.is_pressed('esc'):
                    resposta = pyautogui.confirm("Você deseja parar a execução?", buttons=["Sim", "Não"])
                    if resposta == "Sim":
                        print("Execução parada pelo usuário.")
                        return
                # Se não encontrar no_tasks.png, considera que ela sumiu
                if not find_image('no_tasks.png'):
                    no_tasks_disappeared = True
                    break
                time.sleep(0.5)  # Checa a cada 0.5 segundo

            if no_tasks_disappeared:
                print("A imagem 'no_tasks.png' sumiu. Tocando música...")
                play_music()
                break  # Encerra a execução
            else:
                print("A imagem 'no_tasks.png' ainda está presente. Atualizando página e continuando o ciclo...")
                refresh_page()
                last_refresh = time.time()
                continue  # Retorna ao início do loop para nova verificação

        else:
            # Se 10 segundos se passaram desde a última atualização, atualiza a página
            if time.time() - last_refresh >= REFRESH_INTERVAL:
                print("Nenhuma imagem 'task.png' encontrada. Atualizando página...")
                refresh_page()
                last_refresh = time.time()

        # Pausa breve para evitar sobrecarga da CPU
        time.sleep(0.1)

if __name__ == "__main__":
    main()
