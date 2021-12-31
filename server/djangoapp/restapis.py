#from os import error
import requests
import os
import datetime
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from .classes.cloudrequests import CloudRequestException
from djangoapp.models import CarDealer
from dotenv import load_dotenv
load_dotenv()



SENTIMENT_URL = os.environ.get("SENTIMENT_URL")
NLU_VERSION = os.environ.get("NLU_VERSION")




def get_dealers_from_cf(url, session_object, cloud_request_instance):
    """
    It send a get request to the endpoint via CloudRequest instance for get a list of dealers.    
    """
    result = dict()
    result["message"] = None
    result["list"] = None
    result["error"] = None
    try:

        car_dealer_list = []
        respond = cloud_request_instance.get_request(url, session_object)
        print(respond)

        respond_docs = respond["docs"]
        result["message"] = respond["message"]

        for doc in respond_docs:
            dealer = doc["doc"]
            dealer_obj = CarDealer(
                id=dealer["id"] if dealer.get("id") and dealer["id"] else None,
                city=dealer["city"] if dealer.get("city") and dealer["city"] else None,
                state=dealer["state"] if dealer.get("state") and dealer["state"] else None,
                st=dealer["st"] if dealer.get("st") and dealer["st"] else None,
                address=dealer["address"] if dealer.get("address") and dealer["address"] else None,
                adr_zip=dealer["zip"] if dealer.get("zip") and dealer["zip"] else None,
                lat=dealer["lat"] if dealer.get("lat") and dealer["lat"] else None,
                long=dealer["long"] if dealer.get("long") and dealer["long"] else None,
                short_name=dealer["short_name"] if dealer.get("short_name") and dealer["short_name"] else None,
                full_name=dealer["full_name"] if dealer.get("full_name") and dealer["full_name"] else None)
            car_dealer_list.append(dealer_obj)
        result["list"] = car_dealer_list
        return result
    except requests.HTTPError as ht:
        print(repr(ht))
        result["error"] = str(repr(ht))
        result["message"] = "Not Found the requested URL"
        return result
    except CloudRequestException as cl:
        print(repr(cl))
        result["error"] = str(repr(cl.error))
        result["message"] = cl.message
        return result
    except KeyError as ke:
        print(repr(ke))
        result["error"] = str(repr(ke))
        result["message"] = "Sorry,error occurred on the server"
        return result
    except Exception as ex:
        print(repr(ex))
        result["error"] = str(repr(ex))
        result["message"] = "Sorry,error occurred on the server"
        return result


def get_dealer_reviews_from_cf(
        url,
        session_object,
        cloud_request_instance,
        **kvargs):
    """
    It send a get request to the endpoint via CloudRequest instance for get a review about a dealer by dealerId.    
    """
    result = dict()
    result["message"] = None
    result["list"] = None
    result["error"] = None
    try:
        review_list = []
        respond = cloud_request_instance.get_request(
            url, session_object, **kvargs)

        params = dict()
        params["version"] = NLU_VERSION
        params["features"] = "sentiment"
        params["return_analyzed_text"] = False
        params["language"] = 'en'

        respond_docs = respond["docs"]
        result["message"] = respond["message"]
        print(respond["message"])
        for doc in respond_docs:
            params["text"] = doc["review"]
            sentiment = analyze_review_sentiments(
                SENTIMENT_URL,
                session_object=session_object,
                cloud_request_instance=cloud_request_instance,
                params=params)
            dealer_review_object = DealerReview(
                dealership=doc["dealership"] if doc.get("dealership") and doc["dealership"] else None,
                name=doc["name"] if doc.get("name") and doc["name"] else None,
                purchase=doc["purchase"] if doc.get("purchase") and doc["purchase"] else None,
                review=doc["review"] if doc.get("review") and doc["review"] else None,
                review_date=doc["review_date"] if doc.get("review_date") and doc["review_date"] else None,
                purchase_date=doc["purchase_date"] if doc.get("purchase_date") and doc["purchase_date"] else None,
                car_make=doc["car_make"] if doc.get("purchase_date") and doc["purchase_date"] else None,
                car_model=doc["car_model"] if doc.get("car_model") and doc["car_model"] else None,
                car_year=doc["car_year"] if doc.get("car_year") and doc["car_year"] else None,
                sentiment=sentiment if sentiment else "N/A",
                id=doc["id"] if doc.get("id") and doc["id"] else None)
            review_list.append(dealer_review_object)
        result["list"] = review_list
        return result
    except requests.HTTPError as ht:
        print(repr(ht))
        result["error"] = str(repr(ht))
        result["message"] = "Not Found the requested URL"
        return result
    except CloudRequestException as cl:
        print(repr(cl))
        result["error"] = str(repr(cl.error))
        result["message"] = cl.message
        return result
    except KeyError as ke:
        print(repr(ke))
        result["error"] = str(repr(ke))
        result["message"] = "Sorry,error occurred on the server"
        return result
    except Exception as ex:
        print(repr(ex))
        result["error"] = str(repr(ex))
        result["message"] = "Sorry,error occurred on the server"
        return result


def analyze_review_sentiments(
        url,
        session_object,
        cloud_request_instance,
        **kvargs):
    """
    It send a get request to the IBM NLU endpoint via CloudRequest instance for get the sentiment of the  text
    """ 
    try:
        respond = cloud_request_instance.get_request(
            url, session_object, **kvargs)
        return respond["sentiment"]["document"]["label"]
    except KeyError as keyErr:
        print(keyErr)
        raise keyErr
    except Exception as ex:
        print(ex)
        raise ex


def add_review(url, session_object, cloud_request_instance, **kvargs):
    """
It send a post request to the endpoint via CloudRequest instance for saving a review to Cloudant.
    """
    result = dict()
    result["message"] = None
    result["datas"] = None
    result["error"] = None
    try:
        respond = cloud_request_instance.post_request(
            url, session_object, **kvargs)
        print(respond)
        result["datas"] = respond["datas"]
        result["message"] = respond["message"]
        return result
    except requests.HTTPError as ht:
        print(repr(ht))
        result["error"] = str(repr(ht))
        result["message"] = "Not Found the requested URL"
        return result
    except CloudRequestException as cl:
        print(repr(cl))
        result["error"] = str(repr(cl.error))
        result["message"] = cl.message
        return result
    except KeyError as ke:
        print(repr(ke))
        result["error"] = str(repr(ke))
        result["message"] = "Sorry, error occurred on the server"
        return result
    except Exception as ex:
        print(repr(ex))
        result["error"] = str(repr(ex))
        result["message"] = "Sorry, error occurred on the server"
        return result


#with requests.Session() as session:
#    get_from_cl = CloudRequest()
#    with open('../../functions/sample/python/test_review.json') as test_file:
#        r = json.load(test_file)
#
#        pl = dict()
#        pl = r["review"]
#        pl["rev_date"] =datetime.datetime.utcnow().isoformat()
#        print('++++++++',pl["rev_date"])
#
#    add_review(REVIEW_URL, session, get_from_cl, params=pl)
#    get_from_cl.post_request_result_body(REVIEW_URL, session, pl )
#    get_from_cl = CloudRequest()
#    dealerreview = 'Good morning'
#    auth=HTTPBasicAuth('apikey', SENTIMENT_API_KEY)
#    print(str(auth))
#    print(NLU_VERSION)
#    params = dict()
#    params["text"] = dealerreview
#    params["version"] = NLU_VERSION
#    params["features"] = "sentiment"
#    params["return_analyzed_text"] = False
#    params["language"] = 'en'
#    print(SENTIMENT_URL)
#    session.auth = auth
#    analyze_review_sentiments( SENTIMENT_URL, session, get_from_cl, params=params )
#    get_dealers_from_cf(GET_DEALERSHIPS_URL, session, get_from_cl)
#    analyze_review_sentiments( SENTIMENT_URL, session, get_from_cl, params=params )
#    res = get_dealer_reviews_from_cf(REVIEW_URL, session, get_from_cl, dealerId=23)
    # print(res)
#    with open('../../functions/sample/python/test_review.json') as test_file:
#        r = json.load(test_file)
#
#        pl = dict()
#        pl= r["review"]
#    get_from_cl.post_request_result_body(REVIEW_URL, session, pl )
#    get_from_cl.get_request(REVIEW_URL, session, dealerId=23 )
#    get_from_cl.get_request(REVIEW_URL, session, dealerId=2 )


#get_from_cl.get_request_body(GET_DEALERSHIPS_BY_STATE_URL, state='CAs')
# with open('../../functions/sample/python/test_review.json') as test_file:
#    r = json.load(test_file)
#
#    pl = dict()
#    pl= r["review"]
#    get_from_cl.post_request_result_body(REVIEW_URL,data=pl)
# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
