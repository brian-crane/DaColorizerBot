import requests

def getDeepMindImg(imgUrl):
    r = requests.post(
        "https://api.deepai.org/api/deepdream",
        data={
            'image': imgUrl,
        },
        headers={'api-key': '7fc825a0-b653-4a6e-a10b-73bccf48522e'}
    )
    out = str(r.content)
    out = out[out.index("https://"):len(out)-5]
    #(str(r.content))
    return out