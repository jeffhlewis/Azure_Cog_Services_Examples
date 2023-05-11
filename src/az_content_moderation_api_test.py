""" Script that contains a series of tests for the Azure Content Moderation Cognitive Service """
import json
import time
import requests

# -----=====-----=====-----=====-----=====-----=====-----=====-----=====
# Settings and endpoints
# -----=====-----=====-----=====-----=====-----=====-----=====-----=====
API_KEY                  = "<API KEY>"
API_BASE                 = "https://<SUBDOMAIN>.cognitiveservices.azure.com/"
API_ENDPOINT_TEXT_SCREEN = f"{API_BASE}contentmoderator/moderate/v1.0/ProcessText/Screen"
API_ENDPOINT_IMAGE_OCR   = f"{API_BASE}contentmoderator/moderate/v1.0/ProcessImage/OCR"
API_ENDPOINT_IMAGE_EVAL  = f"{API_BASE}contentmoderator/moderate/v1.0/ProcessImage/Evaluate"
API_TIMEOUT_SECS         = 10

# -----=====-----=====-----=====-----=====-----=====-----=====-----=====
# Test Image URLs
# -----=====-----=====-----=====-----=====-----=====-----=====-----=====
test_urls = {
    "IMAGE_CONTROL_ART"      : "https://as2.ftcdn.net/v2/jpg/05/21/18/03/1000_F_521180377_2iAVJqBQSo3cgKaVp8vMBR8asrC61DoU.jpg",
    "IMAGE_CONTROL_PEOPLE"   : "https://as2.ftcdn.net/v2/jpg/01/06/10/25/1000_F_106102543_8BpQIq6FmY72hMt4ZGArWYMKneLwl5aj.jpg",
    "IMAGE_TEXT_OFFENSIVE_1" : "https://i.etsystatic.com/32805953/r/il/7b73d7/3819750348/il_794xN.3819750348_lhmt.jpg",
    "IMAGE_TEXT_OFFENSIVE_2" : "https://i.kym-cdn.com/photos/images/newsfeed/001/152/678/242.jpg",
    "IMAGE_SUGGESTIVE_1"     : "https://e00-marca.uecdn.es/assets/multimedia/imagenes/2022/11/04/16675708619484.jpg",
    "IMAGE_SUGGESTIVE_2"     : "https://as2.ftcdn.net/v2/jpg/00/97/38/77/1000_F_97387751_My3G68BPBgf8Mte9ncDZhbTPQu3i5pNI.jpg",
    "IMAGE_ADULT_1"          : "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRIoCiibUXdGXPd8_ZYdmMDx0Gb-pdn2EgGLQ&usqp=CAU",
    "IMAGE_ADULT_2"          : "https://ftopx.com/large/201202/29188.jpg",
    "IMAGE_GORY_1"           : "https://bloody-disgusting.com/wp-content/uploads/2021/07/THE-SADNESS.jpg",
    "IMAGE_GORY_2"           : "https://media.wbur.org/wp/2017/03/1111_vietnam01-1-1000x735.jpg"
}

# -----=====-----=====-----=====-----=====-----=====-----=====-----=====
# Functions
# -----=====-----=====-----=====-----=====-----=====-----=====-----=====
def json_print(json_string):
    """Pretty-prints a JSON string to console

    Args:
        jsonString (str): The JSOn string you wish to print
    """
    print(json.dumps(json_string, indent=2))

def text_screen_api(content):
    """Calls the Azure Content Moderation Text Screen API

    Default Categories:
        * Category 1: language that may be considered sexually explicit or adult
        * Category 2: language that may be considered sexually suggestive or mature
        * Category 3: language that may be considered offensive

    Args:
        content (str): a text string you wish to screen for content

    Returns:
        JSON-encoded API response
    """
    request_url = API_ENDPOINT_TEXT_SCREEN
    request_data = content
    request_headers = {
        "Content-Type"  : "text/plain",
        "Ocp-Apim-Subscription-Key" : API_KEY
    }
    request_params = {
        "autocorrect": True,
        "PII" : True,
        "classify" : True,
        "language" : "eng"
    }
    response = requests.post(
        url = request_url,
        data = request_data,
        headers = request_headers,
        params = request_params,
        timeout = API_TIMEOUT_SECS)
    return response.json()

def image_ocr_api(image_url):
    """Calls the Azure Content Moderation Image OCR API

    Args:
        imageUrl (str): URL to an image you wish to run the Image OCR API against

    Returns:
        JSON-encoded API response
    """
    request_url = API_ENDPOINT_IMAGE_OCR
    request_data = json.dumps({
        "DataRepresentation": "URL",
        "Value": image_url
    })
    request_headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": API_KEY
    }
    request_params = {
        "language": "eng",
        "enhanced" : True
    }
    response = requests.post(
        url = request_url,
        data = request_data,
        headers = request_headers,
        params = request_params,
        timeout = API_TIMEOUT_SECS
    )
    return response.json()

def image_eval_api(image_url):
    """Calls the Azure Content Moderation Image Evaluate API

    Args:
        imageUrl (str): URL to an image you wish to run the Image Evaluate API against

    Returns:
        JSON-encoded API response
    """
    request_url = API_ENDPOINT_IMAGE_EVAL
    request_data = json.dumps({
        "DataRepresentation": "URL",
        "Value": image_url
    })
    request_headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": API_KEY
    }
    request_params = {}
    response = requests.post(
        url = request_url,
        data = request_data,
        headers = request_headers,
        params = request_params,
        timeout = API_TIMEOUT_SECS
    )
    return response.json()

def main():
    """Main function - makes all API calls"""

    text_to_screen = "Testing this lovely API and gathering results"
    print(f"Text Screening 1: Control [{text_to_screen}]")
    json_print(text_screen_api(text_to_screen))

    # Wait 1 second (to avoid API rate limit)
    time.sleep(1)

    text_to_screen = "Testing this fucking API and shit"
    print(f"Text Screening 2: Offensive Text [{text_to_screen}]:")
    json_print(text_screen_api(text_to_screen))

    # Wait 1 second (to avoid API rate limit)
    time.sleep(1)

    print("Image Screening 1: Control (Art):")
    json_print(image_eval_api(test_urls["IMAGE_CONTROL_ART"]))

    # Wait 1 second (to avoid API rate limit)
    time.sleep(1)

    print("Image Screening 2: Control (People):")
    json_print(image_eval_api(test_urls["IMAGE_CONTROL_PEOPLE"]))

    # Wait 1 second (to avoid API rate limit)
    time.sleep(1)

    print("Image Screening 3: Offensive Text OCR (C-word):")
    json_print(image_ocr_api(test_urls["IMAGE_TEXT_OFFENSIVE_1"]))

    # Wait 1 second (to avoid API rate limit)
    time.sleep(1)

    print("Image Screening 4: Offensive Text OCR (F-word):")
    json_print(image_ocr_api(test_urls["IMAGE_TEXT_OFFENSIVE_2"]))

    # Wait 1 second (to avoid API rate limit)
    time.sleep(1)

    print("Image Screening 5: Suggestive (Bikini Model):")
    json_print(image_eval_api(test_urls["IMAGE_SUGGESTIVE_1"]))

    # Wait 1 second (to avoid API rate limit)
    time.sleep(1)

    print("Image Screening 6: Suggestive (Couple Makeout):")
    json_print(image_eval_api(test_urls["IMAGE_SUGGESTIVE_2"]))

    # Wait 1 second (to avoid API rate limit)
    time.sleep(1)

    print("Image Screening 7: Adult (70's Playboy Centerfold):")
    json_print(image_eval_api(test_urls["IMAGE_ADULT_1"]))

    # Wait 1 second (to avoid API rate limit)
    time.sleep(1)

    print("Image Screening 8: Adult (Topless, Bed):")
    json_print(image_eval_api(test_urls["IMAGE_ADULT_2"]))

    # Wait 1 second (to avoid API rate limit)
    time.sleep(1)

    print("Image Screening 9: Gory (Movie):")
    json_print(image_eval_api(test_urls["IMAGE_GORY_1"]))

    # Wait 1 second (to avoid API rate limit)
    time.sleep(1)

    print("Image Screening 10: gory (War):")
    json_print(image_eval_api(test_urls["IMAGE_GORY_2"]))

# -----=====-----=====-----=====-----=====-----=====-----=====-----=====
# Main
# -----=====-----=====-----=====-----=====-----=====-----=====-----=====
if __name__ == '__main__':
    main()
