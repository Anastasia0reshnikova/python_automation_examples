"""

Архитектура автотестов — минимальный, но «чистый» каркас

src/
  contracts/      # интерфейсы (по желанию)
  api/            # httpx клиент(ы)
  ui/             # Page Objects
tests/
  api/            # API тесты
  ui/             # UI тесты
  conftest.py     # фикстуры: base_url, driver, api, creds
"""