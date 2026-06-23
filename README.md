# Klima

## Overview

Klima is an IoT solution developed for the IEEE SSCS Arduino Contest. It transforms conventional air conditioners into smart, connected devices through a combination of microcontrollers and environmental sensors, including temperature, humidity, and motion detection. The system is complemented by a Progressive Web Application (PWA) that enables remote control, automated climate management, energy consumption monitoring, and cost analysis, providing users with greater comfort, efficiency, and sustainability.

---

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Mulekotd/klima-iot.git
cd klima-iot
```

---

## Estrutura do Projeto

O projeto é organizado em duas aplicações principais:

- `frontend/`: aplicação web desenvolvida com Next.js.
- `api/`: API backend desenvolvida com FastAPI.

### Frontend: Next.js

```text
frontend/
├── app/                    # Rotas, layouts e segmentos do App Router do Next.js
│   ├── control/            # Tela de controle remoto do ar-condicionado
│   ├── dashboard/          # Painel de monitoramento e visão geral do clima
│   ├── login/              # Página de login
│   ├── register/           # Página de cadastro
│   ├── globals.css         # Estilos globais
│   ├── layout.tsx          # Layout raiz da aplicação
│   ├── manifest.ts         # Configuração do manifesto PWA
│   └── page.tsx            # Rota inicial da aplicação
├── components/             # Componentes reutilizáveis de interface e funcionalidades
├── hooks/                  # Hooks customizados do React
├── public/                 # Arquivos estáticos servidos pelo Next.js
├── state/                  # Estado compartilhado no cliente
├── next.config.ts          # Configurações do Next.js
├── package.json            # Dependências e scripts do frontend
├── tsconfig.json           # Configurações do TypeScript
└── yarn.lock               # Versões travadas das dependências do frontend
```

### Backend: FastAPI

O backend segue uma estrutura em camadas para separar configuração, persistência,
validação, roteamento e regras de negócio:

```text
api/
├── app/
│   ├── core/               # Configurações globais, segurança e banco de dados
│   ├── models/             # Modelos do banco de dados, como SQLAlchemy
│   ├── schemas/            # Modelos Pydantic para validação de entrada e saída
│   ├── routes/             # Camada de roteamento e endpoints da API
│   ├── services/           # Regras de negócio e lógica de processamento
│   └── main.py             # Ponto de entrada da aplicação
├── tests/                  # Testes automatizados
├── pyproject.toml          # Dependências e metadados do projeto
└── uv.lock                 # Versões travadas das dependências do backend
```

## Contributors

<a href="https://github.com/Mulekotd/klima-iot/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Mulekotd/klima-iot" />
</a>
