serve-dev:
	python manage.py runserver 8001

serve-tunnel:
	python ./scripts/dev_tunnel.py -l 8001 -d notices

