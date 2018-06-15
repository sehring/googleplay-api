import os.path
import re
import smtplib # email
from time import sleep
from random import randint

from gpapi.googleplay import GooglePlayAPI, LoginError
import cred # credential file

# set locale & timezone
server = GooglePlayAPI(cred.locale, cred.timezone)

# LOGIN
try:
    # Login with prestored token
    server.login(None, None, cred.token, cred.gsfId)
except:
    # Fallback to manual login
    server.login(cred.email, cred.password, None, None)
    # Replace old token
    with open("cred.py","r") as f:
        content = f.read()
    content = re.sub('[0123456789]{15,}', str(server.gsfId), content)
    content = re.sub('[^ "]{50,}', str(server.authSubToken), content)
    with open('cred.py', 'w') as f:
        f.write(content)
      
# LIST Apps
# get categories
browse = server.browse()
categories = [x['catId'] for x in browse]

# write app names to list.txt
with open("list.txt", "w") as f:
    for category in categories:
        for subcategory in cred.subcategories:
            for offset in range(0, 500, 100): # rankings consist of at most 500 entries
                sleep(randint(1, 9)) # avoid limiting
                try:
                    appList = server.list(category, subcategory, "100", str(offset))
                    for app in appList:
                        f.write(app["docId"] + "\n") # write app name to file
                except:
                    pass

# FILTER List
with open("list.txt") as f:
    applist = f.readlines()
    applist = [x.strip() for x in applist]
applist = list(set(applist))  # remove duplicates
splitted_list = [ applist[x : x + 100] for x in range(0, len(applist), 100) ]  # split into lists of 100

f = open("list.txt", "w")
for sublist in splitted_list:
    sleep(randint(1, 9)) # avoid limiting
    try:
        bulk = server.bulkDetails(sublist) # fetch app details
    except:
        pass
    for app_details in bulk:
        try:
            # print (list(app_details.items())) # print all details for debug # nested dict->list->dict # TODO remove
            if app_details.get("offer")[0].get("checkoutFlowRequired") is False: # remove non-free apps  
                f.write(app_details.get("docId") + "\n")
        except:
            pass
f.close()

# DOWNLOAD Apps from List
# read list
with open("list.txt") as f:
    applist = f.readlines()
    applist = [x.strip() for x in applist]

# download apps from list
dl_counter = 0
for app in applist:
    if os.path.exists("downloads/%s.apk" % app) is False: # skip already downloaded apps
        sleep(randint(1, 9)) # avoid limiting
        try:
            fl = server.download(app) # download app
            with open("downloads/" + app + ".apk", "wb") as apk_file: # save app to disk
                for chunk in fl.get("file").get("data"):
                    apk_file.write(chunk)
                dl_counter += 1
        except:
            pass

# send email when script is done
server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(cred.email, cred.password)
server.sendmail(cred.email, "michael.sehring@rub.de", str(dl_counter) + " Apps successfully fetched")
server.quit()
