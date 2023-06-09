from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import openai
import time

# Configurar a chave da API do OpenAI
openai.api_key = 'SUA CHAVE DA openAI'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')

executable_path = '/usr/local/bin/chromedriver'

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://kahoot.it/")  # Abrir o link do jogo Kahoot

codigo_input = driver.find_element(By.XPATH, "/html/body/div/div[1]/div/div/div/div[3]/div[2]/main/div/form/input") # Localizar o campo de input para o código
codigo_input.send_keys("4229180") # Preencher o código no campo
codigo_input.submit() # Enviar o código para entrar no jogo

time.sleep(2)

codigo_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "/html/body/div/div[1]/div/div/div/div[3]/div[2]/main/div/form/input"))
)
codigo_input.send_keys("OTACÍLIO PROGRAMADOR") # Preencher o NOME no campo
codigo_input.submit() # Enviar o NOME para entrar no jogo

# Variável para armazenar a pergunta anterior
texto_pergunta_anterior = ""

while True:
    try:
        # Aguardar até que a pergunta seja carregada
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[@data-functional-selector='block-title']")))

        # Localizar a pergunta
        pergunta = driver.find_element(By.XPATH, "//span[@data-functional-selector='block-title']")
        texto_pergunta = pergunta.text

        # Verificar se a pergunta mudou
        if texto_pergunta != texto_pergunta_anterior:
            print("Nova pergunta encontrada:", texto_pergunta)

            # Localizar os elementos que contêm as alternativas
            elementos_alternativas = driver.find_elements(By.XPATH, "//span[contains(@data-functional-selector, 'question-choice-text-')]")

            # Lista para armazenar as alternativas
            texto_alternativas = []

            for elemento in elementos_alternativas:
                # Extrair o texto da alternativa
                texto_alternativa = elemento.text.strip()
                # Adicionar o texto da alternativa à lista
                texto_alternativas.append(texto_alternativa)

            # Imprimir as alternativas
            print("Alternativas:")
            for alternativa in texto_alternativas:
                print(alternativa)

            # Construir a mensagem para enviar ao modelo de bate-papo
            messages = [
                {"role": "system", "content": "Você é uma IA que responde perguntas."},
                {"role": "user", "content": f"{texto_pergunta} (chatgpt, escolha uma das alternativas corretas sem dar explicação, seja direto, pois preciso responder em menos de 18seg!)"},
            ]

            # Adicionar as alternativas à mensagem
            for alternativa in texto_alternativas:
                messages.append({"role": "user", "content": alternativa})

            # Enviar a mensagem para o modelo ChatGPT
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=50,
                n=1,
                stop=None,
                temperature=0.7,
                timeout=15,
            )

            # Extrair a resposta gerada pelo modelo
            texto_resposta = response.choices[0].message.content.strip()
            print("Resposta:", texto_resposta)

            # Atualizar a pergunta anterior
            texto_pergunta_anterior = texto_pergunta

    except (NoSuchElementException, TimeoutException):
        print("A pergunta não foi encontrada")

    # Aguardar um tempo antes de verificar novamente
    time.sleep(2)
