.PHONY: build sleep20 minio-provision down

build:
	mkdir -p yamls
	docker-compose up -d --remove-orphans
create_tf_state_bucket:
	docker-compose -f docker-compose.s3.yaml up -d
#minio-provision:
#	docker-compose -f docker-compose.s3.yml up

kill:
	docker-compose -f docker-compose.destroy.yaml up -d
down:
	docker-compose down
sleep20:
	sleep 20

# automate
up: build sleep20 create_tf_state_bucket
down: down
