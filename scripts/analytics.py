"""Shared Google Analytics snippet for static pages."""

GTAG = """<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-R4B36501JF"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-R4B36501JF');
</script>
"""


def ensure_gtag(html: str) -> str:
    if "G-R4B36501JF" in html:
        return html
    if "<head>" in html:
        return html.replace("<head>", "<head>\n" + GTAG, 1)
    return html
