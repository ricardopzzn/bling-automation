import pickle
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# ===== Configuração do Chrome =====
options = Options()
# options.add_argument("--headless")  # NÃO use headless para login manual
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

# ===== Abrir login =====
driver.get("https://www.bling.com.br/login")

# ===== Login manual =====
input("Faça o login MANUALMENTE e pressione ENTER aqui...")

# ===== Salvar cookies =====
with open("cookies.pkl", "wb") as f:
    pickle.dump(driver.get_cookies(), f)

print("Cookies salvos com sucesso ✅")
print("Encerrando navegador")
driver.quit()
