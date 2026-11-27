run-api:
	uv run uvicorn api.fast:app --reload

build-docker-local:
	docker build -t ${DOCKER_IMAGE_NAME}:dev .

docker-run:
	docker run -p 8080:8080 ${DOCKER_IMAGE_NAME}:dev

build-docker-cloud:
	docker build --platform linux/amd64 -t ${GAR_IMAGE_NAME}:prod .

docker-push:
	docker push ${GAR_IMAGE_NAME}:prod

deploy:
	gcloud run deploy ${DOCKER_IMAGE_NAME} --image ${GAR_IMAGE_NAME}:prod --region ${GCP_REGION} --allow-unauthenticated
