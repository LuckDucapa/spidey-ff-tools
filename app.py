from flask import Flask, request, Response, render_template_string
import requests
import datetime
import pytz
import firebase_admin
from firebase_admin import credentials, db

app = Flask(__name__)

# --- CONFIGURATION ---
DOMAIN = "https://spidey-ff-tools.vercel.app"
TG_CONTACT = "https://t.me/spidey_abd"
TG_GROUP = "https://t.me/TubeGrowOfficiall"
TG_CHANNEL = "https://t.me/TubeGroww"
MASTER_KEY = "SpideyTCPTools" 
COST_PER_REQ = 7  # Credits per request

# ======================================================
#  👇👇👇 PASTE YOUR FIREBASE JSON BELOW 👇👇👇
# ======================================================

{
  "type": "service_account",
  "project_id": "spidey-ff-tools",
  "private_key_id": "41b3851517d27c97ec61c3c0819fa70f7b14f893",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDIY9nCIKVFi8vk\nmX0AOr0RPn9Z1pArBMtWIqJe2ae/g567eKkprw0VNoYsffm7XV6655rBDdW+Nm2z\nWoFcqE3BKTyoU3rtOi77yyeWPuQ+tSs8USvQh1XhXSsglSnAXOUawiyxLYmpuNYc\noZenLWMTEtdu9pCYEwDmiCtIJ6lMzH4hW6ub8jvWOuQVUqHq0JR261iQtJyHqkBA\nqWx6jsdPXRD7RlX67epme1sr4BrufAMaO9EvVQUkxEmE5waro4KYUfAixOLA7mvd\ntV9Mkgmu5vpJ+V/IeyIIycnyo8wPDNQacPu6eRM7d8w8Gpxv8i0KzoGdvJ0cmger\naA9X01mfAgMBAAECggEAAhzCAgtbt/jKHJic74su91xmyu4kP+fW3Yto6xdf7s4M\nNs1bTyQCvyCqLRQ439zomjobG1eHfhqkcQ8OV7Pdz0ry0j1rCXl4XvwcaIzfgA+4\ngHQZ7Pf4Pki/+HcfZQvgTbYSnYgthXtRenoeQfYMWiTz3hNoS8oWKNfySNpDgm/i\nl0/XNxNcC1XkPbBQK2N8TT7rzbg65YnvlJaHI3M/Xq160oqIh3jxodCOl3+fR1DI\nSORgNg4Nep/hbzihX9Ukbd0KtlRA6QwtRyQd0qgNzKWtjZI7qf2AnF1r8UzedHJy\nrqU8Vh7U0qFu55KOV1r5PyORpXnWbR0DzCMsLa61TQKBgQD/RFfDL4CXYX2ZlpdE\nL2ishyOaPEbbM9Sx87p8K6T+//ery1dh/bX1aN4BK5a8CST029dbNX7L1ZzxGBq/\nnlpt3t8ellnJn78RKvbY/TkzoaXCAi+C7liDBjGIptlrFHr+u5DRsFrJt5f5/KIU\nLmAjktFMreHcPl52IbEuOQHF0wKBgQDI9ypgBjOW+0dsIAgwE9onxhIV6q5gQ0hT\nXxzd6Vu8mm4KswtGf/oYaFRicRtRVNuucwPj0ByuR+r7nzuY9f7PDkHgLAWY/Lat\nCBNWCPwmJKuvBD1E1j6Pvhbv0Ad9VWUCPIFOSO3TYVEUBX3gLNNXraqGwPvU9Wo7\nM4HFcX9BhQKBgQCOwX6/RpKIllnyifhAhq7oRY9Qk0MhFaRufJqfFJ1qimXNKqPM\nxmF7RFFboC/lKswDL+sJNCqb/fOOFWfoH7v80/Y9meHO00q8ZCW2hi72RAF6NVSy\nyW6wn8cV4BGZQ9PhH65GxnSPeOBCStmtpZ3YZyQr2NaGIE8di4wWCIWIRwKBgHrk\nChmmMS4GgupvvBIKUcE4sh6M4A0ll7jD1NcuuFZg6SHJ0v9NixYZ1mBMYjQd/Ch1\nVM+el6tLdzpfaQZkh2j+gvIeeV3QS7UL1ycpX2fDzOi9YuoRSTiFOWl0gN/3tEjl\nzvycRDKatAXWRd8sCiD3peu5X0YevNNu79BZU0QxAoGAe1kZfkJM8Aayr8XaV2cM\n3TmBhmzKAW+3v0Qehd7dQ5pHfqF8qDC/Zn7WUpubpNzfT8qdmGkFTrT7FuUU+otL\nHyS4TWykIxWS1t/0EVDrk2fdP0/jm1Jkdy5iT5aldedG6xbhoM0IiTA5an1A3AU4\nRqKwcRA4bxU4Ws1GzdMNaWQ=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-fbsvc@spidey-ff-tools.iam.gserviceaccount.com",
  "client_id": "106731642768031071115",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40spidey-ff-tools.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

# ======================================================

# --- FIREBASE INIT ---
try:
    if not firebase_admin._apps:
        if FIREBASE_JSON and len(FIREBASE_JSON) > 1:
            cred = credentials.Certificate(FIREBASE_JSON)
            firebase_admin.initialize_app(cred, {
                'databaseURL': f"https://{FIREBASE_JSON.get('project_id')}-default-rtdb.firebaseio.com/"
            })
except Exception as e:
    print(f"Firebase Error: {e}")

# --- HELPER FUNCTIONS ---
def process_key_credits(key):
    """
    Checks if key exists, has credits, and is active.
    Deducts credits if valid.
    """
    if key == MASTER_KEY: return True, "OK"
    
    try:
        ref = db.reference(f'users/{key}') # Key is the Telegram User ID
        user_data = ref.get()
        
        if not user_data:
            return False, "Invalid API Key"
        
        # Check active status (controlled by Bot)
        if not user_data.get('is_active', True):
            return False, "Key Disabled. Please Join Channel/Group to enable."
            
        credits = user_data.get('credits', 0)
        
        if credits < COST_PER_REQ:
            return False, f"Insufficient Credits. Need {COST_PER_REQ}, Have {credits}. Use /daily_bonus in Bot."
            
        # Deduct Credits
        ref.update({
            'credits': credits - COST_PER_REQ,
            'requests': user_data.get('requests', 0) + 1
        })
        return True, "OK"
            
    except Exception as e:
        return False, f"Server Error: {str(e)}"

# --- THIEF PROTECTION ---
@app.before_request
def block_thief():
    path = request.path.lower()
    blocked = ['app.py', 'vercel.json', 'requirements.txt', '.git', '.env']
    if any(b in path for b in blocked):
        return Response("You are Thief", mimetype='text/plain', status=403)

# --- PUBLIC PAGE ---
HTML_HOME = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Spidey FF Tools API</title>
    <style>
        :root { --bg: #0d1117; --text: #c9d1d9; --accent: #00ff99; --border: #30363d; --card: #161b22; }
        body { background-color: var(--bg); color: var(--text); font-family: monospace; padding: 20px; }
        .container { max-width: 900px; margin: auto; }
        h1 { color: var(--accent); text-align: center; border-bottom: 1px solid var(--border); padding-bottom: 10px; }
        .endpoint { background: var(--card); border: 1px solid var(--border); margin-bottom: 20px; padding: 15px; border-radius: 8px; }
        .url { background: #000; color: var(--accent); padding: 10px; word-break: break-all; border-radius: 4px; margin-top: 5px; }
        .footer { text-align: center; margin-top: 40px; border-top: 1px solid var(--border); padding-top: 20px; }
        a { color: #58a6ff; text-decoration: none; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Spidey FF Tools</h1>
        <p style="text-align:center; color: #ff5555;">Valid API Key Required (Telegram ID)</p>
        <div class="endpoint">
            <strong>Account Info</strong>
            <div class="url">{{ domain }}/api/info?uid={uid}&key={key}</div>
        </div>
        <div class="endpoint">
            <strong>Equip Emote</strong>
            <div class="url">{{ domain }}/api/emote?region={region}&teamcode={tc}&uid={uid}&emote_id={id}&key={key}</div>
        </div>
        <div class="endpoint">
            <strong>Lag Server</strong>
            <div class="url">{{ domain }}/api/lag?region={region}&teamcode={tc}&key={key}</div>
        </div>
        <div class="endpoint">
            <strong>5 Group</strong>
            <div class="url">{{ domain }}/api/5group?region={region}&uid={uid}&key={key}</div>
        </div>
        <div class="endpoint">
            <strong>6 Group</strong>
            <div class="url">{{ domain }}/api/6group?region={region}&uid={uid}&key={key}</div>
        </div>
        <div class="footer">
            <a href="{{ tg_contact }}">Buy API Key</a> | <a href="{{ tg_group }}">Telegram Group</a>
        </div>
    </div>
</body>
</html>
"""

@app.route('/api')
def home():
    return render_template_string(HTML_HOME, domain=DOMAIN, tg_contact=TG_CONTACT, tg_group=TG_GROUP)

# --- PROXY LOGIC ---
def proxy(url, key):
    if not key: return Response("Missing key", 401, mimetype='text/plain')
    
    # Check Credits & Validity
    is_valid, msg = process_key_credits(key)
    if not is_valid: 
        return Response(f"Error: {msg}\nContact: {TG_CONTACT}", 403, mimetype='text/plain')
    
    try:
        r = requests.get(url)
        return Response(r.text + f"\n\nJSON credit: {TG_CONTACT}", mimetype='text/plain')
    except Exception as e: return Response(f"Error: {e}", 500, mimetype='text/plain')

@app.route('/api/info')
def api_info(): return proxy(f"https://danger-info-alpha.vercel.app/accinfo?uid={request.args.get('uid')}&key=DANGERxINFO", request.args.get('key'))

@app.route('/api/emote')
def api_emote(): a=request.args; return proxy(f"https://proapi.sumittools.shop/emote?key=ShadowProTCP&region={a.get('region')}&tc={a.get('teamcode')}&uid1={a.get('uid')}&emote_id={a.get('emote_id')}", a.get('key'))

@app.route('/api/lag')
def api_lag(): a=request.args; return proxy(f"https://proapi.sumittools.shop/lag?key=ShadowProTCP&region={a.get('region')}&tc={a.get('teamcode')}", a.get('key'))

@app.route('/api/5group')
def api_5group(): a=request.args; return proxy(f"https://proapi.sumittools.shop/5group?key=ShadowProTCP&region={a.get('region')}&uid={a.get('uid')}", a.get('key'))

@app.route('/api/6group')
def api_6group(): a=request.args; return proxy(f"https://proapi.sumittools.shop/6group?key=ShadowProTCP&region={a.get('region')}&uid={a.get('uid')}", a.get('key'))

if __name__ == '__main__':
    app.run()