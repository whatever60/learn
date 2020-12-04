# This Dockerfile uses multi-stage build to customize DEV and PROD images:
# https://docs.docker.com/develop/develop-images/multistage-build/

FROM python:3.8.6-slim-buster AS development_build

LABEL maintainer="Yiming Qu, Tsinghua University <quym@foxmail.com>"

ARG DS_ENV

ENV DS_ENV=${DS_ENV} \
	# build:
	BUILD_ONLY_PACKAGES='wget' \
	# python:
	PYTHONFAULTHANDLER=1 \
	PYTHONUNBUFFERED=1 \
	PYTHONHASHSEED=random \
	PYTHONDONTWRITEBYTECODE=1 \
	# pip:
	PIP_NO_CACHE_DIR=off \
	PIP_DISABLE_PIP_VERSION_CHECK=on \
	PIP_DEFAULT_TIMEOUT=100 \
	# poetry:
	POETRY_VERSION=1.1.4 \
	POETRY_NO_INTERACTION=1 \
	POETRY_VIRTUALENVS_CREATE=false \
	POETRY_CACHE_DIR='/var/cache/pypoetry' \
	PATH="$PATH:/root/.poetry/bin" \

# System deps:
RUN apt-get update && \
	apt-get install --no-install-recommends -y \
    bash \
    build-essential \
    curl \
    gettext \
    git \
    libpq-dev \
	zsh \
    # Defining build-time-only dependencies:
    $BUILD_ONLY_PACKAGES \
	# Installing `poetry` package manager:
	# https://github.com/python-poetry/poetry
	curl -sSL 'https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py' | python && \
	poetry --version && \
	# Removing build-time-only dependencies:
	apt-get remove -y $BUILD_ONLY_PACKAGES && \
	# oh-my-zsh
	curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh && \
	git clone git://github.com/zsh-users/zsh-autosuggestions .oh-my-zsh/plugins/zsh-autosuggestions && \
	git clone https://github.com/zsh-users/zsh-syntax-highlighting.git .oh-my-zsh/plugins/zsh-syntax-highlighting && \
	# Cleaning cache:
	apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false && \
	apt-get clean -y && rm -rf /var/lib/apt/lists/* && \
	chsh -s /bin/zsh \
	mkdir /havefun

COPY .zshrc .

SHELL ["zsh", "-c"]

RUN source .zshrc

WORKDIR /havefun

# Setting up proper permissions:
RUN groupadd -r wusuowei60 && useradd -d /havefun -r -g wusuowei60 wusuowei60 \
	&& chown wusuowei60:wusuowei60 -R /havefun \
	&& mkdir -p /var/www/django/static /var/www/django/media \
	&& chown wusuowei60:wusuowei60 /var/www/django/static /var/www/django/media

# Copy only requirements, to cache them in docker layer
COPY --chown=wusuowei60:wusuowei60 ./poetry.lock ./pyproject.toml /havefun/

# Project initialization:
RUN echo "$DS_ENV" && \
	poetry install \
		$(if [ "$DS_ENV" = 'production' ]; then echo '--no-dev'; fi) \
		--no-interaction --no-ansi && \
	jupyter labextension install @jupyterlab/git @telamonian/theme-darcula && \
	# Cleaning poetry installation's cache for production:
	if [ "$DS_ENV" = 'production' ]; then rm -rf "$POETRY_CACHE_DIR"; fi

COPY --chown=wusuowei60:wusuowei60 @jupyterlab .jupyter/lab/user-settings/@jupyterlab

# Running as non-root user:
USER wusuowei60

# The following stage is only for Prod:
# https://wemake-django-template.readthedocs.io/en/latest/pages/template/production.html
FROM development_build AS production_build
COPY --chown=wusuowei60:wusuowei60 . /havefun

CMD ["zsh"]
