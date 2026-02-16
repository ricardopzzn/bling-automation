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


actions = ActionChains(driver)

# --- LOOP PRINCIPAL DE PÁGINA ---
while True:
    wait.until(EC.invisibility_of_element_located((By.ID, "modalWait")))

    # Resetar índice para a nova página
    indice = 0
    linhas = driver.find_elements(By.XPATH, "//table/tbody/tr")

    # Loop para percorrer todas as linhas da página
    while indice < len(linhas):
        linha = linhas[indice]

        try:
            # verifica se contém "Pendente"
            if "Pendente" not in linha.text:
                indice += 1
                continue

            # scroll até a linha
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", linha)

            # clique manual real
            actions.move_to_element(linha).pause(0.3).click().perform()
            print(f"[+] Clique manual índice {indice}")

            # espera abrir a nota
            wait.until(EC.presence_of_element_located((By.ID, "valorProdutos")))

            # Input do valor
            input_valor = wait.until(EC.presence_of_element_located((By.ID, "valorProdutos")))
            valor_str = input_valor.get_attribute("value")
            if valor_str:
                valor_float = float(valor_str.replace(".", "").replace(",", "."))
                if valor_float < 1000.00:
                    desconto = valor_float * 0.9
                    input_desconto = wait.until(EC.presence_of_element_located((By.ID, "desconto")))
                    for _ in range(10):
                        sleep(0.5)
                        input_desconto.send_keys(Keys.BACKSPACE)
                    sleep(2)
                    input_desconto.send_keys(f"{desconto:.2f}".replace(".", ","))
                    driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", input_desconto)
                    sleep(2)

            # Salvar
            save_button = wait.until(EC.element_to_be_clickable((By.ID, "botaoSalvar")))
            driver.execute_script("arguments[0].click();", save_button)
            sleep(0.5)
            indice += 1

        except Exception as e:
            print(f"[!] Erro no índice {indice}:", e)
            indice += 1

    # --- Depois de processar todas as linhas da página, tenta ir para a próxima ---
    try:
        botao_proximo = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//span[contains(text(),'Próxima') or contains(@class,'fa-angle-right')]")
            )
        )
        sleep(0.3)
        botao_proximo.click()
        sleep(3)

    except Exception:
        print("[+] - Última página alcançada, encerrado.")
        break

driver.quit()
     
