"""Tests for plain_html functions."""
from bs4 import BeautifulSoup
from ..readabilipy import plain_html, text_manipulation


def test_remove_metadata():
    html = """
        <!DOCTYPE html>
        <html>
        <head></head>
        <body>
        <!-- Comment here -->
        </body>
        </html>
    """
    soup = BeautifulSoup(html, "html5lib")
    plain_html.remove_metadata(soup)
    assert "<!-- Comment here -->" not in str(soup)


def test_remove_blacklist():
    html = """
        <html>
        <body>
            <button type="button">Click Me!</button>
            <p>Hello</p>
        <body>
        </html>
    """
    soup = BeautifulSoup(html, "html5lib")
    plain_html.remove_blacklist(soup)
    assert "button" not in str(soup)


def test_remove_cdata():
    """Test all possible methods of CData inclusion. Note that in the final
    example the '//' prefixes have no effect (since we are not in a <script>)
    tag and so we expect that the first will be displayed (tested in Chrome and
    Safari)."""
    html = """
        <div>
            <p>Some text <![CDATA[Text inside two tags]]></p>
            <![CDATA[Text inside one tag]]>
        </div>
        <![CDATA[Text outside tags]]>
        <script type="text/javascript">
            //<![CDATA[
            document.write("<");
            //]]>
        </script>
        //<![CDATA[
            invalid CDATA block
        //]]>
    """.strip()
    parsed_html = str(plain_html.parse_to_tree(html))
    expected_output = "<div><p>Some text</p><p>//</p></div>"
    assert text_manipulation.simplify_html(parsed_html) == expected_output
