"""Rasterize the architecture SVGs to PNG for the slide deck."""
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.edge.options import Options

FIGS = Path(__file__).resolve().parent / 'figures'
SVGS = {'arch_system': (1800, 960), 'arch_ensemble': (1800, 730),
        'arch_registry': (1800, 670), 'arch_serving': (1800, 610)}


def main() -> None:
    opts = Options()
    opts.add_argument('--headless=new')
    opts.add_argument('--hide-scrollbars')
    driver = webdriver.Edge(options=opts)
    try:
        for name, (w, h) in SVGS.items():
            wrapper = FIGS / f'_tmp_{name}.html'
            wrapper.write_text(
                '<body style="margin:0;background:white">'
                f'<img src="{name}.svg" style="width:100%"></body>')
            driver.set_window_size(w, h)
            driver.get(wrapper.resolve().as_uri())
            time.sleep(1)
            driver.save_screenshot(str(FIGS / f'{name}.png'))
            wrapper.unlink()
            print(name, 'ok')
    finally:
        driver.quit()


if __name__ == '__main__':
    main()
