# Shopwise Demo Store

A very small Flask application used as the **local target** of the Selenium and Playwright reference frameworks. It has a login with validation messages, a product list with sorting, a cart, a checkout form and a JSON endpoint (`/api/products`).

Why a local app instead of a public demo site: the suites become deterministic, run offline and free in CI, and keep working when a third-party site changes.

```bash
pip install flask
python demo-app/app.py --port 5000
```

`DEMO_USER` and `DEMO_PASSWORD` set the valid login (fixture defaults for this local app only). The user `locked.user` is always rejected as locked. Every element exposes a `data-testid` so tests do not depend on layout or XPath.

