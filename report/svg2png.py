"""Rasterize the architecture SVGs to PNG for the slide deck.

Uses Selenium ELEMENT screenshots (exact crop to the rendered <img>), so
window chrome and display scaling can never clip the bottom of a diagram.
"""
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options

FIGS = Path(__file__).resolve().parent / 'figures'
# name -> aspect (view box w/h); rendered at 1800 px wide
SVGS = {'arch_system': 900 / 470, 'arch_ensemble': 900 / 258,
        'arch_registry': 900 / 330, 'arch_serving': 900 / 300}
WIDTH = 1800


def main() -> None:
    opts = Options()
    opts.add_argument('--headless=new')
    opts.add_argument('--hide-scrollbars')
    opts.add_argument('--force-device-scale-factor=1')
    driver = webdriver.Edge(options=opts)
    try:
        for name, aspect in SVGS.items():
            content_h = int(WIDTH / aspect)
            wrapper = FIGS / f'_tmp_{name}.html'
            wrapper.write_text(
                '<body style="margin:0;background:white">'
                f'<img id="d" src="{name}.svg" style="display:block;'
                f'width:{WIDTH}px"></body>')
            driver.set_window_size(WIDTH + 60, content_h + 400)  # generous slack
            driver.get(wrapper.resolve().as_uri())
            time.sleep(1)
            img = driver.find_element(By.ID, 'd')
            img.screenshot(str(FIGS / f'{name}.png'))
            wrapper.unlink()
            print(name, 'ok', img.size)
    finally:
        driver.quit()


if __name__ == '__main__':
    main()
