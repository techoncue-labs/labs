#!/usr/bin/env python3
"""Made-up documents for trying Paperless-ngx (all companies, people and amounts are fictional).

Writes HTML files to ./samples_html and, if Chromium or Google Chrome is installed,
prints each one to a PDF in ./samples. Otherwise open the HTML files in a browser
and use Print > Save as PDF.

Usage: python3 make_samples.py
"""
import shutil
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
H = HERE / "samples_html"
OUT = HERE / "samples"

CSS = """body{font-family:'DejaVu Sans',Arial,sans-serif;margin:48px 56px;color:#222;font-size:14px}
h1{font-size:26px;margin:0}.top{display:flex;justify-content:space-between;align-items:flex-start;border-bottom:3px solid %s;padding-bottom:14px}
.logo{font-size:24px;font-weight:bold;color:%s}.small{color:#666;font-size:12px}table{width:100%%;border-collapse:collapse;margin-top:24px}
td,th{border-bottom:1px solid #ddd;padding:8px;text-align:left}th{background:#f4f4f4}.r{text-align:right}.tot{font-weight:bold;font-size:16px}
.box{margin-top:26px;padding:14px;background:#f7f7f7;border-left:4px solid %s}.addr{margin-top:26px;line-height:1.5}"""


def page(color, brand, sub, title, meta, body):
    return (f"<html><head><meta charset='utf-8'><style>{CSS % (color, color, color)}</style></head><body>"
            f"<div class='top'><div><div class='logo'>{brand}</div><div class='small'>{sub}</div></div>"
            f"<div style='text-align:right'><h1>{title}</h1><div class='small'>{meta}</div></div></div>"
            f"<div class='addr'>Alex Sample<br>12 Example Road<br>Springfield 01234</div>{body}"
            f"<p class='small' style='margin-top:40px'>This is a made-up sample document for a tutorial. "
            f"All names, companies and amounts are fictional.</p></body></html>")


def rows(items):
    return ("<table><tr><th>Description</th><th class='r'>Amount</th></tr>"
            + "".join(f"<tr><td>{a}</td><td class='r'>{b}</td></tr>" for a, b in items) + "</table>")


D = {
    "brightwater-invoice-october.html": page("#1677c9", "Brightwater Utilities", "Electricity and water for Springfield", "INVOICE",
        "Invoice number BW-10422<br>Date: 3 October 2026",
        rows([("Electricity, September 2026 (312 kWh)", "$71.40"), ("Water service, September 2026", "$12.80"),
              ("<b>Total due by 24 October 2026</b>", "<b>$84.20</b>")])
        + "<div class='box'>Pay online or by bank transfer. Customer number 558-201.</div>"),
    "pinecrest-internet-bill.html": page("#2e9e5b", "Pinecrest Internet", "Fibre broadband", "INVOICE",
        "Invoice number PC-77310<br>Date: 1 October 2026",
        rows([("Fibre 500 plan, October 2026", "$45.00"), ("Router rental", "$5.00"), ("<b>Total</b>", "<b>$50.00</b>")])
        + "<div class='box'>Your plan renews monthly. Thank you for being a customer.</div>"),
    "maple-street-hardware-receipt.html": page("#c0392b", "Maple Street Hardware", "Tools, paint and garden", "RECEIPT",
        "Receipt 004-19876<br>Date: 18 October 2026",
        rows([("Interior paint, white, 5 litres", "$38.90"), ("Paint brushes, set of 3", "$9.50"), ("Masking tape", "$3.20"),
              ("<b>Total paid by card</b>", "<b>$51.60</b>")])),
    "riverside-dental-letter.html": page("#8e44ad", "Riverside Dental", "Family dental care", "APPOINTMENT", "Date: 20 October 2026",
        "<p style='margin-top:26px'>Dear Alex,</p><p>This is a friendly reminder of your check-up appointment on "
        "<b>Tuesday 17 November 2026 at 9:30</b> with Dr. Lane.</p><p>Please arrive ten minutes early. If you need to "
        "change the time, call the front desk.</p><p>Kind regards,<br>Riverside Dental</p>"),
    "harborline-insurance-renewal.html": page("#d35400", "Harborline Insurance", "Car and home insurance", "RENEWAL NOTICE",
        "Policy HL-3390-C<br>Date: 12 October 2026",
        "<p style='margin-top:26px'>Your car insurance policy renews on <b>1 December 2026</b>.</p>"
        + rows([("Comprehensive cover, 12 months", "$612.00"), ("Roadside assistance", "$48.00"), ("<b>Yearly premium</b>", "<b>$660.00</b>")])
        + "<div class='box'>No action is needed if you want to keep the same cover.</div>"),
    "pinecrest-internet-bill-november.html": page("#2e9e5b", "Pinecrest Internet", "Fibre broadband", "INVOICE",
        "Invoice number PC-80544<br>Date: 1 November 2026",
        rows([("Fibre 500 plan, November 2026", "$45.00"), ("Router rental", "$5.00"), ("<b>Total</b>", "<b>$50.00</b>")])
        + "<div class='box'>Your plan renews monthly. Thank you for being a customer.</div>"),
    "brightwater-invoice-november.html": page("#1677c9", "Brightwater Utilities", "Electricity and water for Springfield", "INVOICE",
        "Invoice number BW-11087<br>Date: 3 November 2026",
        rows([("Electricity, October 2026 (288 kWh)", "$65.90"), ("Water service, October 2026", "$12.80"),
              ("<b>Total due by 24 November 2026</b>", "<b>$78.70</b>")])
        + "<div class='box'>Pay online or by bank transfer. Customer number 558-201.</div>"),
}


def find_browser():
    for name in ("chromium", "chromium-browser", "google-chrome", "google-chrome-stable", "chrome"):
        path = shutil.which(name)
        if path:
            return path
    return None


def main():
    H.mkdir(exist_ok=True)
    for name, html in D.items():
        (H / name).write_text(html, encoding="utf-8")
    print(f"wrote {len(D)} HTML files to {H}")
    browser = find_browser()
    if not browser:
        print("No Chromium/Chrome found: open the HTML files in a browser and use Print > Save as PDF into ./samples")
        return
    OUT.mkdir(exist_ok=True)
    for name in D:
        pdf = OUT / name.replace(".html", ".pdf")
        subprocess.run([browser, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                        f"--print-to-pdf={pdf}", (H / name).as_uri()],
                       check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("ok" if pdf.exists() else "FAILED", pdf.name)


if __name__ == "__main__":
    main()
