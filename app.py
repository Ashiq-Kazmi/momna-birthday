"""Five small chapters, made for Momna. Run: python -m streamlit run app.py"""

from __future__ import annotations

import base64
import html
from datetime import date
from pathlib import Path
try:
    import tomllib
except ModuleNotFoundError:  # Python 3.9 and 3.10
    import tomli as tomllib

import streamlit as st

ROOT = Path(__file__).resolve().parent
with (ROOT / "birthday.toml").open("rb") as f:
    CONFIG = tomllib.load(f)
NAME = CONFIG["recipient"]
FIRST = NAME.split()[0]
SENDER = CONFIG["sender"]
BIRTHDAY = date.fromisoformat(CONFIG["birthday"])
DATE_LABEL = f"{BIRTHDAY.day:02d} {BIRTHDAY:%B %Y}"

st.set_page_config(page_title=f"For {NAME} · Happy Birthday", page_icon="🎀", layout="wide")


def markup(value: str) -> None:
    # Dedent-free HTML prevents Markdown from treating indented cards as code.
    st.markdown(value, unsafe_allow_html=True)


@st.cache_data
def photo_uri() -> str:
    content = (ROOT / "assets" / "momna.jpeg").read_bytes()
    return "data:image/jpeg;base64," + base64.b64encode(content).decode("ascii")


def portrait(variant: str = "hero") -> None:
    styles = {"hero": "hero-photo", "polaroid": "polaroid-photo", "full": "full-photo"}
    style = styles.get(variant, "hero-photo")
    caption = "A little spotlight. All yours." if variant == "hero" else "The birthday girl · " + DATE_LABEL
    markup(f'<figure class="portrait-frame {style}"><div class="photo-inner">'
           f'<img src="{photo_uri()}" alt="Portrait of {html.escape(NAME)}" />'
           f'</div><figcaption>{html.escape(caption)}</figcaption>'
           '<span class="photo-sparkle" aria-hidden="true">✧</span></figure>')


def heading(chapter: str, title: str, subtitle: str) -> None:
    markup(f'<div class="chapter-heading"><p class="eyebrow">{chapter}</p>'
           f'<h1>{title}</h1><p class="lead">{subtitle}</p></div>')


def go(key: str) -> None:
    # Streamlit 1.50 ignores page-switch reruns inside widget callbacks.
    # Store the destination, then switch during the next normal script run.
    st.session_state["next_page"] = key


def next_button(key: str, label: str) -> None:
    st.button(label, key=f"continue_{key}", type="primary", width="stretch", on_click=go, args=(key,))


def change(key: str, value: object) -> None:
    st.session_state[key] = value


def celebrate() -> None:
    if st.session_state.get("animations", True):
        st.balloons()


def welcome() -> None:
    with st.container(key="welcome"):
        left, right = st.columns([1.18, 1], gap="large", vertical_alignment="center")
        with left:
            markup(f'<div class="hero-copy"><p class="eyebrow"><span class="tiny-star">✦</span> A DAY THAT BELONGS TO YOU</p>'
                   f'<h1>Happy<br>Birthday,<br><em>{html.escape(FIRST)}.</em></h1>'
                   '<p class="hero-description">A little corner of the internet,<br>made just to make you smile.</p>'
                   f'<div class="dedication"><span class="dedication-line"></span> FOR {html.escape(NAME.upper())} · WITH WARM WISHES</div></div>')
            with st.container(key="hero_actions"):
                next_button("spotlight", "Open your birthday surprise  →")
                markup('<p class="microcopy">Five little chapters. One very special you.</p>')
        with right:
            portrait()
            markup(f'<div class="birthday-stamp"><span>THE BIRTHDAY EDITION</span><strong>{BIRTHDAY:%d / %m}</strong><span>A LITTLE MAGIC INSIDE ✦</span></div>')
    markup('<div class="welcome-note"><span aria-hidden="true">✧</span><p>Today, the ordinary can wait.<br><strong>Let’s celebrate you.</strong></p><span aria-hidden="true">✧</span></div>')


COMPLIMENTS = [
    ("01", "Your own kind of magic", "There is only one you. The world is better with your smile in it."),
    ("02", "A friendship to appreciate", "This little surprise is a reminder that you are thought of and celebrated."),
    ("03", "So much still ahead", "May this next chapter bring brave beginnings, beautiful surprises, and reasons to be proud."),
]


def spotlight() -> None:
    heading("CHAPTER 02 · YOUR SPOTLIGHT", "A little celebration of <em>you.</em>",
            "A photograph, a few kind words, and a reminder: you deserve to feel special.")
    left, right = st.columns([0.95, 1.15], gap="large", vertical_alignment="center")
    with left:
        mode = st.radio("Choose your photo frame", ["Polaroid", "Full photograph"], horizontal=True, key="photo_frame")
        portrait("polaroid" if mode == "Polaroid" else "full")
    with right:
        markup('<div class="note-intro"><span class="handwritten">Just a few little reminders…</span><p>Tap a note. There’s something lovely inside.</p></div>')
        for number, title, message in COMPLIMENTS:
            with st.expander(f"{number}  ·  {title}"):
                markup(f'<div class="compliment"><span aria-hidden="true">✦</span><p>{message}</p></div>')
        markup('<p class="side-quote">“Keep becoming the person<br>you are proud to be.”</p>')
        next_button("letter", "There’s a letter for you  →")


def letter() -> None:
    heading("CHAPTER 03 · FROM ME TO YOU", "Some words, <em>just for you.</em>",
            "Because a birthday wish deserves a little more than a quick message.")
    _, center, _ = st.columns([0.15, 1, 0.15])
    with center:
        if not st.session_state.get("letter_open", False):
            markup(f'<div class="envelope-scene"><div class="envelope"><div class="envelope-flap"></div>'
                   f'<div class="envelope-label">To {html.escape(FIRST)}<small>A birthday letter</small></div>'
                   '<div class="wax-seal" aria-hidden="true">M</div></div><p>A little note, sealed with good wishes.</p></div>')
            st.button("Open your letter  ✉", type="primary", width="stretch", key="open_letter", on_click=change, args=("letter_open", True))
        else:
            language = st.radio("Read your letter in", ["English", "Roman Urdu"], horizontal=True, key="letter_language")
            paragraphs = CONFIG["letter"]["english"] if language == "English" else CONFIG["letter"]["roman_urdu"]
            body = "".join(f"<p>{html.escape(p)}</p>" for p in paragraphs)
            markup(f'<article class="letter-paper"><div class="letter-topline">A BIRTHDAY LETTER <span>{DATE_LABEL}</span></div>'
                   f'<h2>Dear {html.escape(FIRST)},</h2>{body}'
                   f'<div class="letter-signature"><small>With warm wishes,</small><strong>{html.escape(SENDER)}</strong><span>✦</span></div></article>')
            st.button("Seal the letter again", key="close_letter", on_click=change, args=("letter_open", False))
            next_button("wish", "Now, make a little wish  →")


def extinguish() -> None:
    st.session_state["candles_out"] = True
    celebrate()


def reset_cake() -> None:
    st.session_state["candles_out"] = False
    st.session_state["wish_saved"] = False
    st.session_state.pop("birthday_wish", None)


def save_wish() -> None:
    text = st.session_state.get("birthday_wish", "").strip()
    st.session_state["wish_saved"] = bool(text)


def wish() -> None:
    out = st.session_state.get("candles_out", False)
    heading("CHAPTER 04 · A LITTLE BIRTHDAY MAGIC", "Close your eyes.<br><em>Make a wish.</em>",
            "For the hopes you keep close, and the beautiful days still to come.")
    _, center, _ = st.columns([0.25, 1, 0.25])
    with center:
        flames = "" if out else '<span class="flame"></span>'
        candles = "".join(f'<div class="candle candle-{i}">{flames}</div>' for i in range(1, 4))
        markup(f'<div class="cake-scene {"candles-out" if out else ""}" role="img" aria-label="Birthday cake with three {"unlit" if out else "lit"} candles">'
               '<span class="cake-star star-left" aria-hidden="true">✧</span><span class="cake-star star-right" aria-hidden="true">✦</span>'
               f'<div class="cake"><div class="candles">{candles}</div><div class="cake-top"></div><div class="icing"><i></i><i></i><i></i><i></i><i></i></div>'
               '<div class="cake-body"><span>make a wish</span><div class="cake-dots">· &nbsp; · &nbsp; · &nbsp; · &nbsp; ·</div></div><div class="cake-base"></div><div class="cake-plate"></div></div>'
               f'<p>{"The candles are out. Here’s to a wonderful year!" if out else "Three candles. Endless possibilities."}</p></div>')
        if not out:
            st.button("Blow out the candles  ✨", type="primary", width="stretch", key="blow_candles", on_click=extinguish)
            markup('<p class="microcopy">Tap the button when you’re ready.</p>')
        else:
            st.success(f"Happy Birthday, {FIRST}! May your wish find its way to you.")
            with st.expander("Tuck a wish into this moment · optional", expanded=st.session_state.get("wish_saved", False)):
                with st.form("wish_form", clear_on_submit=False):
                    st.text_area("A wish for your new chapter", placeholder="This year, I hope…", key="birthday_wish", max_chars=500)
                    st.caption("Your words stay only in this browser session. Refreshing or closing it can clear them.")
                    st.form_submit_button("Keep this wish for now", on_click=save_wish)
                if st.session_state.get("wish_saved"):
                    st.success("Your wish is tucked into this moment. Keep it close to your heart.")
                elif "wish_saved" in st.session_state:
                    st.info("Write a little wish before tucking it away.")
            st.button("Light the candles again", key="relight", on_click=reset_cake)
            next_button("gift", "One last surprise for you  →")


def keepsake_html() -> bytes:
    name, sender = html.escape(NAME), html.escape(SENDER)
    body = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Happy Birthday, {name}</title><style>
    *{{box-sizing:border-box}}body{{margin:0;background:#f8f3ee;color:#392d33;font-family:Georgia,serif;padding:36px 16px}}.card{{max-width:660px;margin:auto;background:#fffcf7;border:1px solid #dfc7c8;padding:36px;text-align:center;box-shadow:0 18px 70px #61334214;border-radius:8px}}.eyebrow{{font:11px Arial;letter-spacing:3px;color:#895766}}img{{display:block;width:240px;max-width:100%;height:340px;object-fit:cover;object-position:50% 45%;border-radius:130px 130px 12px 12px;margin:24px auto}}h1{{font-size:52px;font-weight:400;line-height:1.05;margin:24px 0}}em{{color:#a75e74}}.message{{max-width:430px;margin:20px auto;font-size:18px;line-height:1.75}}.signature{{font-style:italic;color:#8a4e62;font-size:25px}}button{{border:0;border-radius:30px;background:#9b4f68;color:white;padding:14px 24px;cursor:pointer}}.screen-only{{font:12px Arial;color:#78646b;margin-top:24px}}@media(max-width:480px){{.card{{padding:24px 16px}}h1{{font-size:42px}}}}@media print{{body{{padding:0;background:white}}.card{{box-shadow:none;border:0}}.screen-only{{display:none}}}}
    </style></head><body><main class="card"><p class="eyebrow">A LITTLE KEEPSAKE · {DATE_LABEL.upper()}</p><h1>Happy Birthday,<br><em>{name}.</em></h1><img src="{photo_uri()}" alt="Portrait of {name}"><p class="message">May this year bring you peace in your heart, courage for your dreams, and happiness in the little things. You deserve a beautiful chapter.</p><p class="signature">With warm wishes, {sender}</p><p>✦ &nbsp; ✧ &nbsp; ✦</p><div class="screen-only"><button onclick="window.print()">Print or save as PDF</button><p>A small birthday memory, made just for you.</p></div></main></body></html>'''
    return body.encode("utf-8")


def open_gift() -> None:
    st.session_state["gift_open"] = True
    celebrate()


def gift() -> None:
    heading("CHAPTER 05 · SOMETHING TO KEEP", "A tiny gift.<br><em>A whole lot of good wishes.</em>",
            "One last little surprise before you start your beautiful new chapter.")
    _, center, _ = st.columns([0.2, 1, 0.2])
    with center:
        if not st.session_state.get("gift_open", False):
            markup('<div class="gift-scene"><div class="gift-box"><div class="gift-bow"><i></i><i></i></div><div class="gift-lid"></div><div class="gift-ribbon"></div><div class="gift-tag">for you ✧</div></div><p>Something small. Something made just for you.</p></div>')
            st.button("Unwrap your gift  🎁", type="primary", width="stretch", key="open_gift", on_click=open_gift)
        else:
            markup(f'<article class="keepsake-preview"><p class="eyebrow">YOUR BIRTHDAY KEEPSAKE</p><h2>Here’s to your<br><em>beautiful next chapter.</em></h2>'
                   f'<img src="{photo_uri()}" alt="Portrait of {html.escape(NAME)}" />'
                   '<p>More laughter. More little victories.<br>More moments that feel like sunshine.</p>'
                   f'<div class="handwritten">Happy Birthday, {html.escape(FIRST)}.</div><small>With warm wishes, {html.escape(SENDER)}</small></article>')
            st.download_button("Save your birthday keepsake  ↓", data=keepsake_html(), file_name="Happy_Birthday_Momna_Khan.html", mime="text/html", key="download_keepsake", width="stretch", type="primary", on_click="ignore")
            st.caption("Open the downloaded card in a browser. It includes your photo and works offline; you can also print it or save it as a PDF.")
            col1, col2 = st.columns(2)
            with col1:
                st.button("Celebrate again  ✨", key="replay", width="stretch", on_click=celebrate)
            with col2:
                st.button("Back to the beginning  ↺", key="restart", width="stretch", on_click=go, args=("home",))
            markup('<p class="final-note">The surprise ends here.<br>The good wishes stay with you.</p>')


st.html(f'<style>{(ROOT / "assets" / "style.css").read_text(encoding="utf-8")}</style>')
if not st.session_state.get("animations", True):
    st.html('<style>*,*::before,*::after{animation:none!important;transition:none!important}</style>')

markup(f'<header class="brandbar"><div class="brand"><span class="brand-symbol" aria-hidden="true">✧</span><div>For {html.escape(FIRST)}<small>A LITTLE BIRTHDAY STORY</small></div></div><div class="date-pill"><span aria-hidden="true">✦</span> {DATE_LABEL}</div></header>')

PAGES = {
    "home": st.Page(welcome, title="Welcome", default=True),
    "spotlight": st.Page(spotlight, title="Your Spotlight", url_path="spotlight"),
    "letter": st.Page(letter, title="A Letter", url_path="letter"),
    "wish": st.Page(wish, title="Make a Wish", url_path="wish"),
    "gift": st.Page(gift, title="Your Gift", url_path="gift"),
}
page = st.navigation(list(PAGES.values()), position="hidden")
destination = st.session_state.pop("next_page", None)
if destination in PAGES:
    st.switch_page(PAGES[destination])
items = [("home", "01 · Welcome"), ("spotlight", "02 · Spotlight"), ("letter", "03 · Letter"), ("wish", "04 · Wish"), ("gift", "05 · Gift")]
active = next(key for key, value in PAGES.items() if value.url_path == page.url_path)
with st.container(key="chapters"):
    columns = st.columns(5, gap="small")
    for column, (key, label) in zip(columns, items):
        with column:
            st.button(label, key=f"nav_{key}", type="primary" if active == key else "secondary", width="stretch", on_click=go, args=(key,))

page.run()

markup(f'<footer class="footer"><span>Made with thought, care & a little code.</span><span>FOR {html.escape(NAME.upper())} <span aria-hidden="true">✧</span></span></footer>')
with st.expander("A little music & comfort settings"):
    music, settings = st.columns([1.4, 1])
    with music:
        st.caption("A gentle original melody for your birthday. Press play whenever you like.")
        st.audio((ROOT / "assets" / "birthday_melody.wav").read_bytes(), format="audio/wav")
    with settings:
        st.toggle("Celebration animations", value=True, key="animations", help="Turn off the page animations and birthday balloons.")
        st.caption("Your device’s reduced-motion preference also softens the page animations.")
