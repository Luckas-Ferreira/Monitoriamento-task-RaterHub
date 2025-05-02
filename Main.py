import pyautogui
import time
import os
import keyboard  # pip install keyboard

# Configurações globais
IMAGES_FOLDER = 'assets'
CONFIDENCE = 0.7  # Ajuste conforme necessário (0.7 pode ser mais confiável)
SEARCH_REGION = (0, 0, 1920, 1080)  # Região da tela para busca (ajuste se necessário)
REFRESH_INTERVAL = 15  # Segundos entre atualizações se nada for encontrado
WAIT_AFTER_CLICK = 4 # Segundos para esperar após clicar em task.png

# --- Funções Auxiliares (mantidas do seu código original) ---

def refresh_page():
    """Atualiza a página pressionando F5 com delay."""
    print("Atualizando a página (F5)...")
    pyautogui.press('f5')
    time.sleep(3)  # Tempo para carregar a página após F5

def play_music():
    """Toca a música de alerta."""
    music_path = os.path.join(IMAGES_FOLDER, 'music.mp3')
    print(f"Tentando tocar a música: {music_path}")
    if os.path.exists(music_path):
        try:
            os.startfile(music_path)
            print("Música iniciada.")
        except Exception as e:
            print(f"Erro ao tocar música: {e}")
    else:
        print(f"Erro: Arquivo de música não encontrado em {music_path}")

def find_image(image_name, confidence_level=CONFIDENCE):
    """Procura a imagem na tela com a confiança especificada."""
    image_path = os.path.join(IMAGES_FOLDER, image_name)
    # print(f"Procurando por {image_path} com confiança {confidence_level}") # Descomente para debug
    if not os.path.exists(image_path):
        print(f"Erro: Arquivo de imagem não encontrado: {image_path}")
        return None
    try:
        location = pyautogui.locateCenterOnScreen(
            image_path,
            confidence=confidence_level,
            region=SEARCH_REGION
        )
        # if location:
        #     print(f"Imagem '{image_name}' encontrada em {location}") # Descomente para debug
        # else:
        #     print(f"Imagem '{image_name}' não encontrada.") # Descomente para debug
        return location
    except Exception as e:
        print(f"Erro durante a busca da imagem {image_name}: {e}")
        return None

# --- Função Principal ---
def main():
    pyautogui.alert('O script de monitoramento vai começar. Pressione ESC a qualquer momento para parar.')

    # Talvez não precise do Alt+Tab se a janela já estiver ativa
    # print("Alternando janela (Alt+Tab)...")
    # pyautogui.hotkey('alt', 'tab')
    # time.sleep(2)

    last_refresh = time.time()
    print("Iniciando monitoramento...")

    while True:
        # --- Verificação da Tecla ESC ---
        if keyboard.is_pressed('esc'):
            try:
                # Use um timeout para evitar bloqueio se o pyautogui tiver problemas
                resposta = pyautogui.confirm("Você deseja parar a execução?", buttons=["Sim", "Não"], timeout=5000) # Timeout de 5 segundos
                if resposta == "Sim" or resposta is None: # Considera timeout como Sim para segurança
                    print("Execução parada pelo usuário.")
                    break
            except pyautogui.TimeoutException:
                print("Confirmação expirou. Parando a execução.")
                break
            except Exception as e:
                 print(f"Erro ao exibir confirmação: {e}. Parando a execução.")
                 break
            # Pequena pausa para evitar múltiplas confirmações se ESC for mantido pressionado
            time.sleep(0.5)
            continue # Volta ao início do loop após tratar ESC

        # --- Lógica Principal ---
        print(f"Procurando por 'task.png'...")
        task_location = find_image('task.png') # Tenta encontrar task.png

        if task_location:
            print(f"Imagem 'task.png' encontrada em {task_location}! Clicando...")
            try:
                pyautogui.click(task_location)
                print(f"Clique realizado. Aguardando {WAIT_AFTER_CLICK} segundos...")
                time.sleep(WAIT_AFTER_CLICK) # Espera os 4 segundos definidos

                print("Verificando se 'no_tasks.png' está presente após o clique...")
                no_task_location = find_image('no_tasks.png') # Verifica se no_tasks.png existe

                if no_task_location:
                    # Se no_tasks.png AINDA existe, significa que a ação não foi concluída como esperado
                    print("'no_tasks.png' ainda está presente. Voltando ao monitoramento...")
                    # Opcional: Forçar refresh aqui pode ajudar em alguns casos
                    # refresh_page()
                    # last_refresh = time.time()
                    continue # Volta para o início do loop while para procurar task.png novamente
                else:
                    # Se no_tasks.png NÃO existe, a tarefa foi processada (ou algo mudou)
                    print("'no_tasks.png' não foi encontrada. Tocando música e encerrando.")
                    play_music()
                    break # Encerra o script conforme solicitado

            except Exception as e:
                print(f"Ocorreu um erro após encontrar e clicar em 'task.png': {e}")
                print("Continuando o monitoramento...")
                # Decide o que fazer em caso de erro, talvez apenas continuar?
                time.sleep(2) # Pausa antes de tentar novamente
                continue

        else:
            # Se task.png NÃO foi encontrada
            print("'task.png' não encontrada.")
            current_time = time.time()
            if current_time - last_refresh >= REFRESH_INTERVAL:
                print("Tempo limite desde a última atualização atingido.")
                refresh_page()
                last_refresh = current_time # Atualiza o tempo da última atualização
            else:
                # Espera um pouco antes da próxima verificação para não sobrecarregar a CPU
                wait_time = 1
                print(f"Aguardando {wait_time} segundo(s) antes da próxima verificação...")
                time.sleep(wait_time)

    print("Script finalizado.")

# --- Execução ---
if __name__ == "__main__":
    # Garante que a pasta 'assets' existe
    if not os.path.exists(IMAGES_FOLDER):
        print(f"ERRO: A pasta '{IMAGES_FOLDER}' não foi encontrada.")
        print("Certifique-se de que a pasta 'assets' existe no mesmo diretório do script e contém as imagens 'task.png', 'no_tasks.png' e 'music.mp3'.")
    else:
        main()