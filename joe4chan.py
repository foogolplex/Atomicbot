#IMPORTANT
#Don't remove the time.sleeps; which are in place to comply with 4chan's API rule of 'no more than 1 request per second'
#https://github.com/4chan/4chan-API
import requests, random, json, time

#Returns [random image URL, random image's thread URL]
async def req_4chan():
    #Select a board
    board = 'b'

    #Request board catalog, and get get a list of threads on the board; then sleeping for 1.5 seconds
    threadnums = []
    data = (requests.get('http://a.4cdn.org/' + board + '/catalog.json')).json()
    time.sleep(1.5)

    #Get a list of threads in the data
    for page in data:
        for thread in page["threads"]:
            threadnums.append(thread['no'])

    #Select a thread
    thread = random.choice(threadnums)

    #Request the thread information, and get a list of images in that thread; again sleeping for 1.5 seconds
    imgs = list()
    pd = (requests.get('http://a.4cdn.org/' + board + '/thread/' + str(thread) + '.json')).json()
    for post in pd['posts']:
        #Ignore key missing error on posts with no image
        try:
            imgs.append(str(post['tim']) + str(post['ext']))
        except:
            pass

    #Select an image
    image = random.choice(imgs)

    #Assemble and return the urls
    imageurl = 'https://is2.4chan.org/' + board + '/' + image
    thread = 'https://boards.4chan.org/' + board + '/thread/' + str(thread)
    return [imageurl , thread]

async def get_thread():
    urls = await req_4chan()
    return urls