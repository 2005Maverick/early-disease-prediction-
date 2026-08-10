"""Capture dashboard screenshots for the report via headless Edge + Selenium.

Run with the local app up on :8502:
    .venv\\Scripts\\python.exe report\\take_screens.py
"""
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait

OUT = Path(__file__).resolve().parent / 'screens'
OUT.mkdir(exist_ok=True)
BASE = 'http://localhost:8502'

# name -> (url, css selector that proves the page finished rendering)
SHOTS = {
    'intake': (f'{BASE}/', '.edp-intake'),
    'diab_findings': (f'{BASE}/?demo=diabetes', '.edp-finding'),
    'diab_similar': (f'{BASE}/?demo=diabetes&section=similar', '.vega-embed'),
    'diab_whatif': (f'{BASE}/?demo=diabetes&section=whatif', '.vega-embed'),
    'diab_plan': (f'{BASE}/?demo=diabetes&section=plan', '.edp-plan'),
    'model_lab': (f'{BASE}/?demo=diabetes&section=lab', '.vega-embed'),
    'heart_findings': (f'{BASE}/?demo=heart', '.edp-finding'),
}


def main() -> None:
    opts = Options()
    opts.add_argument('--headless=new')
    opts.add_argument('--disable-gpu')
    opts.add_argument('--window-size=1500,1200')
    opts.add_argument('--hide-scrollbars')
    driver = webdriver.Edge(options=opts)
    try:
        for name, (url, selector) in SHOTS.items():
            driver.get(url)
            WebDriverWait(driver, 90).until(
                lambda d: d.find_elements(By.CSS_SELECTOR, selector))
            time.sleep(4)  # let charts finish drawing
            height = driver.execute_script(
                'return Math.min(2600, document.documentElement.scrollHeight)')
            driver.set_window_size(1500, max(900, height))
            time.sleep(1)
            driver.save_screenshot(str(OUT / f'{name}.png'))
            print(f'{name}: ok ({height}px)')
    finally:
        driver.quit()


if __name__ == '__main__':
    main()
