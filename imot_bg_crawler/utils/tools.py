from bs4 import BeautifulSoup


def get_html_tag_text(text):
    try:
        soup = BeautifulSoup(text, parser='html.parser')
    except (TypeError, AttributeError):
        return ''
    return soup.get_text()
