ARG WORDPRESS_IMAGE_TAG
FROM wordpress:${WORDPRESS_IMAGE_TAG}
RUN if [ -e /usr/local/bin/docker-entrypoint.sh ] ; then mv /usr/local/bin/docker-entrypoint.sh /usr/local/bin/docker-entrypoint-original.sh ; fi
COPY --chmod=0755 ./docker-entrypoint.sh /usr/local/bin/
