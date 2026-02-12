<div align="center">
  <h1>🤑 Bling Automation</h1>
  <p>
    <strong>Automação para aplicar descontos automáticos em notas fiscais pendentes no Bling</strong><br>
    <em>Economize tempo e evite erros manuais</em>
  </p>

  <img src="https://img.shields.io/badge/Python-3.10+-3775A9?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Selenium-✅-43B02A?style=for-the-badge" alt="Selenium"/>
  <img src="https://img.shields.io/badge/ChromeDriver-Auto-4285F4?style=for-the-badge&logo=googlechrome" alt="ChromeDriver"/>
</div>

<br>

## 📁 Estrutura do Projeto

```text
bling-automation/
│
├── main.py               # Script principal de automação
├── criar_cookie.py       # Cookies salvos do bling com login manual
├── README.md             # Este arquivo que você está lendo 😄
├── requirements.txt      # Lista de dependências
└── screenshots/          # (opcional) Pasta para prints de teste/debug
🛠 Requisitos

Python 3.10 ou superior
Google Chrome instalado e atualizado
Pacotes Python:

textselenium
webdriver-manager
Instalação rápida
Bash# Clone o repositório (ou baixe a pasta)
git clone <url-do-seu-repo>  # opcional

# Entre na pasta do projeto
cd bling-automation
ALERTA: crie um ambiente virtual conforme seu SO.

# Instale as dependências
pip install -r requirements.txt
⚙️ Configuração Inicial (muito importante!)

Cookies (recomendado – evita login toda vez)
Faça login manualmente no Bling no seu navegador
Use um script auxiliar `criar_cookie.py` para salvar os cookies em cookies.pkl

ChromeDriver
→ O webdriver-manager baixa e gerencia automaticamente a versão correta compatível com o seu Chrome.
→ Não precisa baixar nada manualmente.
Modo Headless (Desativado)
Por padrão o navegador abre visível (bom para debug).


🚀 Como Executar
Bashpython main.py
O que o script faz automaticamente:

Abre o Chrome
Carrega cookies salvos (se o arquivo cookies.pkl existir)
Acessa a tela de Notas Fiscais → Pendentes
Filtra apenas status Pendente
Aplica 10% de desconto em todas as notas cujo valor total < R$ 1.000,00
Navega por todas as páginas até processar tudo

📝 Funcionalidades Principais

🏷 Filtragem automática de notas pendentes
💰 Cálculo e aplicação de desconto de 90% (apenas valores < R$1000)
📄 Paginação automática (percorre todas as páginas)
⏳ Esperas inteligentes (espera elementos carregarem antes de interagir)
🍪 Suporte a cookies salvos (login automático)

⚠️ Avisos Importantes

O script depende do layout atual do Bling. Qualquer mudança no site pode quebrar a automação.
Use apenas com sua própria conta e credenciais.
Faça backup ou revise as notas antes de rodar em grande quantidade.
Recomenda-se testar primeiro com poucas notas e em ambiente controlado.
Não sou responsável por bloqueios de conta ou problemas decorrentes do uso.

🔧 Tecnologias Utilizadas

Python 3.10+
Selenium WebDriver
webdriver-manager (gerenciamento automático do ChromeDriver)
Pickle (salvar/carregar cookies)


  

  Feito com 💻 e ☕ por alguém que odeia clicar mil vezes no mesmo lugar
  Boa automação! 🚀

```