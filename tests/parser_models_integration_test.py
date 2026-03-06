from mfdballm.models.provider_response import ProviderResponse
from mfdballm.parsers.action_parser import parse_provider_response


def main():

    r = ProviderResponse(text='hello')

    a = parse_provider_response(r)

    assert a.type.name == 'FINISH'

    print('PARSER MODELS TEST PASSED')


if __name__ == '__main__':

    main()
