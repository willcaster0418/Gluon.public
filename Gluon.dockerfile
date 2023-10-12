FROM nginx:latest
# 설치를 위한 폴더 및 파일 설정
# - 폴더설정
COPY ./install /install
COPY ./install/locale.gen /etc/locale.gen
COPY ./pkg /install/pkg
COPY ./run /install/run
COPY ./config /install/config
COPY ./install/.bashrc /root/.bashrc

# - 로컬시간 설정
RUN rm -rf /etc/localtime
RUN ln -s /usr/share/zoneinfo/Asia/Seoul /etc/localtime

# - 파이썬 패키지 설정
RUN apt-get update
RUN apt-get install -y python3.11
RUN apt-get install -y pip
RUN rm -f /usr/lib/python3.11/EXTERNALLY-MANAGED
RUN pip install -r /install/requirements.txt

# - Ngnix 관련 패키지 설치
RUN apt-get install -y uwsgi
RUN apt-get install -y uwsgi-plugin-python3

# - 데이타베이스 관련 패키지 설치(mariadb)
RUN apt-get install -y procps
RUN apt-get install -y mariadb-server

RUN rm -f /var/log/nginx/access.log
RUN rm -f /var/log/nginx/error.log
RUN touch /var/log/nginx/access.log
RUN touch /var/log/nginx/error.log
RUN echo "[mysqld]" >> /etc/mysql/my.cnf
RUN echo "lower_case_table_names=0" >> /etc/mysql/my.cnf

# - 기타 패키지 설치
RUN apt-get install -y vim
RUN apt-get install -y locales
RUN locale-gen

EXPOSE 22
EXPOSE 80

ENV TERM xterm-256color
ENV ENV DEV
ENV LC_ALL=ko_KR.UTF-8
ENV PYTHONENCODING=utf-8

COPY ./client/build /client-dist
RUN /install/install.sh
CMD ["/gluon/run/start.sh"]