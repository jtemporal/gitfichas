FROM ruby:3.2-alpine AS base

# Instalar dependências mínimas necessárias para Jekyll e gems nativas
RUN apk add --no-cache build-base gcc make libc-dev \
    libffi-dev yaml-dev zlib-dev

WORKDIR /srv/jekyll

COPY Gemfile Gemfile.lock ./

# Instalar bundler e gems
RUN gem install bundler -v 2.4.22 

# Expor portas padrão do Jekyll
EXPOSE 4000 35729

ENTRYPOINT ["jekyll"]
CMD ["--help"]