import os
try:
    from dotenv import load_dotenv
    load_dotenv()  # optional: QA_* variables from an untracked .env file
except ImportError:
    pass
from playwright.sync_api import Playwright, sync_playwright, expect, Page
import pytest

def test_01_LogIn(page: Page):
    page.set_viewport_size({"width": 1920, "height": 1080})
    page.goto("https://es.arodriguezf.com/home")
    page.get_by_role("button", name="Cerrar").click()
    page.get_by_role("button", name="Iniciar sesión").click()
    page.get_by_placeholder("Tu correo").click()
    page.get_by_placeholder("Tu correo").fill(os.environ["QA_EMAIL"])
    page.get_by_placeholder("Contraseña").click()
    page.get_by_placeholder("Contraseña").fill(os.environ["QA_UI_PASSWORD"])
    page.get_by_role("button", name="Iniciar sesión").click()


def test_02_ReviewClient(page: Page):
    page.get_by_role("button", name="Panel").click()
    page.get_by_role("button", name="Acciones").hover()
    page.pause()

