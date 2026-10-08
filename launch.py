"""Start Streamlit, then open the browser once the app is ready."""

from pathlib import Path
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
import webbrowser

ROOT = Path(__file__).resolve().parent
URL = "http://localhost:8501"


def open_when_ready(server: subprocess.Popen) -> None:
    # The app stays in headless mode to skip Streamlit's first-run email prompt.
    # Opening the page here lets the browser wait for a healthy server instead.
    local_http = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    for _ in range(150):
        if server.poll() is not None:
            return
        try:
            with local_http.open(URL + "/_stcore/health", timeout=1) as response:
                if response.status == 200:
                    print(f"\nYour birthday app is ready: {URL}\n", flush=True)
                    if not webbrowser.open_new_tab(URL):
                        print("Open the address above in Chrome or Edge.", flush=True)
                    return
        except (urllib.error.URLError, TimeoutError, OSError):
            pass
        time.sleep(0.3)
    print(f"The app is taking longer to start. Open {URL} or check the error above.", flush=True)


def main() -> int:
    server = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "app.py",
         "--server.headless", "true", "--server.address", "127.0.0.1",
         "--server.port", "8501", "--browser.serverAddress", "localhost"],
        cwd=ROOT,
    )
    threading.Thread(target=open_when_ready, args=(server,), daemon=True).start()
    try:
        return server.wait()
    except KeyboardInterrupt:
        if server.poll() is None:
            server.terminate()
        try:
            server.wait(timeout=10)
        except subprocess.TimeoutExpired:
            server.kill()
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
