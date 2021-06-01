# Automatic subscription to leftover vaccinations in northen jutland
For each config in subs makes a subscription for leftover vaccinations.

## subs 
```json
The formatted JSON file that should be output,
looks like this:
Aalborg:
{
    "name": "tekst dit fulde navn",
    "phone": "tekst dit telefonnr",
    "email": "tekst din email addresse",
    "num_on_list": "0 indekseret af listen over vaccinatiaons steder",
    "big_place": "aalborg",
    "age": "text din alder i tal"
}
Aarhus:
{
    "name": "tekst dit fulde navn",
    "phone": "tekst dit telefonnr",
    "email": "tekst din email addresse",
    "num_on_list": "0 indekseret af listen over vaccinatiaons steder",
    "big_place": "aarhus",
    "age": "text din alder i tal",
    "date_of_birth": "text dd/mm/yyyy din f\u00f8dselsdato"
}
```

Then we headless emulate the clicks required to fill out the form for subscribing to leftover vaccinations.

And after this have completed, then sends a mail to the person, that we've successfully subscribed them for the leftover vaccinations

## mail
An SMTP server is required to send mail (durh), currently only gmail is supported.

In the config.json file, insert your gmail account mail, and generate a applications specific password here:

https://support.google.com/accounts/answer/185833?p=InvalidSecondFactor&visit_id=637569503595505208-1415581680&rd=1

## Requirements
Besides the python pacakages listed in requirements.txt, the we also need xvfe to emulate a xorg server in a headless env.
(essentially so that it can be ran on a server without X installed)

debian:

`apt install xvfe`

arch:

`pacman -S xorg-server-xvfb`


## Usage
As this is a selfcontained script, all you have to do to run it.
A good way of having this running every day is to use a CRON job, or equivalent.

a jobber job could look like
```
RestVaccineScript:
     cmd: /path/to/rest-vac/venv/bin/python /path/to/rest-vac/main.py
     time: '0 0 8 * * *'
     onError: Backoff
```

A cron job could look like:
```
0 8 * * * /path/to/rest-vac/venv/bin/python /path/to/rest-vac/main.py
```


