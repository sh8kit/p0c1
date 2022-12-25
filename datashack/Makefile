build:
	docker build . -t mzsrtgzr/poc_1_app:latest

docker_push:
	docker push mzsrtgzr/poc_1_app:latest

terraform_apply_internal:
	terraform apply -var presto_host=presto -var kafka_connect_host=kafka-connect -var minio_host=minio -var  kafka_bootstarp_server="kafka:29092"