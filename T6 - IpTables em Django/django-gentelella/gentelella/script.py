import sys
import re
import operator
import socket

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

import json

arquivo = sys.argv[1]

# Exercicio 1

def numero_pacotes():
    with open(arquivo) as f:
        return len(f.readlines())

total_pacotes = numero_pacotes()
print('Numero Total de Pacotes:', total_pacotes)

print()

# -----------------------------------------------------------

# Exercicio 2

def pegar_ips(lista_ips, string):
    with open(arquivo) as f:
        for line in f:
            expr_reg = re.escape(string) + r"=(.*?)[\s]"
            match = re.search(expr_reg, line)
            if match is not None:
                ip = match.group(1)
                lista_ips.append(ip)
        return lista_ips

lista_ips_src = pegar_ips([], 'SRC')

def contar_ips(lista_ips, dic_ips):     # conta quantas vezes a ip aparece e coloca num dicionario
    for x in lista_ips:
        if x not in dic_ips:
            dic_ips[str(x)] = lista_ips.count(x)
    return dic_ips

dic_ips_src = contar_ips(lista_ips_src, {})

lista_src_ordenada = sorted(dic_ips_src.items(), key=operator.itemgetter(1),reverse=True)

top10_src = lista_src_ordenada[:10]

print("Top 10 IPs fonte, quantos pacotes cada um e cidade/país de cada um:")

def adicionar_top10_na_lista(top10):
    lista = []
    for tupla in top10:
        url = ("http://ipvigilante.com/" + tupla[0] + "/full")
        response = urlopen(url)
        data = response.read().decode("utf-8")
        data = json.loads(data)

        lista.append((tupla[0], tupla[1], data["data"]["country_name"]))

    return lista

lista_tuplas_src = adicionar_top10_na_lista(top10_src)

for x in lista_tuplas_src:
    print(x)

print()

#-------------------------------------------------------

# Exercicio 5

lista_ips_dpt = pegar_ips([], 'DPT')

dic_ips_dpt = contar_ips(lista_ips_dpt, {})

lista_dpt_ordenada = sorted(dic_ips_dpt.items(), key=operator.itemgetter(1),reverse=True)

top10_dpt = lista_dpt_ordenada[:10]

print("Top 10 portas usadas (nome, número da porta e quantidade):")

lista_tuplas_dpt = []

for tupla in top10_dpt:
    lista_tuplas_dpt.append((socket.getservbyport(int(tupla[0])), tupla[0], tupla[1]))

for x in lista_tuplas_dpt:
    print(x)

# ---------------------------------------------------------------------------
# Popular o banco com os dados do iptables

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gentelella.settings")

import django
django.setup()

from app.models import IpsFonte
from app.models import IpTables
from app.models import Portas

if __name__ == '__main__':
    # Adicionar no banco o total de pacotes do arquivo iptablesyslog
    iptables = IpTables()
    iptables.ident = 1
    iptables.total_pacotes = total_pacotes
    iptables.save()

    print('IpTables:', IpTables.objects.all())

    print()

    aux = 1

    # Adicionar IPs fonte no banco
    for x in lista_tuplas_src:
        ip = IpsFonte()
        ip.ident = aux
        ip.endereco_ip = x[0]
        ip.numero_pacotes = x[1]
        ip.pais = x[2]
        ip.save()
        aux += 1

    ips = IpsFonte.objects.all()
    print('Lista de Ips Fonte:', ips)

    for x in ips:
        print(x.ident)
        print(x.endereco_ip)
        print(x.numero_pacotes)
        print(x.pais)
        print()

    aux = 1
    # Adicionar portas no banco
    for x in lista_tuplas_dpt:
        porta = Portas()
        porta.ident = aux
        porta.nome = x[0]
        porta.numero_porta = x[1]
        porta.quantidade = x[2]
        porta.save()
        aux += 1

    portas = Portas.objects.all()
    print('Lista de Portas:', portas)

    for x in portas:
        print(x.ident)
        print(x.nome)
        print(x.numero_porta)
        print(x.quantidade)
        print()
