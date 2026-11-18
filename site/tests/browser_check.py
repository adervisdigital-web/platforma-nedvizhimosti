"""Открывает страницу в headless Chrome и печатает ошибки JS и ключевые счётчики. py -3 site/tests/browser_check.py <url>"""
import sys, os, json, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'tools'))
from cdp import Browser
url = sys.argv[1]
b = Browser()
b.call('Page.addScriptToEvaluateOnNewDocument', source='window.__e=[];addEventListener("error",e=>__e.push(e.message+" @"+(e.filename||"").split("/").pop()+":"+e.lineno));')
b.open(url, wait=3)
r = b.ev('JSON.stringify({err: window.__e, pn: typeof PN, items: typeof ITEMS !== "undefined" ? ITEMS.length : -1, cards: document.querySelectorAll(".card").length, houses: document.querySelectorAll(".hc").length, title: document.title})')
print(r); b.close()
