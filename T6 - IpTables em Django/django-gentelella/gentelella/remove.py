# ---------------------------------------------------------------------------
# Remover todos os dados do banco

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gentelella.settings")

import django
django.setup()

from app.models import IpsFonte
from app.models import IpTables
from app.models import Portas

if __name__ == '__main__':
    print('IpTables:', IpTables.objects.all())

    # Remover tudo de IpTables()
    print('Removendo tudo de IpTables()...')
    iptables = IpTables.objects.all()
    iptables.delete()
    print('IpTables vazio:', IpTables.objects.all())

    print()

    ips = IpsFonte.objects.all()
    print('Lista de Ips Fonte:', ips)

    for x in ips:
        print(x.ident)
        print(x.endereco_ip)
        print(x.numero_pacotes)
        print(x.pais)
        print()

    # Remover tudo de IpsFonte()
    print('Removendo tudo de IpsFonte()...')
    ips = IpsFonte.objects.all()
    ips.delete()
    print('Lista de Ips Fonte vazia:', IpsFonte.objects.all())

    portas = Portas.objects.all()
    print('Lista de Portas:', portas)

    for x in portas:
        print(x.ident)
        print(x.nome)
        print(x.numero_porta)
        print(x.quantidade)
        print()

    # Remover tudo de Portas()
    print('Removendo tudo de Portas()...')
    portas = Portas.objects.all()
    portas.delete()
    print('Lista de Portas vazia:', Portas.objects.all())
