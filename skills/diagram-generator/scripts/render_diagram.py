#!/usr/bin/env python3
"""
Reusable HTML-to-PNG renderer using Playwright.

Renders an HTML template to a high-DPI PNG screenshot, optionally injecting
logo images via JavaScript. Used by the diagram-generator skill.

Usage:
    python render_diagram.py --template path/to.html --output path/to.png
    python render_diagram.py --template path/to.html --output path/to.png \
        --width 1080 --height 1350 --scale 4 \
        --header-icon path/to/icon.png --footer-logo path/to/logo.png

Dependencies:
    pip install playwright
    python -m playwright install chromium
"""

import argparse
from pathlib import Path
from playwright.sync_api import sync_playwright


def render(
    template: Path,
    output: Path,
    width: int = 1080,
    height: int = 1350,
    scale: int = 4,
    selector: str = ".card",
    header_icon: Path | None = None,
    footer_logo: Path | None = None,
    wait_ms: int = 1200,
):
    """Render an HTML template to a high-DPI PNG via Playwright."""
    template = template.resolve()
    output = output.resolve()
    if header_icon:
        header_icon = header_icon.resolve()
    if footer_logo:
        footer_logo = footer_logo.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(
            viewport={"width": width, "height": height},
            device_scale_factor=scale,
        )
        page = context.new_page()
        page.goto(template.as_uri(), wait_until="networkidle")
        page.emulate_media(media="screen")

        # Inject logo images if provided
        inject_data = {}
        if header_icon and header_icon.exists():
            inject_data["header_icon_url"] = header_icon.as_uri()
        if footer_logo and footer_logo.exists():
            inject_data["footer_logo_url"] = footer_logo.as_uri()

        if inject_data:
            page.evaluate(
                """(data) => {
                    if (data.header_icon_url) {
                        const img = document.getElementById('header-icon-img');
                        if (img) img.src = data.header_icon_url;
                    }
                    if (data.footer_logo_url) {
                        const container = document.getElementById('footer-logo');
                        if (container) {
                            container.innerHTML = '';
                            const img = document.createElement('img');
                            img.src = data.footer_logo_url;
                            img.style.height = '100%';
                            img.style.objectFit = 'contain';
                            container.appendChild(img);
                        }
                    }
                }""",
                inject_data,
            )

        page.wait_for_timeout(wait_ms)

        # Screenshot the target element or full page
        card = page.query_selector(selector)
        if card:
            card.screenshot(path=str(output))
        else:
            page.screenshot(path=str(output), full_page=True)

        try:
            context.close()
        finally:
            browser.close()

    size_kb = output.stat().st_size / 1024
    print(f"Saved: {output} ({size_kb:.0f} KB)")


def main():
    parser = argparse.ArgumentParser(
        description="Render an HTML template to a high-DPI PNG via Playwright"
    )
    parser.add_argument("--template", required=True, type=Path, help="HTML template path")
    parser.add_argument("--output", required=True, type=Path, help="Output PNG path")
    parser.add_argument("--width", type=int, default=1080, help="Viewport width (default: 1080)")
    parser.add_argument("--height", type=int, default=1350, help="Viewport height (default: 1350)")
    parser.add_argument("--scale", type=int, default=4, help="Device scale factor (default: 4)")
    parser.add_argument("--selector", default=".card", help="CSS selector to screenshot (default: .card)")
    parser.add_argument("--header-icon", type=Path, default=None, help="Header icon image path")
    parser.add_argument("--footer-logo", type=Path, default=None, help="Footer logo image path")
    parser.add_argument("--wait", type=int, default=1200, help="Wait ms for fonts/images (default: 1200)")
    args = parser.parse_args()

    render(
        template=args.template,
        output=args.output,
        width=args.width,
        height=args.height,
        scale=args.scale,
        selector=args.selector,
        header_icon=args.header_icon,
        footer_logo=args.footer_logo,
        wait_ms=args.wait,
    )


if __name__ == "__main__":
    main()
