import backoff
import requests
from requests.exceptions import ConnectionError
from singer import metrics, utils
import singer

LOGGER = singer.get_logger()


class Server5xxError(Exception):
    pass


class Server429Error(Exception):
    pass


class ImpactError(Exception):
    pass


class ImpactBadRequestError(ImpactError):
    pass


class ImpactUnauthorizedError(ImpactError):
    pass


class ImpactRequestFailedError(ImpactError):
    pass


class ImpactNotFoundError(ImpactError):
    pass


class ImpactMethodNotAllowedError(ImpactError):
    pass


class ImpactConflictError(ImpactError):
    pass


class ImpactForbiddenError(ImpactError):
    pass


class ImpactUnprocessableEntityError(ImpactError):
    pass


class ImpactInternalServiceError(ImpactError):
    pass

class ImpactUnknownError(ImpactError):
    pass

ERROR_CODE_EXCEPTION_MAPPING = {
    400: ImpactBadRequestError,
    401: ImpactUnauthorizedError,
    402: ImpactRequestFailedError,
    403: ImpactForbiddenError,
    404: ImpactNotFoundError,
    405: ImpactMethodNotAllowedError,
    409: ImpactConflictError,
    422: ImpactUnprocessableEntityError,
    500: ImpactInternalServiceError,
    520: ImpactUnknownError}


def get_exception_for_error_code(error_code):
    return ERROR_CODE_EXCEPTION_MAPPING.get(error_code, ImpactError)

def raise_for_error(response):
    LOGGER.error('ERROR {}: {}, REASON: {}'.format(response.status_code,\
        response.text, response.reason))
    try:
        response.raise_for_status()
    except (requests.HTTPError, requests.ConnectionError) as error:
        try:
            content_length = len(response.content)
            if content_length == 0:
                # There is nothing we can do here since Impact has neither sent
                # us a 2xx response nor a response content.
                return
            response = response.json()
            if ('error' in response) or ('errorCode' in response):
                message = '%s: %s' % (response.get('error', str(error)),
                                      response.get('message', 'Unknown Error'))
                error_code = response.get('status')
                ex = get_exception_for_error_code(error_code)
                raise ex(message)
            else:
                raise ImpactError(error)
        except (ValueError, TypeError):
            raise ImpactError(error)


class ImpactClient(object):
    def __init__(self,
                 account_sid,
                 auth_token,
                 api_catalog,
                 user_agent=None):
        self.__account_sid = account_sid
        self.__auth_token = auth_token
        self.__api_catalog = api_catalog
        base_url = "https://api.impact.com/{}/{}".format(api_catalog, account_sid)
        self.base_url = base_url
        self.__user_agent = user_agent
        self.__session = requests.Session()
        self.__verified = False

    def __enter__(self):
        self.__verified = self.check_access()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.__session.close()

    @backoff.on_exception(backoff.expo,
                          Server5xxError,
                          max_tries=7,
                          factor=3)
    def check_access(self):
        if self.__account_sid is None or self.__auth_token is None:
            raise Exception('Error: Missing account_sid or auth_token in config.json.')
        if self.__account_sid is None:
            raise Exception('Error: Missing account_sid in cofig.json.')
        if self.__api_catalog is None:
            raise Exception('Error: Missing api_catalog in cofig.json.')
        headers = {}
        # Endpoint: simple API call to return a single record (CompanyInformation) to test access
        # https://developer.impact.com/default/documentation/Rest-Adv-v8#operations-Company_Information-GetCompanyInfo
        endpoint = 'CompanyInformation'
        url = '{}/{}.json'.format(self.base_url, endpoint)
        if self.__user_agent:
            headers['User-Agent'] = self.__user_agent
        headers['Accept'] = 'application/json'
        response = self.__session.get(
            url=url,
            headers=headers,
            # Basic Authentication:
            # https://developer.impact.com/default/guides/request-authentication
            auth=(self.__account_sid, self.__auth_token))
        if response.status_code != 200:
            LOGGER.error('Error status_code = {}'.format(response.status_code))
            raise_for_error(response)
        else:
            return True


    @backoff.on_exception(backoff.expo,
                          (Server5xxError, ConnectionError, Server429Error),
                          max_tries=7,
                          factor=3)
    # Rate Limiting: https://developer.impact.com/default/guides/rate-limiting
    @utils.ratelimit(1000, 3600)
    def request(self, method, path=None, url=None, json=None, version=None, **kwargs):
        if not self.__verified:
            self.__verified = self.check_access()

        if not version:
            version = 'v2'

        if not url and path:
            url = '{}/{}.json'.format(self.base_url, path)

        if 'endpoint' in kwargs:
            endpoint = kwargs['endpoint']
            del kwargs['endpoint']
        else:
            endpoint = None

        if 'headers' not in kwargs:
            kwargs['headers'] = {}

        kwargs['headers']['Accept'] = 'application/json'

        if self.__user_agent:
            kwargs['headers']['User-Agent'] = self.__user_agent

        if method == 'POST':
            kwargs['headers']['Content-Type'] = 'application/json'

        with metrics.http_request_timer(endpoint) as timer:
            response = self.__session.request(
                method=method,
                url=url,
                # Basic Authentication:
                # https://developer.impact.com/default/guides/request-authentication
                auth=(self.__account_sid, self.__auth_token),
                json=json,
                **kwargs)
            timer.tags[metrics.Tag.http_status_code] = response.status_code

        if response.status_code >= 500:
            raise Server5xxError()

        if response.status_code != 200:
            raise_for_error(response)

        return response.json()

    def get(self, path, **kwargs):
        return self.request('GET', path=path, **kwargs)

    def post(self, path, **kwargs):
        return self.request('POST', path=path, **kwargs)
