import argparse
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from time import sleep
from typing import Callable

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager

from mail import get_message, send_mail, get_adm_message
from webpages_drivers.DriverClass import DriverClass
from webpages_drivers.aalborg import Aalborg
from webpages_drivers.aarhus import Aarhus

root = Path(__file__).parent
with open(root.joinpath('config.json'), 'r+') as f:
    config = json.load(f)

locatiaon = {
    'aalborg': Aalborg,
    'aarhus': Aarhus
}

hard_coded_location_names = {
    'aalborg': [
        'Aars, Messevej 1, 9600 Aars (Messecenter Vesthimmerland)',
        'Aalborg, Håndværkervej 24C, 9000 Aalborg',
        'Brovst. Damengvej 2, 9460 Brovst',
        'Brønderslev. Knudsgade 15, 9700 Brønderslev',
        'Frederikshavn, Harald Nielsens Plads 9, 9900 Frederikshavn (Arena Nord)',
        'Hobro, Amerikavej 22, 9500 Hobro (Hobro Idrætscenter)',
        'Hjørring, Fuglsigvej 23, 9800 Hjørring (Bagterphallen)',
        'Nykøbing Mors. Nygade 29, 7900 Nykøbing Mors',
        'Thisted, Munkevej 9E, 7700 Thisted (Munkehallen)',
        'Skørping, Himmerlandsgade 59, 9520 Skørping',
    ],
    'aarhus': [
        'Vaccination Aarhus NORD, Paludan-Müllers Vej 110, 8200 Aarhus N',
        'Vaccination Aarhus SYD, Sletvej 30, 8310 Tranbjerg J',
        'Vaccination Aarhus Ø, Hveens gade 4, 8000 Aarhus C',
        'Vaccination Skanderborg, Festsalen Sølund, Sølundsvej 3, 8660 Skanderborg',
        'Vaccination Samsø, SamBiosen, Pillemarksvej 1, 8305 Samsø ',
    ]

}


class RestVacBot:

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        options = Options()
        options.headless = True
        self.driver = webdriver.Firefox(
            executable_path=GeckoDriverManager(
                log_level=50,
                print_first_line=False).install(),
            options=options)

    def run(self, klass: Callable[[webdriver.Firefox, any], DriverClass], args):
        b = klass(self.driver, args)
        errors = b.validate(**self.kwargs)

        if errors:
            return errors
        b.run(**self.kwargs)
        return errors

    def close(self):
        self.driver.quit()


def send_mail_to_config(recepient, content, errors, args):
    message = MIMEMultipart()
    text_type = 'plain'
    txt = get_message(config['author']['name'], content, errors)
    msg = MIMEText(txt, text_type, 'utf-8')
    msg['Subject'] = f'{"!!!FEJL!!!!" if errors else "SUCCESS"}: anmodning om restvaccine'
    msg['From'] = config['email']['username']
    msg['To'] = recepient
    message.attach(msg)

    if args.dummy_run:
        root.joinpath('dummydata').mkdir(exist_ok=True)
        root.joinpath('dummydata').joinpath(f'{recepient}.txt').write_text(txt)
    else:
        send_mail(config['email']['username'], config['email']['password'], msg)


def send_admin_mail(all_errors: dict):
    text_type = 'plain'
    txt = get_adm_message(config['author']['name'], all_errors)
    msg = MIMEText(txt, text_type, 'utf-8')
    msg['Subject'] = f'Admin message'
    msg['From'] = config['email']['username']
    msg['To'] = config['author']['email']
    send_mail(config['email']['username'], config['email']['password'], msg)


def full_stack():
    import traceback, sys
    exc = sys.exc_info()[0]
    if exc is not None:
        f = sys.exc_info()[-1].tb_frame.f_back
        stack = traceback.extract_stack(f)
    else:
        stack = traceback.extract_stack()[:-1]  # last one would be full_stack()
    trc = 'Traceback (most recent call last):\n'
    stackstr = trc + ''.join(traceback.format_list(stack))
    if exc is not None:
        stackstr += '  ' + traceback.format_exc().lstrip(trc)
    return stackstr


def do_the_config(config_path: Path, args):
    all_errors = []
    with open(config_path, 'r+') as f:
        obj = json.load(f)
        obj['image_location'] = root.joinpath('images')
        with Display() as display:
            runner = RestVacBot(**obj)
            method = locatiaon.get(obj['big_place'])
            try:
                all_errors = runner.run(method, args)
                sleep(3)
            except Exception as e:
                all_errors.append(full_stack())
                runner.close()
            finally:
                runner.close()
        obj['place_name'] = hard_coded_location_names[obj['big_place']][obj['num_on_list']]

        send_mail_to_config(obj['email'], method(None, args).get_info(**obj), all_errors, args)
    return all_errors


def main(args):
    all_errors = dict()
    if args.get_json_formats:
        print("The formatted JSON file that should be output,\n"
              "looks like this:")
        for x in locatiaon.values():
            json_formatted = json.dumps(x(None, args).required, indent=4)
            print(x.__name__ + ":")
            print(json_formatted)
        exit()

    if args.all:
        for file in args.config_folder.glob('subs/*'):
            if args.list_configs:
                print(file.name)
            if file.name.endswith('.json') and (args.ignore is None or file not in [Path(x) for x in args.ignore]):
                all_errors[file.name] = do_the_config(file, args)

    else:
        for file in args.config:
            if args.list_configs:
                print(file.name)
            if not file.name.endswith('.json'):
                all_errors[file.name] = ['Wrong file type']
            else:
                all_errors[file.name] = do_the_config(file, args)
    send_admin_mail(all_errors)


if __name__ == '__main__':
    args = argparse.ArgumentParser('Rest-Vac bot, automatically submits applications for leftover vacinations')

    args.add_argument('--config-folder', default=root, help='The folder that the configurations are stored ')

    args.add_argument('--ignore', nargs='+',
                      help="if --all is set, this ignores the configurations with the path here")

    debug_options = args.add_argument_group(title="debug options")
    debug_options.add_argument('--list-configs', action='store_true',
                               help="Prints all configurations as they are loaded")
    debug_options.add_argument('--dummy-run', action='store_true',
                               help="Creates a run, that pretends to do everything, but does not send mail or sign up"
                                    "to leftover vaccinations")

    mutually_exclusive = args.add_mutually_exclusive_group(required=True)
    mutually_exclusive.add_argument('--get-json-formats', action='store_true',
                                    help='Displays the JSON format that is required for each of the configurations')
    mutually_exclusive.add_argument('-a', '--all', action='store_true',
                                    help='Runs all configurations that can be found')
    mutually_exclusive.add_argument('-c', '--config', nargs='+',
                                    help='give the paths of the configurations that should be run now')

    main(args.parse_args())
