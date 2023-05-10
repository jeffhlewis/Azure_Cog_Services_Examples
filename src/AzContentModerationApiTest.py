import requests
import json
import time

# -----=====-----=====-----=====-----=====-----=====-----=====-----=====-----=====-----=====-----=====
# Settings and endpoints
# -----=====-----=====-----=====-----=====-----=====-----=====-----=====-----=====-----=====-----=====
API_KEY                     = "<API KEY>"
API_ENDPOINT_BASE           = "https://<SUBDOMAIN>.cognitiveservices.azure.com/"
API_ENDPOINT_TEXT_SCREEN    = f"{API_ENDPOINT_BASE}contentmoderator/moderate/v1.0/ProcessText/Screen?autocorrect=true&PII=true&classify=true&language=eng"
API_ENDPOINT_IMAGE_OCR      = f"{API_ENDPOINT_BASE}contentmoderator/moderate/v1.0/ProcessImage/OCR?language=end&enhanced=true"
API_ENDPOINT_IMAGE_EVALUATE = f"{API_ENDPOINT_BASE}contentmoderator/moderate/v1.0/ProcessImage/Evaluate"

# -----=====-----=====-----=====-----=====-----=====-----=====-----=====-----=====-----=====-----=====
# Test Image URLs
# -----=====-----=====-----=====-----=====-----=====-----=====-----=====-----=====-----=====-----=====
IMAGE_CONTROL_ART           = "https://as2.ftcdn.net/v2/jpg/05/21/18/03/1000_F_521180377_2iAVJqBQSo3cgKaVp8vMBR8asrC61DoU.jpg"
IMAGE_CONTROL_PEOPLE        = "https://as2.ftcdn.net/v2/jpg/01/06/10/25/1000_F_106102543_8BpQIq6FmY72hMt4ZGArWYMKneLwl5aj.jpg"
IMAGE_TEXT_OFFENSIVE_1      = "https://i.etsystatic.com/32805953/r/il/7b73d7/3819750348/il_794xN.3819750348_lhmt.jpg"
IMAGE_TEXT_OFFENSIVE_2      = "https://i.kym-cdn.com/photos/images/newsfeed/001/152/678/242.jpg"
IMAGE_SUGGESTIVE_1          = "https://e00-marca.uecdn.es/assets/multimedia/imagenes/2022/11/04/16675708619484.jpg"
IMAGE_SUGGESTIVE_2          = "https://as2.ftcdn.net/v2/jpg/00/97/38/77/1000_F_97387751_My3G68BPBgf8Mte9ncDZhbTPQu3i5pNI.jpg"
IMAGE_ADULT_1               = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRIoCiibUXdGXPd8_ZYdmMDx0Gb-pdn2EgGLQ&usqp=CAU"
IMAGE_ADULT_2               = "https://ftopx.com/large/201202/29188.jpg"
IMAGE_GORY_1                = "https://bloody-disgusting.com/wp-content/uploads/2021/07/THE-SADNESS.jpg"
IMAGE_GORY_2                = "https://media.wbur.org/wp/2017/03/1111_vietnam01-1-1000x735.jpg"

# -----=====-----=====-----=====-----=====-----=====-----=====-----=====-----=====-----=====-----=====
# Functions
# -----=====-----=====-----=====-----=====-----=====-----=====-----=====-----=====-----=====-----=====
def jsonPrint(jsonString):
    """Pretty-prints a JSON string to console

    Args:
        jsonString (str): The JSOn string you wish to print
    """
    print(json.dumps(jsonString, indent=2))

def textScreenApi(content):
    """Calls the Azure Content Moderation Text Screen API

    Args:
        content (str): a text string you wish to screen for content

    Returns:
        JSON-encoded API response
    """
    requestUrl = API_ENDPOINT_TEXT_SCREEN
    requestData = content
    requestHeaders = {
        "Content-Type"  : "text/plain",
        "Ocp-Apim-Subscription-Key" : API_KEY
    }
    response = requests.post(url=requestUrl, data=requestData, headers=requestHeaders)
    return response.json()

def imageOcrAPI(imageUrl):
    """Calls the Azure Content Moderation Image OCR API

    Args:
        imageUrl (str): URL to an image you wish to run the Image OCR API against

    Returns:
        JSON-encoded API response
    """
    requestUrl = API_ENDPOINT_IMAGE_OCR
    requestData = json.dumps({
        "DataRepresentation": "URL",
        "Value": imageUrl
    })
    requestHeaders = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": API_KEY
    }
    response = requests.post(url=requestUrl, data=requestData, headers=requestHeaders)
    return response.json()

def imageEvalAPI(imageUrl):
    """Calls the Azure Content Moderation Image Evaluate API

    Args:
        imageUrl (str): URL to an image you wish to run the Image Evaluate API against

    Returns:
        JSON-encoded API response
    """
    requestUrl = API_ENDPOINT_IMAGE_EVALUATE
    requestData = json.dumps({
        "DataRepresentation": "URL",
        "Value": imageUrl
    })
    requestHeaders = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": API_KEY
    }
    response = requests.post(url=requestUrl, data=requestData, headers=requestHeaders)
    return response.json()

# -----=====-----=====-----=====-----=====-----=====-----=====-----=====-----=====-----=====-----=====
# Main
# -----=====-----=====-----=====-----=====-----=====-----=====-----=====-----=====-----=====-----=====
textToScreen = "Testing this lovely API and gathering results"
print(f"Text Screening 1: Control [{textToScreen}]")
jsonPrint(textScreenApi(textToScreen))

# Wait 1 second (to avoid API rate limit)
time.sleep(1)

textToScreen = "Testing this fucking API and shit"
print(f"Text Screening 2: Offensive Text [{textToScreen}]:")
jsonPrint(textScreenApi(textToScreen))

# Wait 1 second (to avoid API rate limit)
time.sleep(1)

print(f"Image Screening 1: Control (Art):")
jsonPrint(imageEvalAPI(IMAGE_CONTROL_ART))

# Wait 1 second (to avoid API rate limit)
time.sleep(1)

print(f"Image Screening 2: Control (People):")
jsonPrint(imageEvalAPI(IMAGE_CONTROL_PEOPLE))

# Wait 1 second (to avoid API rate limit)
time.sleep(1)

print(f"Image Screening 3: Offensive Text OCR (C-word):")
jsonPrint(imageOcrAPI(IMAGE_TEXT_OFFENSIVE_1))

# Wait 1 second (to avoid API rate limit)
time.sleep(1)

print(f"Image Screening 4: Offensive Text OCR (F-word):")
jsonPrint(imageOcrAPI(IMAGE_TEXT_OFFENSIVE_2))

# Wait 1 second (to avoid API rate limit)
time.sleep(1)

print(f"Image Screening 5: Suggestive (Bikini Model):")
jsonPrint(imageEvalAPI(IMAGE_SUGGESTIVE_1))

# Wait 1 second (to avoid API rate limit)
time.sleep(1)

print(f"Image Screening 6: Suggestive (Couple Makeout):")
jsonPrint(imageEvalAPI(IMAGE_SUGGESTIVE_2))

# Wait 1 second (to avoid API rate limit)
time.sleep(1)

print(f"Image Screening 7: Adult (70's Playboy Centerfold):")
jsonPrint(imageEvalAPI(IMAGE_ADULT_1))

# Wait 1 second (to avoid API rate limit)
time.sleep(1)

print(f"Image Screening 8: Adult (Topless, Bed):")
jsonPrint(imageEvalAPI(IMAGE_ADULT_2))

# Wait 1 second (to avoid API rate limit)
time.sleep(1)

print(f"Image Screening 9: Gory (Movie):")
jsonPrint(imageEvalAPI(IMAGE_GORY_1))

# Wait 1 second (to avoid API rate limit)
time.sleep(1)

print(f"Image Screening 10: gory (War):")
jsonPrint(imageEvalAPI(IMAGE_GORY_2))