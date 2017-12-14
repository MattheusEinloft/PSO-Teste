source venv/bin/activate          # ativar virtual environment
cd django-gentelella
cd gentelella

python manage.py runserver        # rodar servidor

python script.py iptablesyslog    # executar script que adiciona dados no banco

python remove.py                  # executar script que remove tudo do banco

# caso sejam feitas alteracoes no banco (models.py), executar:
python manage.py makemigrations
python manage.py migrate

