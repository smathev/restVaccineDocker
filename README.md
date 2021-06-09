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

Everything is in a docker image, so simply replace the user in subs/user.json with your relevant users, one entry pr. person and replace text in config.json.

An SMTP server is required to send mail (durh), currently only gmail is supported.

In the config.json file, insert your gmail account mail, and generate a applications specific password here:

https://support.google.com/accounts/answer/185833?p=InvalidSecondFactor&visit_id=637569503595505208-1415581680&rd=1

To run, either use a .yml-composefile:
version: '3.4'
 services:
   restVaccine:
     container_name: restVaccine
     image: smathev/restvaccine:latest
     volumes:
         - /localdir/where/you/store/the/NeededFiles:/config:rw
         
 Or:
docker run -d \
  --name=restVaccine\
  -v /localdir/where/you/store/the/NeededFiles:/config \
  smathev/restvaccine
