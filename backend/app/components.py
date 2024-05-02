from jinjax.catalog import Catalog
from markupsafe import Markup


class CustomCatalog(Catalog):
    # Patching Catalog library to recognize "/" as a absolute path
    def render_assets(self, fingerprint: bool = False) -> str:
        html_css = []
        for url in self.collected_css:
            if not url.startswith(("http://", "https://", "/")):
                url = f"{self.root_url}{url}"
            html_css.append(f'<link rel="stylesheet" href="{url}">')

        html_js = []
        for url in self.collected_js:
            if not url.startswith(("http://", "https://", "/")):
                url = f"{self.root_url}{url}"
            html_js.append(f'<script type="module" src="{url}"></script>')

        return Markup("\n".join(html_css + html_js))


catalog = CustomCatalog()
catalog.add_folder("backend/components/")
