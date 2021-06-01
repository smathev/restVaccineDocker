from time import sleep

from webpages_drivers.DriverClass import DriverClass


class Aalborg(DriverClass):
    def __init__(self, driver, args):
        super().__init__(driver, args)
        self.required['age'] = 'text din alder i tal'

    def _go_to_page(self):
        self.driver.get('https://rn.dk/sundhed/patient-i-region-nordjylland/coronavirus/covid-vaccination/restvacciner')
        sleep(5)
        accept_cookies = self.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[4]/div[2]/div/button')
        accept_cookies.click()
        sleep(1)
        drop_down_click = self.driver.find_element_by_xpath(
            '/html/body/form/div[4]/div[1]/div/div/div/div/div[3]/div[2]/div/div[1]/div/div[1]/div[4]/div/div/div/ul/li[3]/h3/a')
        drop_down_click.click()
        sleep(1)
        navigate_to_page = self.driver.find_element_by_xpath(
            '/html/body/form/div[4]/div[1]/div/div/div/div/div[3]/div[2]/div/div[1]/div/div[1]/div[4]/div/div/div/ul/li[3]/div/div/div/div/div/div/div/div/div/p[4]/a')
        navigate_to_page.click()

    def _fill_out_form(self, **kwargs):
        already_vaccinated = self.driver.find_element_by_xpath(
            '/html/body/div/form/div[1]/div[2]/table/tbody/tr[2]/td/div/span[2]/label')
        already_vaccinated.click()
        name_field = self.driver.find_element_by_xpath('//*[@id="t337561910"]')
        name_field.send_keys(kwargs['name'])
        age_field = self.driver.find_element_by_xpath('//*[@id="n337561915"]')
        age_field.send_keys(kwargs['age'])
        phone_filed = self.driver.find_element_by_xpath('//*[@id="t337561922"]')
        phone_filed.send_keys(kwargs['phone'])
        sleep(1)
        sleep(1)
        vaccination_place = self.driver.find_element_by_xpath(
            f'/html/body/div/form/div[1]/div[6]/table/tbody/tr[2]/td/div/span[{kwargs["num_on_list"] + 1}]/label')
        vaccination_place.click()
        sleep(2)
        if not self.args.dummy_run:
            next_button = self.driver.find_element_by_xpath('/html/body/div/form/div[2]/div[3]/input')
            next_button.click()
            self._screenshot(kwargs['image_location'], kwargs['name'])
            sleep(5)
            close_button = self.driver.find_element_by_xpath('/html/body/div/form/div[2]/div[3]/input')
            close_button.click()

    @staticmethod
    def get_info(**kwargs):
        return f"""
allerede vaccineret: nej
navn: {kwargs['name']}
alder: {kwargs['age']}
telefon: {kwargs['phone']}
vaccinerings sted: 
 - {kwargs['big_place']}.
    - {kwargs['place_name']}


"""