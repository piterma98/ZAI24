FROM python:3.11.11-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    wait-for-it \
    curl \
    rlwrap \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

ENV USER user
ENV HOME /home/$USER
ENV PATH $HOME/.local/bin:$PATH
RUN useradd --user-group $USER --create-home --home-dir $HOME

USER $USER
WORKDIR $HOME

USER user

ARG APP_VERSION
ENV APP_VERSION=$APP_VERSION

COPY ./src/requirements/base.txt /tmp/base.txt
RUN pip install --user --no-cache-dir -r /tmp/base.txt

WORKDIR $HOME/src
COPY --chmod=777 ./src/ .

USER root

RUN mkdir -p static && chown -R user:user static
RUN mkdir -p media && chown -R user:user media
USER user

RUN pip install --user --no-cache-dir ipython==9.0.2
RUN python manage.py collectstatic --noinput


ENTRYPOINT [ "./entrypoint.sh" ]

