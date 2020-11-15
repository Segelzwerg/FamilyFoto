from flask_api import status
from lxml import html


def assertImageIsLoaded(test_case, filename):
    response = test_case.client.get(f'/image/{filename}')
    html_content = html.fromstring(response.data.decode('utf-8'))
    image = html_content.xpath('//img')[0].attrib['src']
    response = test_case.client.get(image)
    message = f'The image resource could not be loaded: {image}'
    test_case.assertEqual(status.HTTP_200_OK, response.status_code, msg=message)