FROM python:3.10
WORKDIR .
COPY /src .
ADD src/requirements.txt .
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
ENV TZ=Asia/Yekaterinburg
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezon
CMD  python manage.py run_worker
