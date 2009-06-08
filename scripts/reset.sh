echo "drop database {{ db_name }};" | mysql --user={{ db_user }} --password={{ db_password }}
rm -rf /home/websites/{{ site_directory }}/
rm -rf /home/websites/lighttpd/{{ site_directory }}
rm /etc/apache2/sites-enabled/{{ apache_conf }} && rm /etc/apache2/sites-available/{{ apache_conf }}
rm /etc/lighttpd/conf-enabled/{{ lighttpd_conf }} && rm /etc/lighttpd/conf-available/{{ lighttpd_conf }}