## Qlick Monorepo

Qlick: QR menü + sipariş + AI upsell.

Monorepo yapısı:

- apps/
  - web: React + Vite + Tailwind + shadcn/ui
- services/
  - api: FastAPI + SQLAlchemy + Alembic
- packages/
  - ui: Paylaşılan React bileşenleri
  - core: Tipler ve yardımcılar (TS)

Gereksinimler:

- Node.js >= 18, pnpm >= 9
- Python 3.11, pip

Kurulum:

```bash
pnpm i
```

Geliştirme:

```bash
# Web (Vite)
pnpm dev:web

# API (FastAPI)
cd services/api
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Testler:

```bash
pnpm test
cd services/api && pytest
```

Lisans: MIT


