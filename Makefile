conda-export:
	conda env export > conda.yml

db:
	docker-compose up -d mongodb

run:
	docker-compose up -d
