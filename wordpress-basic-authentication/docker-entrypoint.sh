#!/usr/bin/env bash
set -eu

# Function to compare two semantic versions
# Returns 0 if v1 = v2
# Returns 1 if v1 > v2
# Returns 2 if v1 < v2
semver_compare() {
  if [[ "$1" == "$2" ]]; then
    return 0
  fi

  local IFS=.
  local v1=($1)
  local v2=($2)

  # Pad shorter version with zeros for consistent comparison
  for ((i=0; i<${#v1[@]} || i<${#v2[@]}; i++)); do
    local n1=${v1[i]:-0} # Default to 0 if component is missing
    local n2=${v2[i]:-0} # Default to 0 if component is missing

    if (( 10#$n1 > 10#$n2 )); then
      return 1
    elif (( 10#$n1 < 10#$n2 )); then
      return 2
    fi
  done

  return 0
}

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

# # Since legacy image doesn't support `WORDPRESS_CONFIG_EXTRA`, the version threshold: < 5.0.0 may not accurate.
# Inject WORDPRESS_CONFIG_EXTRA into wp-config-sample.php
# before the original entrypoint processes it
# semver_compare "$WORDPRESS_VERSION" '5.0.0'
# if [ $? -eq 2 ]; then
if [ -n "${WORDPRESS_CONFIG_EXTRA:-}" ]; then
    WP_SAMPLE="/usr/src/wordpress/wp-config-sample.php"

    if [ -f "$WP_SAMPLE" ] && ! grep -q "WORDPRESS_CONFIG_EXTRA_INJECTED" "$WP_SAMPLE"; then
        echo >&2 "Injecting WORDPRESS_CONFIG_EXTRA into wp-config-sample.php..."

        # Create a temp file with the injection
        TEMP_FILE=$(mktemp)

        # Remove the default WP_DEBUG definition first (to avoid duplicate define)
        # Then inject WORDPRESS_CONFIG_EXTRA before "That's all, stop editing!" comment
        awk -v extra="$WORDPRESS_CONFIG_EXTRA" '
            # Skip the default WP_DEBUG line to prevent duplicate constant definition
            /^define\( *. *WP_DEBUG. *, *false *\);/ {
                next
            }
            /\/\* That.s all, stop editing/ {
                print "/* WORDPRESS_CONFIG_EXTRA_INJECTED */"
                print extra
                print ""
            }
            { print }
        ' "$WP_SAMPLE" > "$TEMP_FILE"

        # Replace the original
        mv "$TEMP_FILE" "$WP_SAMPLE"

        echo >&2 "WORDPRESS_CONFIG_EXTRA injection complete."
    fi
fi
# fi

set +u
exec docker-entrypoint-original.sh "${@}"
