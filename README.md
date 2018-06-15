# PlayStoreApkcrawler

This project contains an Play Store crawler. It is based on an unofficial google play API for, see (https://github.com/NoMore201/googleplay-api).

It crawls every free app in the first 500 position of each Play Store category and downloads it, if it does not exist in the local directory. 

Possible improvements..

* add database of apk version numbers
* add comparison with new crawls
* => overwrite old versions => up-to-date database

* add detailed exceptions

# Usage
 python3 dl_apk.py
