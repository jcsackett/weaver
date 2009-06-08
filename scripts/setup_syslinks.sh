#!/bin/bash
cd /home/websites/lighttpd/fab/site_media/
if [[ -d /home/websites/lighttpd/site_media/css ]]; then
    echo "Media links exist."
else
    ln -s /home/websites/fab/fabsite/site_media/* .
    ln -s /usr/lib/python2.5/site-packages/django/contrib/admin/media ./admin_media
fi

cd /home/websites/fab
if [[ -d /home/websites/fab/cache ]]; then
    echo "Cache link exists."
else
    ln -s /home/websites/lighttpd/fab/lighttpdcache ./cache
fi

if [[ -d /home/websites/fab/media ]]; then
    echo "Second media link exists."
else
    ln -s /home/websites/lighttpd/fab/site_media ./media
fi

cd /home/websites/fab/logs
if [[ -d /home/websites/fab/logs/lighttpd ]]; then
    echo "Log links exist."
else
    ln -s /var/log/lighttpd/fab ./lighttpd
fi
