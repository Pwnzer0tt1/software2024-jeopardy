import os

basedir = os.path.abspath(os.path.dirname(__file__))

static_articles = [
    {
        "title":"1.000.000$ FLAG 🚩",
        "description":"Acquista una flag antica 1.000.000 di anni fa, vale 1$ per ogni anno di vita. Affrettati a comprarla!",
        "price":1_000_000.00,
        "img":"/static/imgs/art6.png",
        "secret_content": f"""
Hai davvero speso 1.000.000$ di dollari per una flag?
Ecco un tutorial per la prossima volta:
<br />
e la tua flag: {os.getenv('FLAG1','FLAG{REDACTED1}')}
<br />
<iframe width="560" height="315" src="https://www.youtube.com/embed/KEkrWRHCDQU" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

"""
    },
    {
        "title":"Cappello Gatto 😺",
        "description":"Descrizione Articolo 1",
        "price":8.0,
        "img":"/static/imgs/art4.png",
        "secret_content": "🎩🐈"
    },
    {
        "title":"Sticker Pwnzer0tt1",
        "description":"Gli sticker ufficiali dei Pwnzer0tt1 ad un prezzo STRACCIATO🍕",
        "price":2.25,
        "img":"/static/imgs/art1.png",
        "secret_content": """<img src="/static/imgs/sticker.jpg" >"""
    },
    {
        "title":"-10°C FLAG 🚩",
        "description":"Questa flag deve essere conservata a -10°C, hai bisogno di un 'Samsung Smart Fridge' per poterla acquistare'",
        "price":4_599.98,
        "img":"/static/imgs/art7.png",
        "secret_content": f"""
<img src="/static/imgs/samsung_smart_fridge.png" >
{os.getenv('FLAG2','FLAG{REDACTED2}')} 
"""
    },
    {
        "title":"Nyan Cat 🌈",
        "description": "🐈🐈🐈🐈🐈🐈🐈🐈🐈",
        "price":20.50,
        "img":"/static/imgs/art3.png",
        "secret_content": """<iframe width="560" height="315" src="https://www.youtube.com/embed/2yJgwwDcgV8?si=kLvxZgdSgOlOO6S9" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>"""
    },
    {
        "title":"STACCAH! STACCAH!",
        "description":"CI STANNO TRACCIANDO! STACCAH 🔌",
        "price":0.01,
        "img":"/static/imgs/art5.png",
        "secret_content": f"""
        <iframe width="560" height="315" src="https://www.youtube.com/embed/oE5JTpoIYck" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
        """
    },


]

secret_article = {
    "title":"FLAG 🚩",
    "description":"Questa flag è molto speciale, non può essere acquistata normalmente.",
    "price":0.0,
    "img":"/static/imgs/secret.png",
    "secret_content": f"Sei un vero appassionato di gatti vedo... 🐈 Meriti questa flag: {os.getenv('FLAG3','FLAG{REDACTED3}')} "
}