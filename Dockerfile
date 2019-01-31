FROM frolvlad/alpine-miniconda3 as builder

MAINTAINER Pascal Pellmont <github@ppo2.ch>

COPY .condarc /opt/conda/
COPY setup.* /app/
COPY environment.yml /app/
COPY pymlhelloworld /app/pymlhelloworld/
COPY requirements.txt /app/
COPY LICENSE /app/
COPY .coveragerc /app/
WORKDIR /app
RUN conda env create --file /app/environment.yml -p /env \
    && source activate /env \
    && tox \
    && conda install uwsgi \
    && pip install -r requirements.txt \
    && pip install .

FROM frolvlad/alpine-miniconda3

MAINTAINER Pascal Pellmont <github@ppo2.ch>

COPY --from=builder /env /env
EXPOSE 5000
RUN adduser --system uwsgi
USER uwsgi
CMD source activate /env && uwsgi --http 0.0.0.0:5000 --master --module pymlhelloworld.app:APP --processes 4



