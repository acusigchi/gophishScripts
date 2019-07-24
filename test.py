from gophish import Gophish

apiKey = "a13fe2c8d9b2fff652fed82530e4c6db5fe7acc0012808968a113d8cb724941a"
baseUri = "https://www.acu-edu.info:3333"
apiConnection = Gophish(apiKey, host=baseUri, verify=False)

for page in apiConnection.pages.get():
    print(page.name)
