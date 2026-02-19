import pickle
import os
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager



options = Options()
# options.add_argument("--headless")  # DESATIVADO
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

driver.get("https://www.bling.com.br")
sleep(3)

if os.path.exists("cookies.pkl") and os.path.getsize("cookies.pkl") > 0:
    with open("cookies.pkl", "rb") as f:
        cookies = pickle.load(f)

    for cookie in cookies:
        cookie.pop("sameSite", None)
        driver.add_cookie(cookie)
    print("[+] - Cookies carregados com SUCESSO.")
else:
    print("\033[31m[+] - Cookies não encontrados\033[0m")


driver.get("https://www.bling.com.br/notas.fiscais.php#list")
wait = WebDriverWait(driver, 15)
sleep(15)


# Clicando no campo do filtro
botao = driver.find_element(By.ID, "link-pesquisa")
driver.execute_script("arguments[0].scrollIntoView(true);", botao)
driver.execute_script("arguments[0].click();", botao)
sleep(2)

# Selecionando o dropdown (Opção do filtro)
dropdown = wait.until(
    EC.presence_of_element_located(
        (By.CLASS_NAME, "InputDropdown-select")
    )
)

driver.execute_script(
    "arguments[0].scrollIntoView({block: 'center'});",
    dropdown
)

# Selecionando a opção Pendentes e Clicando 
driver.execute_script("arguments[0].focus();", dropdown)
driver.execute_script("arguments[0].click();", dropdown)

opcao_pendentes = wait.until(
    EC.presence_of_element_located(
        (
            By.XPATH,
            "//li[contains(@class,'Dropdown-item') and normalize-space()='Pendentes']"
        )
    )
)
sleep(0.5)
driver.execute_script("arguments[0].click();", opcao_pendentes)
sleep(2)

# Clicar no botão filtrar
botao_filtrar = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//div[@id='filter-button-area']//button[text()='Filtrar']"))
)
sleep(0.5)
botao_filtrar.click()



# --- LOOP PRINCIPAL DE PÁGINA ---
# --- LOOP PRINCIPAL ---
# Começamos em 0 para pegar o primeiro item da lista filtrada
indice = 0 

while True:
    # 1. Aguarda o carregamento sumir
    wait.until(EC.invisibility_of_element_located((By.ID, "modalWait")))
    sleep(2) 

    # 2. Recaptura apenas as linhas que possuem o status Pendente
    # Isso evita percorrer as 24 linhas vazias que você viu no log
    linhas = driver.find_elements(By.XPATH, "//tr[.//span[contains(.,'Pendente')]]")

    # Verifica se o índice ainda é válido
    if indice >= len(linhas):
        print("Todos os itens pendentes desta página foram processados.")
        # Lógica de próxima página
        try:
            botao_proximo = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//span[contains(text(),'Próxima') or contains(@class,'fa-angle-right')]")
                )
            )
            print("Indo para a próxima página...")
            botao_proximo.click()
            sleep(3)
            indice = 0
        except Exception:
            print("[+] - Última página alcançada, encerrado.")
            break
        
        continue
        
    linha = linhas[indice]    
    
    try:
        # 3. Localiza o badge dentro da linha capturada
        pendente = linha.find_elements(By.XPATH, ".//span[contains(.,'Pendente')]")

        if not pendente:
            indice += 1
            continue

        # 4. AÇÃO DE CLIQUE
        elemento = pendente[0]
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elemento)
        sleep(0.5)
        elemento.click()
        print(f"Processando item pendente: {indice}")

        # 5. ESPERA A TELA DE EDIÇÃO ABRIR
        wait.until(EC.invisibility_of_element_located((By.ID, "modalWait")))
        
        # --- INÍCIO DO SEU BLOCO DE VALOR (MANTIDO IGUAL) ---
        input_valor = wait.until(EC.presence_of_element_located((By.ID, "valorProdutos")))
        valor_str = input_valor.get_attribute("value")
        
        if valor_str:
            valor_float = float(valor_str.replace(".", "").replace(",", "."))
            if valor_float < 1000.00:
                desconto = valor_float * 0.9
                input_desconto = wait.until(EC.presence_of_element_located((By.ID, "desconto")))
                
                # Limpando o campo
                for _ in range(10):
                    input_desconto.send_keys(Keys.BACKSPACE)
                
                sleep(1)
                input_desconto.send_keys(f"{desconto:.2f}".replace(".", ","))
                driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", input_desconto)
                sleep(2)

        # 6. SALVAR
        save_button = wait.until(EC.element_to_be_clickable((By.ID, "botaoSalvar")))
        driver.execute_script("arguments[0].click();", save_button)
        
        # 7. ESPERA FINALIZAÇÃO DO SALVAMENTO
        wait.until(EC.invisibility_of_element_located((By.ID, "modalWait")))
        print(f"Item {indice} salvo com sucesso.")
        
        # SÓ INCREMENTA O ÍNDICE AQUI (após salvar com sucesso)
        indice += 1
        sleep(2) # Pausa para o sistema não repetir o clique no mesmo item

    except Exception as e:
        print(f"Erro ao processar o índice {indice}: {e}")
        indice += 1 # Pula se der erro para não travar o bot
        continue
    
driver.quit()
