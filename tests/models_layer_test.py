from mfdballm.models.tool_result import ToolResult
from mfdballm.models.provider_response import ProviderResponse


def main():

    r = ToolResult('echo','hello',True)

    p = ProviderResponse(text='ok')

    assert r.success

    assert p.text == 'ok'

    print('MODELS LAYER TEST PASSED')


if __name__ == '__main__':

    main()
