from flask import Flask, request, Response, render_template_string, session, redirect, url_for
import requests
import datetime
import pytz
import os

app = Flask(__name__)
app.secret_key = "SPIDEY_SECRET_KEY_CHANGE_THIS"

# --- CONFIGURATION ---
DOMAIN = "https://spidey-ff-tools.vercel.app"
ADMIN_EMAIL = "spidyabd07@gmail.com"
ADMIN_PASS = "7344010091@gmail"
MASTER_KEY = "SpideyTCPTools"

# Telegram Links
TG_CONTACT = "https://t.me/spidey_abd"
TG_GROUP = "https://t.me/TubeGrowOfficiall"
TG_CHANNEL = "https://t.me/TubeGroww"

# --- DATA STORE (In-Memory) ---
api_keys = {}

# --- SECURITY: THIEF PROTECTION ---
@app.before_request
def block_source_access():
    """
    This function runs before EVERY request.
    If someone tries to access source files, we block them immediately.
    """
    path = request.path.lower()
    blocked_files = ['/app.py', '/vercel.json', '/requirements.txt', '/.git', '/.env']
    
    for blocked in blocked_files:
        if path.endswith(blocked) or blocked in path:
            return Response("Sudhar Ja Bhosdi Ke", mimetype='text/plain', status=403)

# --- HTML TEMPLATES ---

# 1. Public API Page (Redesigned)
HTML_HOME = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Spidey FF Tools API</title>
    <style>
        :root { --bg: #0d1117; --text: #c9d1d9; --accent: #00ff99; --border: #30363d; --card: #161b22; --fail: #ff5555; }
        body { background-color: var(--bg); color: var(--text); font-family: 'Consolas', 'Monaco', monospace; margin: 0; padding: 20px; }
        .container { max-width: 900px; margin: auto; }
        h1 { color: var(--accent); text-align: center; text-transform: uppercase; letter-spacing: 2px; border-bottom: 2px solid var(--border); padding-bottom: 10px; }
        .alert { background: rgba(255, 85, 85, 0.1); border: 1px solid var(--fail); color: var(--fail); padding: 15px; border-radius: 6px; text-align: center; margin-bottom: 30px; }
        .endpoint-card { background-color: var(--card); border: 1px solid var(--border); border-radius: 8px; margin-bottom: 25px; overflow: hidden; }
        .card-header { background: #21262d; padding: 10px 15px; font-weight: bold; color: #fff; border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; }
        .badge { background: var(--accent); color: #000; padding: 2px 8px; border-radius: 4px; font-size: 0.8em; font-weight: bold; }
        .card-body { padding: 15px; }
        .url-box { background: #000; color: var(--accent); padding: 10px; border-radius: 4px; word-break: break-all; font-size: 0.9em; border: 1px solid #333; margin-top: 5px; }
        .label { font-size: 0.8em; color: #8b949e; text-transform: uppercase; letter-spacing: 1px; }
        .footer { text-align: center; margin-top: 50px; border-top: 1px solid var(--border); padding-top: 20px; font-size: 0.9em; }
        a { color: #58a6ff; text-decoration: none; }
        a:hover { text-decoration: underline; }
        .btn-admin { display: inline-block; background: var(--border); color: #fff; padding: 8px 16px; border-radius: 6px; margin-top: 10px; border: 1px solid #777; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Spidey FF Tools</h1>
        
        <div class="alert">
            <strong>ACCESS RESTRICTED:</strong> You need a valid API Key to use these endpoints.<br>
            Without a key, requests will fail.
        </div>

        <!-- Info Endpoint -->
        <div class="endpoint-card">
            <div class="card-header">
                <span>Account Info</span>
                <span class="badge">GET</span>
            </div>
            <div class="card-body">
                <div class="label">Request URL</div>
                <div class="url-box">{{ domain }}/api/info?uid={uid}&key={key}</div>
            </div>
        </div>

        <!-- Emote Endpoint -->
        <div class="endpoint-card">
            <div class="card-header">
                <span>Equip Emote</span>
                <span class="badge">GET</span>
            </div>
            <div class="card-body">
                <div class="label">Request URL</div>
                <div class="url-box">{{ domain }}/api/emote?region={region}&teamcode={tc}&uid={uid}&emote_id={id}&key={key}</div>
            </div>
        </div>

        <!-- Lag Endpoint -->
        <div class="endpoint-card">
            <div class="card-header">
                <span>Lag Server</span>
                <span class="badge">GET</span>
            </div>
            <div class="card-body">
                <div class="label">Request URL</div>
                <div class="url-box">{{ domain }}/api/lag?region={region}&teamcode={tc}&key={key}</div>
            </div>
        </div>

        <!-- 5Group Endpoint -->
        <div class="endpoint-card">
            <div class="card-header">
                <span>5 Group Glitch</span>
                <span class="badge">GET</span>
            </div>
            <div class="card-body">
                <div class="label">Request URL</div>
                <div class="url-box">{{ domain }}/api/5group?region={region}&uid={uid}&key={key}</div>
            </div>
        </div>

        <!-- 6Group Endpoint -->
        <div class="endpoint-card">
            <div class="card-header">
                <span>6 Group Glitch</span>
                <span class="badge">GET</span>
            </div>
            <div class="card-body">
                <div class="label">Request URL</div>
                <div class="url-box">{{ domain }}/api/6group?region={region}&uid={uid}&key={key}</div>
            </div>
        </div>

        <div class="footer">
            <p><strong>Contact & Support</strong></p>
            <p>
                <a href="{{ tg_contact }}">Admin (Buy Key)</a> • 
                <a href="{{ tg_group }}">Telegram Group</a> • 
                <a href="{{ tg_channel }}">Telegram Channel</a>
            </p>
            <br>
            <a href="/admin_734401" class="btn-admin">Admin Login</a>
        </div>
    </div>
</body>
</html>
"""

# 2. Login Page (Dark Theme)
HTML_LOGIN = """
<!DOCTYPE html>
<html>
<head>
    <title>Admin Login</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { background-color: #0d1117; color: #c9d1d9; font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .box { background: #161b22; padding: 40px; border-radius: 10px; border: 1px solid #30363d; text-align: center; width: 300px; box-shadow: 0 4px 12px rgba(0,0,0,0.5); }
        input { width: 90%; padding: 12px; margin: 10px 0; background: #0d1117; border: 1px solid #30363d; color: white; border-radius: 6px; outline: none; }
        input:focus { border-color: #58a6ff; }
        button { width: 100%; padding: 12px; background: #238636; border: none; color: white; cursor: pointer; border-radius: 6px; font-weight: bold; margin-top: 10px; }
        button:hover { background: #2ea043; }
        h2 { color: #fff; margin-top: 0; }
    </style>
</head>
<body>
    <div class="box">
        <h2>SECURE LOGIN</h2>
        <form action="/admin/login_action" method="POST">
            <input type="email" name="email" placeholder="Email Address" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Access Panel</button>
        </form>
    </div>
</body>
</html>
"""

# 3. Admin Dashboard
HTML_DASHBOARD = """
<!DOCTYPE html>
<html>
<head>
    <title>Admin Panel</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { background-color: #0d1117; color: #c9d1d9; font-family: monospace; padding: 20px; }
        h1 { color: #58a6ff; }
        .panel { background: #161b22; padding: 20px; border-radius: 8px; margin-bottom: 20px; border: 1px solid #30363d; }
        input, select { padding: 8px; background: #0d1117; border: 1px solid #30363d; color: white; margin-right: 10px; border-radius: 4px; }
        button { padding: 8px 15px; background: #1f6feb; border: none; cursor: pointer; color: white; font-weight: bold; border-radius: 4px; }
        .del-btn { background: #da3633; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #30363d; padding: 10px; text-align: left; }
        th { color: #58a6ff; background: #21262d; }
    </style>
</head>
<body>
    <div style="display:flex; justify-content:space-between; align-items:center;">
        <h1>Admin Panel</h1>
        <a href="/admin/logout" style="color: #da3633; text-decoration: none; border: 1px solid #da3633; padding: 5px 10px; border-radius: 4px;">Logout</a>
    </div>
    
    <div class="panel">
        <h3 style="margin-top:0;">Generate Key</h3>
        <form action="/admin/add_key" method="POST">
            <input type="text" name="new_key" placeholder="Key Name (e.g. User1)" required>
            <label>Expiry (IST):</label>
            <input type="datetime-local" name="expiry_time" required>
            <button type="submit">Create Key</button>
        </form>
    </div>

    <div class="panel">
        <h3 style="margin-top:0;">Active Keys</h3>
        <table>
            <tr>
                <th>Key</th>
                <th>Hits</th>
                <th>Expiry (IST)</th>
                <th>Status</th>
                <th>Action</th>
            </tr>
            {% for key, data in keys.items() %}
            <tr>
                <td>{{ key }}</td>
                <td>{{ data['requests'] }}</td>
                <td>{{ data['expiry'] }}</td>
                <td style="color: {{ 'red' if data['expired'] else '#3fb950' }}">
                    {{ 'EXPIRED' if data['expired'] else 'ACTIVE' }}
                </td>
                <td>
                    <form action="/admin/delete_key" method="POST" style="display:inline;">
                        <input type="hidden" name="key_to_delete" value="{{ key }}">
                        <button type="submit" class="del-btn">Remove</button>
                    </form>
                </td>
            </tr>
            {% endfor %}
            <tr>
                <td style="color: #a371f7">{{ master_key }}</td>
                <td>∞</td>
                <td>NEVER</td>
                <td style="color: #3fb950">PERMANENT</td>
                <td>Admin</td>
            </tr>
        </table>
    </div>
</body>
</html>
"""

# --- HELPER FUNCTIONS ---

def get_ist_time():
    return datetime.datetime.now(pytz.timezone('Asia/Kolkata'))

def is_key_valid(key):
    if key == MASTER_KEY:
        return True
    if key in api_keys:
        key_data = api_keys[key]
        if get_ist_time() > key_data['expiry']:
            return False
        api_keys[key]['requests'] += 1
        return True
    return False

def proxy_request(target_url, key):
    if not key:
        return Response("Error: Missing 'key' parameter.", status=401, mimetype='text/plain')
    if not is_key_valid(key):
        return Response(f"Error: Invalid or Expired API Key.\nContact Admin: {TG_CONTACT}", status=403, mimetype='text/plain')

    try:
        response = requests.get(target_url)
        # Combine response with credit, ensuring clean newlines
        final_output = response.text + f"\n\nJSON credit: {TG_CONTACT}"
        return Response(final_output, mimetype='text/plain')
    except Exception as e:
        return Response(f"Internal Error: {str(e)}", status=500, mimetype='text/plain')

# --- ROUTES ---

@app.route('/api')
def home():
    return render_template_string(HTML_HOME, domain=DOMAIN, tg_contact=TG_CONTACT, tg_group=TG_GROUP, tg_channel=TG_CHANNEL)

@app.route('/admin_734401')
def admin_login():
    if session.get('logged_in'): return redirect('/admin/dashboard')
    return render_template_string(HTML_LOGIN)

@app.route('/admin/login_action', methods=['POST'])
def login_action():
    if request.form.get('email') == ADMIN_EMAIL and request.form.get('password') == ADMIN_PASS:
        session['logged_in'] = True
        return redirect('/admin/dashboard')
    return Response("Wrong Credentials.", status=403, mimetype='text/plain')

@app.route('/admin/dashboard')
def dashboard():
    if not session.get('logged_in'): return redirect('/admin_734401')
    
    display_keys = {}
    now = get_ist_time()
    for k, v in api_keys.items():
        display_keys[k] = {
            'requests': v['requests'],
            'expiry': v['expiry'].strftime('%Y-%m-%d %H:%M:%S'),
            'expired': now > v['expiry']
        }
    return render_template_string(HTML_DASHBOARD, keys=display_keys, master_key=MASTER_KEY)

@app.route('/admin/add_key', methods=['POST'])
def add_key():
    if not session.get('logged_in'): return redirect('/admin_734401')
    nk, exp = request.form.get('new_key'), request.form.get('expiry_time')
    if nk and exp:
        try:
            dt_aware = pytz.timezone('Asia/Kolkata').localize(datetime.datetime.strptime(exp, '%Y-%m-%dT%H:%M'))
            api_keys[nk] = {'expiry': dt_aware, 'requests': 0}
        except: pass
    return redirect('/admin/dashboard')

@app.route('/admin/delete_key', methods=['POST'])
def delete_key():
    if not session.get('logged_in'): return redirect('/admin_734401')
    k = request.form.get('key_to_delete')
    if k in api_keys: del api_keys[k]
    return redirect('/admin/dashboard')

@app.route('/admin/logout')
def logout():
    session.pop('logged_in', None)
    return redirect('/api')

# --- API ENDPOINTS ---

@app.route('/api/info')
def api_info():
    uid = request.args.get('uid')
    key = request.args.get('key')
    if not uid: return Response("Error: Missing uid", mimetype='text/plain')
    return proxy_request(f"https://danger-info-alpha.vercel.app/accinfo?uid={uid}&key=DANGERxINFO", key)

@app.route('/api/emote')
def api_emote():
    args = request.args
    req = ['region', 'teamcode', 'uid', 'emote_id']
    if not all(args.get(x) for x in req): return Response("Error: Missing parameters", mimetype='text/plain')
    return proxy_request(f"https://proapi.sumittools.shop/emote?key=ShadowProTCP&region={args['region']}&tc={args['teamcode']}&uid1={args['uid']}&emote_id={args['emote_id']}", args.get('key'))

@app.route('/api/lag')
def api_lag():
    args = request.args
    if not (args.get('region') and args.get('teamcode')): return Response("Error: Missing parameters", mimetype='text/plain')
    return proxy_request(f"https://proapi.sumittools.shop/lag?key=ShadowProTCP&region={args['region']}&tc={args['teamcode']}", args.get('key'))

@app.route('/api/5group')
def api_5group():
    args = request.args
    if not (args.get('region') and args.get('uid')): return Response("Error: Missing parameters", mimetype='text/plain')
    return proxy_request(f"https://proapi.sumittools.shop/5group?key=ShadowProTCP&region={args['region']}&uid={args['uid']}", args.get('key'))

@app.route('/api/6group')
def api_6group():
    args = request.args
    if not (args.get('region') and args.get('uid')): return Response("Error: Missing parameters", mimetype='text/plain')
    return proxy_request(f"https://proapi.sumittools.shop/6group?key=ShadowProTCP&region={args['region']}&uid={args['uid']}", args.get('key'))

if __name__ == '__main__':
    app.run(debug=True)