import smtplib
import ssl
from email.mime.text import MIMEText
from os import linesep


def get_message(authorname, content, errors):
    return f"""
Hej,

Mit navn er Bot. Jeg er en automatisk vaccine indmelding apperatus, ekstraordinær!

I min fantalastiske virken, har jeg formået at indsætte dine yderst komplicerede oplysninger ind en utaknemmelig form, ved hjælp af 
en meget hemmelig algorithme som kun min skrivers store hjerne kan læse! (kan ses her: https://i.kym-cdn.com/entries/icons/facebook/000/030/525/cover5.jpg)

og algorithmen kan ses her: https://github.com/asger-weirsoee/rest-vaccine-tilmelder.

I min iver har jeg {"succesfuld" if not errors else "fejlet i at"} oprettet en anmodning om restvaccine i dit navn {":)" if not errors else ":("}

de oplysninger jeg har kunne fremsniffe fra... ja.. altså.. fra de oplysninger du har givet mig, har jeg indsat følgende oplysninger:

{content}

{"Fejlene der er kommet er: " if errors else ""}
{linesep.join(errors)}

Hvis der er nogen oplysninger der er forkert her... SÅ må du meget gerne lige give et kald eller 2 til min kode slave: {authorname}!
eller hvis du er frisk, oprette er træk ønske på FåKnudepunktet 


Vh
Bot

Ps. min kodeslave er single!

    """


def parse_error_msg(all_errors: dict):
    res_str = ""
    for key in all_errors.keys():
        res_str += f"{key}\n"
        for error in all_errors.get(key):
            res_str += f">{error}\n\n"
        res_str += "\n"
    return res_str


def get_adm_message(authorname, all_errors: dict):
    return f"""
Hej {authorname},

Jeg har kørt, og fået samlet nogle informationer sammen til dig :)

der er blevet sendt ({len(all_errors.keys())}) anmodninger.

Med følgende konfigurationer:
{parse_error_msg(all_errors)}


vh 
Bot
    
    """


def send_mail(usr, passwd, msg: MIMEText):
    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls
    sender_email = usr
    password = passwd

    # Create a secure SSL context
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)  # Secure the connection
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.send_message(msg)
