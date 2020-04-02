from urllib.request import Request, urlopen
import urllib.request
import re
import http


def getHTML(url):
    # Open the URL
    # Spoof the user agent
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
    req = Request(url=url, headers=headers)
    # Read the response as HTML
    try:
        html = urlopen(req).read().decode('ascii', 'ignore')
        if len(re.findall('error-desc', html)) > 0:
            return None
        else:
            return html
    except urllib.error.HTTPError as err:
        print("%s for %s" % (err.code, url))
        return None
    except:
        print('END POINT ERROR')
        return None