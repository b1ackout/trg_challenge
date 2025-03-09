
help:
	@echo "network - Create the develop docker network"
	@echo "spark - Run a Spark cluster (exposes port 8100)"
	@echo "jupter - Run a Jupyter server (exposes port 9999)"
	@echo "jupter-token - Print the jupyter authentication token"
	@echo "generate_df - Run a spark submit job"
	@echo unpack_data - Unzip the downloaded data
	@echo down - Stops all containers

all: network spark jupyter

network:
	@docker network inspect develop >/dev/null 2>&1 || docker network create develop

spark:
	docker-compose up -d

generate_df:
	cp pyspark/src/* /tmp/
	docker exec spark spark-submit \
	       	--master spark://spark:7077 \
		/data/generate_df.py

generate_kpis:
	cp pyspark/src/* /tmp/
	docker exec spark spark-submit \
	       	--master spark://spark:7077 \
		/data/generate_kpis.py

jupyter:
	@docker start jupyter > /dev/null 2>&1 || docker run \
	    -p 9999:8888 \
		-p 4040:4040 \
		-p 4041:4041 \
		-v /tmp:/home/jovyan \
		--net=develop \
		--name jupyter_pyspark \
		--restart always \
		-e GRANT_SUDO=yes \
		-d docker pull jupyter/pyspark-notebook:x86_64-spark-3.5.0
jupyter_token:
	@docker logs jupyter_pyspark 2>&1 | findstr '\?token\='

unpack_data:
	cp .\files\data\subscribers.csv /tmp
down:
	docker compose down
	docker stop jupyter_pyspark
