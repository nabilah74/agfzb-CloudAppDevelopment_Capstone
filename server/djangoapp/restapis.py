import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    print(kwargs)
    print("Post from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.post(url, params=kwargs, json=json_payload)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list



# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(review):
    url = "https://api.us-south.natugiral-language-understanding.watson.cloud.ibm.com/instances/8dcd5f6d-d581-41d6-ac49-ef77b857d58e"
    myapikey = "wbh-f2wwqdjhVp5zUfl0fFANEHyXtFAQr_GFvELov8Ul"
    authenticator = IAMAuthenticator(myapikey)
    NLU = NaturalLanguageUnderstandingV1(
        version='2022-04-07',
        authenticator=authenticator)
    NLU.set_service_url(url)
    response = NLU.analyze(text=review,features=Features(sentiment=SentimentOptions())).get_result()
    return response["sentiment"]

def get_dealer_reviews_from_cf(url, dealerID):
    results = []
    json_result = get_request(url)
    print(json_result)
    print(json_result)
    print(json_result)
    if json_result:
        dealers = json_result["docs"]
        # For each dealer object
        for dealer in dealers["docs"]:
            sentiment = analyze_review_sentiments(dealer["review"])
            dealer_review_obj = DealerReview(dealership=dealer["dealership"], name=dealer["name"], purchase=dealer["purchase"],
                                   review=dealer["review"], purchase_date=dealer["purchase_date"], car_make=dealer["car_make"],
                                   car_model=dealer["car_model"],car_year=dealer["car_year"], id=dealer["id"],sentiment=sentiment)
            results.append(dealer_review_obj)
    return results