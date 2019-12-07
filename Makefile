build:
	docker build -t caarlos0/nuofx .

run:
	@docker run --rm -it -e NU_CPF=$(NU_CPF) -e NU_PWD=$(NU_PWD) -v $(HOME)/Downloads/:/tmp caarlos0/nuofx

push:
	docker push caarlos0/nuofx
