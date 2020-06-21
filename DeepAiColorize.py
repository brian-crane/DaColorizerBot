import requests

def getDeepMindImg(imgUrl):
    r = requests.post(
        "https://api.deepai.org/api/colorizer",
        data={
            'image': 'https://i.redd.it/slilibrw36651.jpg',
        },
        headers={'api-key': 'quickstart-QUdJIGlzIGNvbWluZy4uLi4K'}
    )
    print(r.json())
    return r.json()