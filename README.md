# YouTube Playlist Creator - Setup & Usage Guide

This README explains step by step how to set up and use the Python script to create a YouTube playlist from a list of songs.

---

## 1. Authentication: Create OAuth Client ID

1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Make sure you select or create the project you want to use.
3. Enable the **YouTube Data API v3** for this project:

   * Navigate to **APIs & Services → Library**.
   * Search for **YouTube Data API v3** and click **Enable**.
4. Configure OAuth consent screen:

   * Navigate to **APIs & Services → OAuth consent screen**.
   * Select **External** user type.
   * Fill in required fields:

     * App name (e.g., "YouTube Playlist Creator")
     * User support email (your Gmail)
     * Developer contact email (your Gmail)
   * Save.
5. Add your account as a **Test User**:

   * Go to **Test Users** tab in the OAuth consent screen.
   * Click **+ Add users** and add your Gmail account.
   * Save.
6. Create OAuth Client ID:

   * Go to **APIs & Services → Credentials**.
   * Click **Create Credentials → OAuth client ID**.
   * Choose **Application type: Desktop app**.
   * Give it a name (e.g., "YouTube Playlist Script").
   * Download the JSON file and save it as `client_secret.json` in the same folder as the script.

---

## 2. Prepare Your Song List

* Create a simple `.txt` file with one song per line, e.g., `songs.txt`:

  ```
  Coldplay - Yellow
  Adele - Hello
  Imagine Dragons - Believer
  ```
* Place this file in the same folder as your Python script.

---

## 3. Install Python Dependencies

Open a terminal and run:

```bash
pip install google-api-python-client google-auth-oauthlib
```

---

## 4. Run the Script

1. Make sure you have the following files in the same folder:

   * `main.py` (the Python script)
   * `client_secret.json` (OAuth credentials)
   * `songs.txt` (your song list)
2. Run the script:

```bash
python main.py
```

3. The first time it runs, it will open a browser window:

   * Log in with the Gmail account you added as a Test User.
   * Grant permission to the app.
   * A `token.pickle` file will be saved for future runs, so you won’t need to log in again.
4. The script will create a new playlist in your account and add all songs from your list.

---

## 5. Notes & Tips

* **Quota Limits**: YouTube Data API has a daily quota (10,000 units/day by default). Each search request uses units, so if your song list is very long, you might hit the quota.
* **Caching Video IDs**: To avoid exceeding quota, the script can cache video IDs after the first search.
* **Re-running**: You can re-run the script anytime; it will use the saved OAuth token and continue adding songs.

---

## 6. Limitations

* **Daily Quota:** Each project has a limited number of API requests per day. For large playlists, you may exceed this quota.
* **Search Accuracy:** The script picks the first search result. If multiple videos match a song title, it may not select the intended version.
* **Public/Private Playlists:** The playlist will be created as public by default. You can change privacy settings manually or modify the script.
* **Rate Limits:** Making too many requests in a short time may trigger temporary API rate limits.
* **Test Users:** Only accounts added as Test Users can authorize the OAuth app if it is not published


## 7. Additanl Notes
* **Token Expiration**:  
  Sometimes the saved `token.pickle` becomes invalid (expired or revoked). If you see an error like `invalid_grant: Token has been expired or revoked`, you need to refresh your credentials:
  1. Run the helper script `auth_refresh.py`:
     ```bash
     python auth_refresh.py
     ```
  2. A browser window will open. Log in with the same Google account.
  3. A new `token.pickle` will be generated, and you can run `main.py` again.

## 8. Folder Structure Example

```
youtube_playlist/
│
├─ main.py
├─ client_secret.json
├─ songs.txt
├─last_added.txt
├─authrefresh.py
└─ token.pickle  # generated after first run

```

---

Follow this guide every time you want to create a playlist from a list of songs.
