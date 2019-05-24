import requests

index = 0
with open("urls.txt", "r") as url_file:
    for url in url_file.readlines():
        url = url.strip('\n')
        r = requests.get(url, verify=False)
        if r.status_code == 200:
            index += 1
            with open("images/"+str(index)+".jpg", "wb") as img:
                img.write(r.content)
