from flask import Flask, request, Response, render_template_string, session, redirect, url_for
import requests
import datetime
import pytz

app = Flask(__name__)
app.secret_key = "SPIDEY_SECRET_KEY_CHANGE_THIS"  # Needed for login sessions

# --- CONFIGURATION ---
ADMIN_EMAIL = "spidyabd07@gmail.com"
ADMIN_PASS = "7344010091@gmail"
MASTER_KEY = "SpideyTCPTools"  # This key always works and is hidden

# Telegram Links
TG_CONTACT = "https://t.me/spidey_abd"
TG_GROUP = "https://t.me/TubeGrowOfficiall"
TG_CHANNEL = "https://t.me/TubeGroww"

# --- DATA STORE (In-Memory) ---
# Format: {'KEY_NAME': {'expiry': datetime_obj, 'requests': 0}}
# Note: On Vercel, this resets if the server restarts.
api_keys = {}

# --- HTML TEMPLATES ---

# 1. Public API Page
HTML_HOME = """
<!DOCTYPE html>
<html>
<head>
    <title>Spidey FF Tools API</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { background-color: #121212; color: #00ff99; font-family: monospace; padding: 20px; }
        .container { max-width: 800px; margin: auto; }
        h1 { text-align: center; color: #ff3333; }
        .endpoint { background: #1e1e1e; padding: 15px; margin-bottom: 20px; border-radius: 8px; border: 1px solid #333; }
        .method { color: #ffff00; font-weight: bold; }
        a { color: #00ccff; text-decoration: none; }
        .btn { display: inline-block; padding: 10px 20px; background: #ff3333; color: white; border-radius: 5px; margin-top: 10px; }
        .footer { margin-top: 40px; text-align: center; font-size: 0.9em; color: #888; }
    </style>
</head>
<body>
    <div class="container">
        <h1>SPIDEY FF TOOLS API</h1>
        
        <div class="endpoint">
            <p>Welcome to the official API page. Below are the available endpoints.</p>
            <p style="color: #ffaa00;">Note: You need a valid API Key to use these tools. Contact Admin to buy keys.</p>
        </div>

        <h3>Endpoints</h3>

        <div class="endpoint">
            <span class="method">GET</span> /api/info<br>
            <small>Example: /api/info?uid=12345678&key=YOUR_KEY</small>
        </div>

        <div class="endpoint">
            <span class="method">GET</span> /api/emote<br>
            <small>Example: /api/emote?region=ind&teamcode=1234&uid=1234&emote_id=hello&key=YOUR_KEY</small>
        </div>

        <div class="endpoint">
            <span class="method">GET</span> /api/lag<br>
            <small>Example: /api/lag?region=ind&teamcode=1234&key=YOUR_KEY</small>
        </div>

        <div class="endpoint">
            <span class="method">GET</span> /api/5group<br>
            <small>Example: /api/5group?region=ind&uid=1234&key=YOUR_KEY</small>
        </div>
        
        <div class="endpoint">
            <span class="method">GET</span> /api/6group<br>
            <small>Example: /api/6group?region=ind&uid=1234&key=YOUR_KEY</small>
        </div>

        <div class="footer">
            <p>Contact Admin for API Key:</p>
            <a href="{{ tg_contact }}" class="btn">Telegram Admin</a><br><br>
            <a href="{{ tg_group }}">Join Group</a> | <a href="{{ tg_channel }}">Join Channel</a>
        </div>
    </div>
</body>
</html>
"""

# 2. Login Page
HTML_LOGIN = """
<!DOCTYPE html>
<html>
<head>
    <title>Admin Login</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { background-color: #000; color: white; font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .box { background: #1a1a1a; padding: 40px; border-radius: 10px; box-shadow: 0 0 20px #ff0000; text-align: center; }
        input { width: 100%; padding: 10px; margin: 10px 0; background: #333; border: none; color: white; border-radius: 5px; }
        button { width: 100%; padding: 10px; background: #ff0000; border: none; color: white; cursor: pointer; border-radius: 5px; font-weight: bold; }
        h2 { color: #ff0000; }
    </style>
</head>
<body>
    <div class="box">
        <h2>SECURE LOGIN</h2>
        <form action="/admin/login_action" method="POST">
            <input type="email" name="email" placeholder="Gmail" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">LOGIN</button>
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
        body { background-color: #121212; color: #ddd; font-family: monospace; padding: 20px; }
        h1 { color: #00ff99; }
        .panel { background: #1e1e1e; padding: 20px; border-radius: 8px; margin-bottom: 20px; border: 1px solid #333; }
        input, select { padding: 8px; background: #333; border: 1px solid #555; color: white; margin-right: 10px; }
        button { padding: 8px 15px; background: #00ccff; border: none; cursor: pointer; color: black; font-weight: bold; }
        .del-btn { background: #ff3333; color: white; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #333; padding: 10px; text-align: left; }
        th { color: #00ff99; }
    </style>
</head>
<body>
    <h1>Admin Panel: Spidey Tools</h1>
    <a href="/admin/logout" style="color: #ff3333;">Logout</a>
    
    <div class="panel">
        <h3>Create New API Key</h3>
        <form action="/admin/add_key" method="POST">
            <input type="text" name="new_key" placeholder="Enter New API Key" required>
            <br><br>
            <label>Expiry Date/Time (IST):</label>
            <input type="datetime-local" name="expiry_time" required>
            <button type="submit">Add Key</button>
        </form>
    </div>

    <div class="panel">
        <h3>Active Keys & Usage</h3>
        <table>
            <tr>
                <th>API Key</th>
                <th>Requests</th>
                <th>Expiry (IST)</th>
                <th>Status</th>
                <th>Action</th>
            </tr>
            {% for key, data in keys.items() %}
            <tr>
                <td>{{ key }}</td>
                <td>{{ data['requests'] }}</td>
                <td>{{ data['expiry'] }}</td>
                <td style="color: {{ 'red' if data['expired'] else '#00ff00' }}">
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
                <td>{{ master_key }}</td>
                <td>(Unlimited)</td>
                <td>NEVER</td>
                <td style="color: #00ff00">PERMANENT</td>
                <td>Cannot Delete</td>
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
    # 1. Check Master Key
    if key == MASTER_KEY:
        return True
    
    # 2. Check User Keys
    if key in api_keys:
        key_data = api_keys[key]
        current_time = get_ist_time()
        # Check Expiry
        if current_time > key_data['expiry']:
            return False # Expired
        
        # Valid: Increment Count
        api_keys[key]['requests'] += 1
        return True
    
    return False

def proxy_request(target_url, key):
    if not key:
        return Response("Error: Missing 'key' parameter.", status=401, mimetype='text/plain')

    if not is_key_valid(key):
        return Response("Error: Invalid or Expired API Key. Contact Admin: https://t.me/spidey_abd", status=403, mimetype='text/plain')

    try:
        response = requests.get(target_url)
        data = response.text
        # Append credit skipping one line
        final_output = data + "\n\nJSON credit: https://t.me/spidey_abd"
        return Response(final_output, mimetype='text/plain')
    except Exception as e:
        return Response(f"Internal Error: {str(e)}", status=500, mimetype='text/plain')

# --- ROUTES ---

# 1. Public Home Page
@app.route('/api', methods=['GET'])
def home():
    return render_template_string(HTML_HOME, tg_contact=TG_CONTACT, tg_group=TG_GROUP, tg_channel=TG_CHANNEL)

# 2. Admin Login Page
@app.route('/admin_734401', methods=['GET'])
def admin_login():
    if session.get('logged_in'):
        return redirect('/admin/dashboard')
    return render_template_string(HTML_LOGIN)

# 3. Login Action
@app.route('/admin/login_action', methods=['POST'])
def login_action():
    email = request.form.get('email')
    password = request.form.get('password')
    
    if email == ADMIN_EMAIL and password == ADMIN_PASS:
        session['logged_in'] = True
        return redirect('/admin/dashboard')
    else:
        return Response("Wrong Credentials. Access Denied.", status=403)

# 4. Admin Dashboard
@app.route('/admin/dashboard', methods=['GET'])
def dashboard():
    if not session.get('logged_in'):
        return redirect('/admin_734401')
    
    # Prepare data for display
    display_keys = {}
    now = get_ist_time()
    
    for k, v in api_keys.items():
        is_expired = now > v['expiry']
        display_keys[k] = {
            'requests': v['requests'],
            'expiry': v['expiry'].strftime('%Y-%m-%d %H:%M:%S'),
            'expired': is_expired
        }

    return render_template_string(HTML_DASHBOARD, keys=display_keys, master_key=MASTER_KEY)

# 5. Add Key
@app.route('/admin/add_key', methods=['POST'])
def add_key():
    if not session.get('logged_in'):
        return redirect('/admin_734401')
        
    new_key = request.form.get('new_key')
    expiry_str = request.form.get('expiry_time') # Format: 2023-12-30T15:00
    
    if new_key and expiry_str:
        # Convert HTML datetime input to Python datetime object (Naive)
        dt_naive = datetime.datetime.strptime(expiry_str, '%Y-%m-%dT%H:%M')
        # Localize to IST
        ist = pytz.timezone('Asia/Kolkata')
        dt_aware = ist.localize(dt_naive)
        
        api_keys[new_key] = {
            'expiry': dt_aware,
            'requests': 0
        }
        
    return redirect('/admin/dashboard')

# 6. Delete Key
@app.route('/admin/delete_key', methods=['POST'])
def delete_key():
    if not session.get('logged_in'):
        return redirect('/admin_734401')
    
    key_to_del = request.form.get('key_to_delete')
    if key_to_del in api_keys:
        del api_keys[key_to_del]
        
    return redirect('/admin/dashboard')

# 7. Logout
@app.route('/admin/logout')
def logout():
    session.pop('logged_in', None)
    return redirect('/api')

# --- API ENDPOINTS ---

@app.route('/api/info', methods=['GET'])
def api_info():
    uid = request.args.get('uid')
    key = request.args.get('key')
    if not uid: return Response("Missing uid", mimetype='text/plain')
    
    target = f"https://danger-info-alpha.vercel.app/accinfo?uid={uid}&key=DANGERxINFO"
    return proxy_request(target, key)

@app.route('/api/emote', methods=['GET'])
def api_emote():
    region = request.args.get('region')
    tc = request.args.get('teamcode')
    uid = request.args.get('uid')
    eid = request.args.get('emote_id')
    key = request.args.get('key')
    
    if not (region and tc and uid and eid): return Response("Missing parameters", mimetype='text/plain')
    
    target = f"https://proapi.sumittools.shop/emote?key=ShadowProTCP&region={region}&tc={tc}&uid1={uid}&emote_id={eid}"
    return proxy_request(target, key)

@app.route('/api/lag', methods=['GET'])
def api_lag():
    region = request.args.get('region')
    tc = request.args.get('teamcode')
    key = request.args.get('key')
    
    if not (region and tc): return Response("Missing parameters", mimetype='text/plain')
    
    target = f"https://proapi.sumittools.shop/lag?key=ShadowProTCP&region={region}&tc={tc}"
    return proxy_request(target, key)

@app.route('/api/5group', methods=['GET'])
def api_5group():
    region = request.args.get('region')
    uid = request.args.get('uid')
    key = request.args.get('key')
    
    if not (region and uid): return Response("Missing parameters", mimetype='text/plain')
    
    target = f"https://proapi.sumittools.shop/5group?key=ShadowProTCP&region={region}&uid={uid}"
    return proxy_request(target, key)

@app.route('/api/6group', methods=['GET'])
def api_6group():
    region = request.args.get('region')
    uid = request.args.get('uid')
    key = request.args.get('key')
    
    if not (region and uid): return Response("Missing parameters", mimetype='text/plain')
    
    target = f"https://proapi.sumittools.shop/6group?key=ShadowProTCP&region={region}&uid={uid}"
    return proxy_request(target, key)

# --- SECURITY "THIEF" PROTECTION ---
@app.route('/source')
@app.route('/.git')
@app.route('/app.py')
def security_check():
    return Response("Bhosdi Ke! Sudhar Ja", mimetype='text/plain')

# Entry point
app = app