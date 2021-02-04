import re

lista = re.findall(r'\d+', 'RE: :  3338888 Incorporar  campo  "Destino Mercancía" en PAS/SAP')

print(lista)

for i in lista:
    if (len(str(i))) == 7:
       ticket = i
       break
    else:
        ticket = 99

if not lista:
    print("no hay numeros")

else: 

    if ticket == 99:
        print("no hay numero de 7 digitos")
    else:
        print("el ticket debe ser", ticket)


