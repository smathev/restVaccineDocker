from time import sleep

from webpages_drivers.DriverClass import DriverClass


class Aarhus(DriverClass):
    def __init__(self, driver, args):
        super().__init__(driver, args)
        self.required['date_of_birth'] = 'text dd/mm/yyyy din fødselsdato'

    def _go_to_page(self):
        self.driver.get('https://www.auh.dk/om-auh/tilbud-om-covid-vaccination-ved-brug-af-restvacciner/')
        sleep(5)
        accept_cookies = self.driver.find_element_by_xpath('//*[@id="CybotCookiebotDialogBodyButtonAccept"]')
        accept_cookies.click()

    def _fill_out_form(self, **kwargs):
        name_field = self.driver.find_element_by_xpath('//*[@id="06ea46a4-9fe2-49c0-b3fa-9217ab3e3c0e"]')
        name_field.send_keys(kwargs['name'])
        date_of_birth_field = self.driver.find_element_by_xpath('// *[ @ id = "56930c3b-65ef-4e63-bb15-27a36a4256b8"]')
        date_of_birth_field.send_keys(kwargs['date_of_birth'])
        email_field = self.driver.find_element_by_xpath('//*[@id="db67108b-6627-43d7-982e-2b11c6b5b26e"]')
        email_field.send_keys(kwargs['email'])
        phone_field = self.driver.find_element_by_xpath('//*[@id="41df7f89-d7b9-4203-b18a-8f4c86023f89"]')
        phone_field.send_keys(kwargs['phone'])
        vac_field = self.driver.find_element_by_xpath(
            f'/html/body/div[2]/div/div[2]/div/main/div[2]/div[3]/div/div/div/div/div/div/form/div[2]/section/div[5]/fieldset/label[{kwargs["num_on_list"] + 1}]')
        vac_field.click()

        sleep(1)
        if not self.args.dummy_run:
            submit_button = self.driver.find_element_by_xpath('//*[@id="58efbdd7-1555-4202-aec4-30c5745c4797"]')
            submit_button.click()
        self._screenshot(kwargs['image_location'], kwargs['name'])

    @staticmethod
    def get_info(**kwargs):
        return f"""
allerede vaccineret: nej
navn: {kwargs['name']}
alder: {kwargs['date_of_birth']}
telefon: {kwargs['phone']}
vaccinerings sted: 
 - {kwargs['big_place']}.
    - {kwargs['place_name']}
        
        
"""