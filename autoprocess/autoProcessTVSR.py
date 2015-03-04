#!/usr/bin/env python

# Author: Nic Wolfe <nic@wolfeden.ca>
# URL: http://code.google.com/p/sickbeard/
#
# This file is part of SickRage.
#
# SickRage is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SickRage is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SickRage.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import with_statement

import os.path
import sys
import 

sys.path.insert(1, os.path.abspath(os.path.join(os.path.dirname(__file__), 'lib')))

try:
    import requests
except ImportError:
    print ("You need to install python requests library")
    sys.exit(1)

# Try importing Python 2 modules using new names
try:
    import urllib2
    from urllib import urlencode

# On error import Python 3 modules
except ImportError:
    import urllib.request as urllib2
    from urllib.parse import urlencode

def processEpisode(dir_to_process, settings, org_NZB_name=None, status=None):
    host = settings.Sickbeard['host']
    port = settings.Sickbeard['port']
    username = settings.Sickbeard['user']
    password = settings.Sickbeard['pass']

    try:
        ssl = int(settings.Sickbeard['ssl'])
    except:
        ssl = 0

    try:
        web_root = settings.Sickbeard['web_root']
        if not web_root.startswith("/"):
            web_root = "/" + web_root
        if not web_root.endswith("/"):
            web_root = web_root + "/"
    except:
        web_root = ""

    params = {}

    params['quiet'] = 1

    params['dir'] = dir_to_process
    if org_NZB_name != None:
        params['nzbName'] = org_NZB_name

    if status != None:
        params['failed'] = status

    if ssl:
        protocol = "https://"
    else:
        protocol = "http://"

    url = protocol + host + ":" + port + web_root + "home/postprocess/processEpisode"
    login_url = protocol + host + ":" + port + web_root + "login"

    print ("Opening URL: " + url)

    try:
        sess = requests.Session()
        sess.post(login_url, data={'username': username, 'password': password}, stream=True, verify=False)
        result = sess.get(url, params=params, stream=True, verify=False)

        for line in result.iter_lines():
            if line:
                print (line.strip())

    except IOError:
        e = sys.exc_info()[1]
        print ("Unable to open URL: " + str(e))
        sys.exit(1)


if __name__ == "__main__":
    print ("This module is supposed to be used as import in other scripts and not run standalone.")
    print ("Use sabToSickBeard instead.")
    sys.exit(1)