[pytest]

addopts = --color=yes --cov=quest2pdf --cov-report=term -ra

log_cli = 1
log_cli_level = INFO
log_cli_format = %(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)
log_cli_date_format = %Y-%m-%d %H:%M:%S
