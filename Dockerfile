FROM debian:9.6

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        apache2 \
        python \
        ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /tmp/pear

RUN a2dissite 000-default

RUN a2enmod cgid rewrite
RUN echo 'ServerName feedvalidator.org' >>/etc/apache2/apache2.conf

WORKDIR /feedvalidator

ADD . /feedvalidator
ADD sites-available-feedvalidator.conf /etc/apache2/sites-available/feedvalidator.conf

RUN a2ensite feedvalidator

EXPOSE 80

ENV HTTP_HOST https://feedvalidator.org/
ENV SCRIPT_NAME check.cgi
ENV SCRIPT_FILENAME /feedvalidator/check.cgi

CMD ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"]
