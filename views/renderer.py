from jinja2 import Environment, FileSystemLoader, select_autoescape
from fastapi.responses import HTMLResponse

_env = Environment(
    loader=FileSystemLoader("views/templates"),
    autoescape=select_autoescape(["html", "xml"]),
)

def render(template: str, **context) -> HTMLResponse:
    html = _env.get_template(template).render(**context)
    return HTMLResponse(html)