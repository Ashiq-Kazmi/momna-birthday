# For Momna — a little birthday story

A complete five-page Streamlit birthday website for **Momna Khan**, dated
**9 October 2026**, from **Kazmi Wazir**. The attached photograph is already
included. The design uses warm ivory, rose, gold, serif headings, and soft
animations. It includes an original melody and works without external APIs.

## The five pages

1. **Welcome:** a personal birthday greeting, framed photo, and surprise button.
2. **Your Spotlight:** a Polaroid or full-photo view and three notes to open.
3. **A Letter:** click the sealed envelope to reveal a friendly birthday letter.
   Switch between English and Roman Urdu.
4. **Make a Wish:** animated cake and candles. Click to blow them out, celebrate,
   write an optional wish, or light the candles again.
5. **Your Gift:** unwrap a photo keepsake, download a self-contained HTML birthday
   card, and replay the celebration. The card can be printed or saved as a PDF.

Click the five chapter buttons at the top to visit any page. Each page also has
a button that moves the story forward. Music is optional: expand **A little
music & comfort settings** at the bottom and press play. Animations can be
disabled there.

## Run on Windows

The app supports **Python 3.9 or newer**, with **Python 3.12 recommended**.
Install Python from https://www.python.org/downloads/
and select **Add Python to PATH** during installation.

1. Extract the ZIP completely. Do not run the app from inside the ZIP.
2. Open the `momna_birthday` folder.
3. Double-click **START_WINDOWS.bat**. The first launch installs Streamlit.
4. Your browser should open automatically. If it does not, open
   **http://localhost:8501** yourself. Keep the black terminal window open.

The black window is the running app server, not the birthday page. The page
opens in Chrome, Edge, or another browser. Installation can take a few minutes
the first time. If an error appears, the launcher keeps the window open so you
can copy the message.

You can instead open PowerShell inside that folder and run:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

No PowerShell activation command or execution-policy change is needed. If `py`
is unavailable but Python is installed, use `python` instead for the first line.

## Run on macOS or Linux

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m streamlit run app.py
```

Or use `bash start.sh`. Open http://localhost:8501.

## Personalise it

Edit **birthday.toml** to change the name, signature, date, or letter paragraphs.
Replace **assets/momna.jpeg** if you want a different photograph. Keep that exact
filename, or update `photo_uri()` in `app.py`.

Files:

```text
momna_birthday/
  app.py
  launch.py
  birthday.toml
  requirements.txt
  START_WINDOWS.bat
  start.sh
  README.md
  .streamlit/config.toml
  assets/momna.jpeg
  assets/style.css
  assets/birthday_melody.wav
```

## Let Momna open it

`localhost` works on your own computer. Sending that address to someone else
does not share the app.

For a phone on the **same Wi-Fi**, run:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py --server.address 0.0.0.0
```

Run `ipconfig` to find your computer's Wi-Fi IPv4 address. On her phone, open
`http://YOUR-COMPUTER-IP:8501`. If Windows asks about network access, allow Python
on the private network. Your computer and the app must remain running.

For a link she can open from another location, deploy the extracted project to
**Streamlit Community Cloud**:

1. Put the extracted project files in a GitHub repository; keep the picture and
   assets with the code. A private repository keeps the source and photo from
   appearing in a public code repository.
2. Sign in at https://share.streamlit.io/ and create an app from that repository.
3. Select `app.py` as the entrypoint and Python 3.11 or newer. If you committed
   the parent folder, use `momna_birthday/app.py` instead.
4. Review the app's sharing settings. For an app restricted to invited viewers,
   select the supported private sharing option and invite Momna's email address.
   Apps initially inherit the repository's privacy; review the app settings
   because these can be changed independently afterward.
5. Copy the app's deployed URL and send it to her.

No hosted link is included in this download. It is the complete runnable app.
The downloaded HTML keepsake is a separate, simple card you can also send as a
file; it opens in a browser without Python and includes the photo.
An already prepared copy, **Birthday_Keepsake.html**, is included in the ZIP.
Double-click it to see the card immediately, or send that file to Momna.

The optional wish is stored only in the Streamlit session; it is not written to
a database or file. Closing or refreshing the session can clear it.

## Design references

Publicly searchable birthday projects and creator examples inspired the chapter
structure, letter reveal, gift reveal, and candle interaction. This app's code,
styling, and messages were written specifically for Momna; no paid template was
downloaded or copied.

- Birthday Wishing Website, a creator's project inspired by Instagram reels:
  https://stardance.hackclub.com/projects/13095
- Peoniestudio's birthday website overview (creator active on TikTok/Instagram):
  https://ko-fi.com/s/ea7884dd8f
- Streamlit multipage navigation documentation:
  https://docs.streamlit.io/develop/api-reference/navigation/st.navigation
- Streamlit Community Cloud deployment documentation:
  https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app
- Streamlit sharing and privacy documentation:
  https://docs.streamlit.io/deploy/streamlit-community-cloud/share-your-app

The original bell melody was synthesised for this app. No music download,
payment, Facebook login, or API key is needed.

## Checks completed

Tested with Streamlit 1.50.0 and Chromium: the five-page journey, photo modes,
letter reveal and both languages, candle blowing and relighting, wish submission,
gift reveal and actual card download, music playback, animation controls, and
navigation back to previously opened pages. Layouts were inspected at 1440px
desktop and 390px phone widths. The original photograph's bytes are preserved.
