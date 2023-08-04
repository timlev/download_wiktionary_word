import urllib
import urllib.parse
import urllib.request
import os
import tempfile
import platform
import bs4

def check_downloaded_word(word, directory="./"):
    """Check if word is already in directory in any format.
    Returns True or False"""
    soundfiles = os.listdir(directory)
    #strip extension
    downloaded_words = [os.path.splitext(x)[0] for x in soundfiles]
    if word in downloaded_words:
        return True
    else:
        return False

def choose(ogg_files):
    if len(ogg_files) == 0:
        return ""
    choice = ""
    while choice not in [str(x) for x in range(len(ogg_files))] and choice != None:
        print('Choices:')
        for i, c in enumerate(ogg_files):
            print(str(i), ":",c)
        choice = input("Which do you want?\n")
    return ogg_files[int(choice)].replace("/wiki/","")

def get_wiki(word, directory="./"):
    """Check if word is in directory and download word.ogg into directory"""
    """Return oggpath if it downloads successfully.
    Return 0 if it is already downloaded
    Return 1 if you have trouble searching.
    Return 2 if you can't download wiktionary page or ogg file."""
    if check_downloaded_word(word, directory):
        print(word + " already downloaded")
        return 0
    #search for wiktionary word
    base = "https://en.wiktionary.org/wiki/"
    query = base + urllib.parse.quote(word)
    print(query)
    try:
        response = urllib.request.urlopen(query)
        print(response)
    except:
        print("Couldn't find", word)
        return 1
    print("Processing response")
    index = bs4.BeautifulSoup(response,"html5lib")
    #search for links to ogg files
    links = [link.get("href") for link in index.find_all("a") if link.get("href") != None and ".ogg" in link.get("href")]
    print("Found: ", " ".join(links))
    us_links = [x for x in links if "n-us-" + word + ".ogg" in x]

    if len(us_links) > 0:
        #filenameguess = "File:en-us-" + word + ".ogg"
        #filenameguess = "File:en-us-" + word + ".ogg"
        filenameguess = us_links[0].replace("/wiki/","")
    else:
        filenameguess = choose(links)
    #Jump to file wiktionary page
    query = base + filenameguess
    try:
        response = urllib.request.urlopen(query)
    except:
        print("HTTP error for " + query)
        return 2
    print(response)
    index = bs4.BeautifulSoup(response, "html5lib")
    links = index.find_all("a")
    oggsource = ""
    for link in links:
        href = str(link.get("href"))
        #if "upload" in href and "n-us" in href and ".ogg" in href and word in href:
        if "upload" in href:
            oggsource = "https:" + href
            print(oggsource)
    print("Downloading to: " + os.path.join(directory, word + ".ogg"))
    try:
        print("Getting ogg...")
        getogg = urllib.request.urlopen(oggsource)
        print("Saving file ...")
        ofp = open(os.path.join(directory, word + ".ogg"),'wb')
        print("Writing file ...")
        ofp.write(getogg.read())
        ofp.close()
        return os.path.join(directory, word + ".ogg")
    except:
        #print("Could not download:", word)
        return 2


#convert ogg to mp3

def convert_ogg_to_mp3(oggfile, remove_ogg = False):
    """Return mp3path after converting with ffmpeg"""
    oggpath = os.path.abspath(oggfile)
    ogg_dir = os.path.dirname(oggfile)
    oggfile = os.path.basename(oggfile)
    mp3file = oggfile.replace(".ogg", ".mp3")
    mp3path = oggpath.replace(".ogg",".mp3")
    if os.path.exists(oggpath):
        os.system('ffmpeg -i "' + oggpath + '" -acodec libmp3lame "' + mp3path + '"')
        if remove_ogg:
            os.remove(oggpath)
        return mp3path
    else:
        print("************\n Problem with " + word + "\n******************\n")
    

if __name__ == "__main__":

    """Example usage of get_wiki() and convert_ogg_to_mp3"""
    #wordlist = ["school", "musician"]
    wordlist = ['yaup',
 'yawp',
 'yearn',
 'yield_up',
 'zero_in',
 'zip_by',
 'zip_up',
 'zonk_out',
 'zoom_along',
 'address']

    print(len(wordlist))
    missing_words = []
    for word in wordlist:
        if get_wiki(word) in [1,2]:
            missing_words.append(word)
        convert_ogg_to_mp3(word + ".ogg", True)
    print("Missing Words: {}".format(missing_words))
