#!/usr/bin/env bash
set -eu

BASIC_AUTHENTICATION_USER_NAME=${BASIC_AUTHENTICATION_USER_NAME}
BASIC_AUTHENTICATION_USER_PASSWORD=${BASIC_AUTHENTICATION_USER_PASSWORD}

# @see https://www.digitalocean.com/community/tutorials/how-to-set-up-password-authentication-with-apache-on-ubuntu-14-04
htpasswd -b -c /etc/apache2/.htpasswd "${BASIC_AUTHENTICATION_USER_NAME}" "${BASIC_AUTHENTICATION_USER_PASSWORD}"

match='\s*#Include\sconf-available\/serve-cgi-bin\.conf'
raw='        #Include conf-available\/serve-cgi-bin.conf'
insert="        <Directory \"\/var\/www\/html\">\n            AuthType Basic\n            AuthName \"Restricted Content\"\n            AuthUserFile \/etc\/apache2\/.htpasswd\n            Require valid-user\n        <\/Directory>"
file='/etc/apache2/sites-available/000-default.conf'

sed -i "s/$match/$raw\n$insert/" "$file"

# @see https://serverfault.com/questions/773866/ah00027-no-authentication-done-error-after-upgrading-from-apache-2-2-to-2-4/774084#774084
echo "Include mods-available/authz_core.load" >> /etc/apache2/apache2.conf

set +u
exec docker-entrypoint-original.sh "${@}"
