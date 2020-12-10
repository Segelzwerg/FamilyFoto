from flask_api import status
from lxml import html


# Assertion should look like junit assertions
# pylint: disable = invalid-name
def assertImageIsLoaded(test_case, response):
    """
    Asserts if the images is loaded in the response.
    :param test_case: from which the assertion is called.
    :param response: response to check for image
    """
    html_content = html.fromstring(response.data.decode('utf-8'))
    image = html_content.xpath('//img')[0].attrib['src']
    response = test_case.client.get(image)
    message = f'The image resource could not be loaded: {image}'
    test_case.assertEqual(status.HTTP_200_OK, response.status_code, msg=message)


def assertPublicSharing(test_case, value):
    """
    Asserts if the status flag has the value.
    :param test_case: from which the assertion is called.
    :param value: of the public sharing attribute
    """
    response = test_case.client.get(f'/image/{test_case.photo.hash}')
    html_content = html.fromstring(response.data.decode('utf-8'))
    inputs = html_content.xpath('//input')
    public_share = list(filter(lambda x: x.attrib['id'] == 'public', inputs))[0]
    test_case.assertEqual(value, public_share.attrib['value'])
