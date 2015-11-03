#!/usr/bin/env python

from lib.endomondo import Endomondo
import lib.tcx as tcx
import re
import getpass
import sys
import os
import requests  # Verifica PROXY

__VERSION__ = "0.4.2"
__APP__ = "Endomondo Export TCX files"

nl = "\n"
CREDENCIALES = "endomondo_data.txt"
sesion = requests.Session()
ERROR_NO_INTERNET = "ERROR"

# create a somewhat useful filename for the specified workout
def create_filename(workout):
    ret = ''
    if workout.start_time:
        ret = workout.start_time.strftime("%Y%m%d") + "_"
    ret += str(workout.id)
    name = workout.name
    if name:
        name = re.sub(r'[\[\]/\\;,><&*:%=+@!#\(\)\|\?\^]', '', name)
        name = re.sub(r"[' \t]", '_', name)
        ret += "_" + name
    ret += ".tcx"
    return ret


# create a new directory to store the exported files in
def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


# create the TCX file for the specified workout
def create_tcx_file(workout):
    directory_name = 'export'
    activity = workout.get_activity()
    name = create_filename(workout)
    create_directory(directory_name)
    filename = os.path.join(directory_name, name)
    if not os.path.isfile(filename):
        print "Writing %s, %s, %s trackpoints" % (filename, activity.sport, len(activity.trackpoints))

        writer = tcx.Writer()
        tcxfile = writer.write(activity)
        if tcxfile:
            with open(filename, 'w') as f:
                f.write(tcxfile)

def credenciales():
    txt = [""]
    try:
        with open(CREDENCIALES, 'r') as r:
            txt = r.read()
            txt = txt.split(nl)
            if len(txt) == 2: txt.append('')    # No proxi en fichero TXT
    except:
        txt = [""]
    return txt

def main():
    try:
        print "Endomondo: export most recent workouts as TCX files"
        cred = credenciales()

        if len(cred) > 1:
            email, password, proxy = cred  # cred[0], cred[1]
            s_proxy = necesita_proxy(proxy)
            if s_proxy == ERROR_NO_INTERNET:
                print ("No Internet Access. Impossible to continue!")
                return 0
        else:
            email = raw_input("Email: ")
            password = getpass.getpass()

        maximum_workouts = raw_input("Maximum number of workouts (press Enter to ignore) ")
        endomondo = Endomondo(email, password, s_proxy)

        workouts = endomondo.get_workouts(maximum_workouts)
        print "Fetched latest", len(workouts), "workouts"
        for workout in workouts:
            create_tcx_file(workout)
        print "Export done!!"
        return 0

    except ValueError, exception:
        sys.stderr.write(str(exception) + "\n")
        return 1

def necesita_proxy(proxy):
    url = "http://www.bing.es"
    t_proxy = ""
    html = get_url(url)
    if not html:
        t_proxy = proxy
        sesion.proxies = {"http": proxy, "https": proxy}
        html = get_url(url)
        if not html:
            sesion.proxies = {}
            t_proxy = ERROR_NO_INTERNET
    return t_proxy

def get_url(url):
    try:
        r = sesion.get(url)
        return r.text
    except:
        return ''

if __name__ == "__main__":
    sys.exit(main())
