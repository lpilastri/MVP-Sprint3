# Meu Front

Projeto de MVP para a conclusão do Sprint III da Pós Graduação em Engenharia de Software pela PUC-RIO

---
## Como executar em modo de desenvolvimento

Basta fazer o download do projeto e abrir o arquivo index.html no seu browser.

## Como executar através do Docker

Certifique-se de ter o [Docker](https://docs.docker.com/engine/install/) instalado e em execução em sua máquina.

Navegue até o diretório que contém o Dockerfile no terminal e seus arquivos de aplicação e
Execute **como administrador** o seguinte comando para construir a imagem Docker:

```
$ docker build --pull --rm -f "Dockerfile" -t mvp-front:latest "."
```

Uma vez criada a imagem, para executar o container basta executar, **como administrador**, seguinte o comando:

```
$ docker run -d -p 8080:80 mvp-front
```

Uma vez executando, para acessar o front-end, basta abrir o [http://localhost:8080/#/](http://localhost:8080/#/) no navegador.

## API Externa

A API externa utilizada se chamaAI Weather by Meteosource, é uma API que apresenta dados metereológicos 
baseado em coordenadas de lat e long passadas em sua chamada.

Sua licença gratuita é baseada em um cadastro feito através do site https://rapidapi.com/MeteosourceWeather/api/ai-weather-by-meteosource/
e permite até 100 acessos durante o mês. a chave de acesso é passada através do header da chamada da API externa, que esta no arquivo script.js

A rota implementada é a "GET".
