from abc import ABC
from pathlib import Path
from time import sleep

from selenium.webdriver.firefox.webdriver import WebDriver


class DriverClass(ABC):
    location = ''
    required = None

    def __init__(self, driver, args):
        self.driver: WebDriver = driver
        self.args = args
        self.required = {
            'name': 'tekst dit fulde navn',
            'phone': 'tekst dit telefonnr',
            'email': 'tekst din email addresse',
            'num_on_list': '0 indekseret af listen over vaccinatiaons steder',
            'big_place': 'string needs to be one of the supported regions.',
        }

    def run(self, **kwargs):
        self._go_to_page()
        sleep(10)
        self._fill_out_form(**kwargs)

    def _screenshot(self, path, name: str):
        screen_shot_location = Path(path).joinpath(
            name.replace(' ', '')
            .replace('æ', 'ae')
            .replace('Æ', 'Ae')
            .replace('ø', 'oe')
            .replace('Ø', 'Oe')
            .replace('å', 'aa')
            .replace('Å', 'Aa')
            + '.png').__str__()
        self.driver.save_screenshot(screen_shot_location)

    def _go_to_page(self):
        raise NotImplementedError("Must override method")

    def _fill_out_form(self, **kwargs):
        raise NotImplementedError("Must override method")

    def validate(self, **kwargs):
        errors = []
        for v in self.required.keys():
            if v not in kwargs.keys():
                errors.append(f'{v} is required')
        return errors
    @staticmethod
    def get_info(**kwargs):
        raise NotImplementedError("Must override method")
