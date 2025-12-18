from flask import Flask, request, Response, render_template_string, session, redirect, url_for
import requests
import datetime

app = Flask(__name__)
app.secret_key = "SPIDEY_ULTRA_SECRET"

# --- CONFIGURATION ---
ADMIN_ROUTE = "/admin_734401"
ADMIN_USER = "admin" # Not used, just logic placeholder
ADMIN_PASS = "7344010091@gmail"
TG_CREDIT = "\n\nCredit: https://t.me/spidey_abd"

# --- DEFAULT HTML TEMPLATES (You can edit these in Admin Panel) ---
DEFAULT_HOME = """
<!DOCTYPE html>
<html>
<head>
    <title>Spidey FF Tools</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body{background:#0d1117;color:#c9d1d9;font-family:sans-serif;padding:0;margin:0;display:flex;flex-direction:column;min-height:100vh;}
        header{background:#161b22;padding:20px;text-align:center;border-bottom:1px solid #30363d;}
        h1{color:#00ff99;margin:0;}
        .container{max-width:800px;margin:40px auto;padding:20px;text-align:center;}
        .btn{display:inline-block;padding:15px 30px;background:#238636;color:white;text-decoration:none;border-radius:6px;font-weight:bold;margin:10px;}
        .btn-blue{background:#1f6feb;}
        footer{margin-top:auto;text-align:center;padding:20px;color:#8b949e;border-top:1px solid #30363d;}
    </style>
</head>
<body>
    <header><h1>SPIDEY FF TOOLS</h1></header>
    <div class="container">
        <h2>Welcome to the Official Tool Site</h2>
        <p>Your one-stop destination for Free Fire Tools and APIs.</p>
        <br>
        <a href="/api" class="btn">🚀 Visit API Page</a>
        <a href="https://spidyai.rf.gd/I2U" class="btn btn-blue">🖼️ Image To URL</a>
        <br><br>
        <h3>About Me</h3>
        <p>Developer by passion. Providing high quality APIs for the community.</p>
        <p>Contact: <a href="https://t.me/spidey_abd" style="color:#58a6ff;">@spidey_abd</a></p>
    </div>
    <footer>&copy; 2025 Spidey Tools</footer>
</body>
</html>
"""

DEFAULT_API_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Spidey API Docs</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body{background:#0d1117;color:#c9d1d9;font-family:monospace;padding:20px;max-width:900px;margin:auto;}
        h1{color:#00ff99;text-align:center;border-bottom:1px solid #30363d;padding-bottom:10px;}
        .card{background:#161b22;border:1px solid #30363d;padding:20px;margin-bottom:20px;border-radius:8px;}
        .title{color:#58a6ff;font-size:1.2em;font-weight:bold;margin-bottom:5px;}
        .desc{color:#8b949e;margin-bottom:15px;font-family:sans-serif;}
        .url{background:#000;color:#00ff99;padding:12px;word-break:break-all;border-radius:4px;border:1px solid #333;}
        .tag{display:inline-block;padding:2px 6px;font-size:0.8em;border-radius:4px;margin-left:10px;}
        .tag-free{background:#238636;color:white;}
        .tag-key{background:#da3633;color:white;}
    </style>
</head>
<body>
    <h1>AVAILABLE APIs</h1>
    <div style="text-align:center;margin-bottom:20px;">
        <a href="/" style="color:#58a6ff;">&larr; Back Home</a>
    </div>

    <!-- The endpoint list is injected here by Python -->
    {% for route, data in endpoints.items() %}
    <div class="card">
        <div class="title">
            {{ data.title }}
            {% if data.require_key %}
                <span class="tag tag-key">Key Required</span>
            {% else %}
                <span class="tag tag-free">Free</span>
            {% endif %}
        </div>
        <div class="desc">{{ data.desc }}</div>
        <div class="url">https://spidey-ff-tools.vercel.app/api/{{ route }}</div>
    </div>
    {% endfor %}
</body>
</html>
"""

# --- IN-MEMORY DATA ---
DATA = {
    "config": {
        "home_html": DEFAULT_HOME,
        "api_html": DEFAULT_API_PAGE
    },
    "api_keys": {
        # Format: "KeyName": {requests, limit_req, limit_users, limit_time, used_by_uids}
        "SpideyTCPTools": {
            "requests": 0,
            "limit_req": -1,       # -1 = Unlimited
            "limit_users": -1,     # -1 = Unlimited
            "limit_time": None,    # None = Lifetime
            "used_by": []          # List of UIDs/IPs
        }
    },
    "endpoints": {
        # Format: "route": {target, title, desc, require_key, requests}
        "info": {
            "target": "https://danger-info-alpha.vercel.app/accinfo?uid={uid}&key=DANGERxINFO",
            "title": "Account Info",
            "desc": "Get FF Account details using UID.",
            "require_key": True,
            "requests": 0
        }
    }
}

# --- HELPER FUNCTIONS ---

def check_key(key, uid_or_ip):
    """Checks if key is valid based on all limits."""
    if key not in DATA['api_keys']:
        return False, "Invalid Key"
    
    k_data = DATA['api_keys'][key]

    # 1. Check Time Limit
    if k_data['limit_time']:
        try:
            exp_date = datetime.datetime.fromisoformat(k_data['limit_time'])
            if datetime.datetime.now() > exp_date:
                return False, "Key Expired"
        except: pass

    # 2. Check Request Limit
    if k_data['limit_req'] != -1 and k_data['requests'] >= k_data['limit_req']:
        return False, "Request Limit Reached"

    # 3. Check User Limit
    if k_data['limit_users'] != -1:
        if uid_or_ip not in k_data['used_by']:
            # New user trying to use key
            if len(k_data['used_by']) >= k_data['limit_users']:
                return False, "User Limit Reached for this Key"
            # Add new user
            k_data['used_by'].append(uid_or_ip)

    # All good, increment requests
    k_data['requests'] += 1
    return True, "OK"

# --- ROUTES: PUBLIC ---

@app.route('/')
def index():
    return render_template_string(DATA['config']['home_html'])

@app.route('/api')
def api_docs():
    return render_template_string(DATA['config']['api_html'], endpoints=DATA['endpoints'])

@app.route('/api/<path:route>')
def proxy(route):
    # 1. Find Endpoint
    ep = DATA['endpoints'].get(route)
    if not ep:
        return Response("Error: Endpoint not found.", status=404, mimetype='text/plain')

    # 2. Check Security (If Key Required)
    if ep['require_key']:
        key = request.args.get('key')
        if not key:
            return Response("Error: API Key Required.", status=401, mimetype='text/plain')
        
        # Identify User (UID param or IP)
        user_id = request.args.get('uid') or request.remote_addr
        
        valid, msg = check_key(key, user_id)
        if not valid:
            return Response(f"Error: {msg}", status=403, mimetype='text/plain')

    # 3. Update Stats
    ep['requests'] += 1

    # 4. Proxy Request
    try:
        # Format URL
        target_url = ep['target'].format(**request.args.to_dict())
        r = requests.get(target_url)
        return Response(r.text + TG_CREDIT, mimetype='text/plain')
    except Exception as e:
        return Response(f"Request Error: {str(e)}", status=500, mimetype='text/plain')

# --- ROUTES: ADMIN ---

@app.route(ADMIN_ROUTE, methods=['GET', 'POST'])
def admin_panel():
    if session.get('logged_in'):
        return render_template_string(HTML_ADMIN, data=DATA)
    
    if request.method == 'POST':
        if request.form.get('password') == ADMIN_PASS:
            session['logged_in'] = True
            return redirect(ADMIN_ROUTE)
    
    return render_template_string(HTML_LOGIN)

@app.route('/admin/action', methods=['POST'])
def admin_action():
    if not session.get('logged_in'): return redirect(ADMIN_ROUTE)
    
    act = request.form.get('action')
    
    # --- ENDPOINT ACTIONS ---
    if act == 'add_endpoint':
        route = request.form.get('route').strip('/')
        DATA['endpoints'][route] = {
            "target": request.form.get('target'),
            "title": request.form.get('title'),
            "desc": request.form.get('desc'),
            "require_key": request.form.get('req_key') == 'on',
            "requests": 0
        }
    
    elif act == 'del_endpoint':
        route = request.form.get('route')
        if route in DATA['endpoints']: del DATA['endpoints'][route]

    # --- KEY ACTIONS ---
    elif act == 'add_key':
        k = request.form.get('key_name')
        
        # Parse Limits
        l_req = int(request.form.get('limit_req')) if request.form.get('limit_req') else -1
        l_users = int(request.form.get('limit_users')) if request.form.get('limit_users') else -1
        l_time = request.form.get('limit_time') if request.form.get('limit_time') else None

        # Create/Update Key
        DATA['api_keys'][k] = {
            "requests": 0,
            "limit_req": l_req,
            "limit_users": l_users,
            "limit_time": l_time,
            "used_by": []
        }

    elif act == 'del_key':
        k = request.form.get('key')
        if k in DATA['api_keys']: del DATA['api_keys'][k]

    # --- PAGE ACTIONS ---
    elif act == 'save_html':
        p = request.form.get('page')
        content = request.form.get('content')
        if p in DATA['config']: DATA['config'][p] = content

    return redirect(ADMIN_ROUTE)

@app.route('/admin/logout')
def logout():
    session.pop('logged_in', None)
    return redirect('/')

# --- ADMIN TEMPLATES ---

HTML_LOGIN = """
<body style="background:#000;display:flex;justify-content:center;align-items:center;height:100vh;">
    <form method="POST" style="border:1px solid #0f0;padding:40px;text-align:center;">
        <h2 style="color:#0f0;font-family:monospace;">ADMIN LOGIN</h2>
        <input type="password" name="password" placeholder="Password" style="padding:10px;">
        <br><br><button style="background:#0f0;border:none;padding:10px 20px;cursor:pointer;">ENTER</button>
    </form>
</body>
"""

HTML_ADMIN = """
<!DOCTYPE html>
<html>
<head>
    <title>Spidey Admin</title>
    <style>
        body{background:#111;color:#eee;font-family:sans-serif;padding:20px;max-width:1200px;margin:auto;}
        .panel{background:#222;padding:20px;margin-bottom:20px;border-radius:8px;border:1px solid #444;}
        h2{color:#00ccff;border-bottom:1px solid #444;padding-bottom:10px;}
        input, textarea, select{background:#000;color:#fff;border:1px solid #555;padding:8px;margin:5px 0;width:100%;box-sizing:border-box;}
        .row{display:flex;gap:10px;}
        button{background:#0070f3;color:white;border:none;padding:10px 15px;cursor:pointer;border-radius:4px;}
        .del{background:#e00;}
        table{width:100%;border-collapse:collapse;margin-top:10px;}
        th,td{border:1px solid #444;padding:8px;text-align:left;font-size:0.9em;}
        th{color:#00ccff;}
        .tag{padding:2px 5px;border-radius:3px;font-size:0.8em;}
    </style>
</head>
<body>
    <div style="display:flex;justify-content:space-between;">
        <h1>SPIDEY ADMIN PANEL</h1>
        <a href="/admin/logout" style="color:#e00;">Logout</a>
    </div>

    <!-- 1. API KEYS -->
    <div class="panel">
        <h2>🔑 API Keys Management</h2>
        <form action="/admin/action" method="POST">
            <input type="hidden" name="action" value="add_key">
            <div class="row">
                <input type="text" name="key_name" placeholder="Key Name" required>
                <input type="number" name="limit_req" placeholder="Max Requests (-1 for Unlimited)">
                <input type="number" name="limit_users" placeholder="Max Users (-1 for Unlimited)">
                <input type="datetime-local" name="limit_time" title="Expiry Date">
            </div>
            <br>
            <button>Save / Update Key</button>
        </form>
        <br>
        <table>
            <tr><th>Key</th><th>Used / Limit</th><th>Users / Limit</th><th>Expiry</th><th>Action</th></tr>
            {% for k, v in data.api_keys.items() %}
            <tr>
                <td>{{ k }}</td>
                <td>{{ v.requests }} / {{ '∞' if v.limit_req == -1 else v.limit_req }}</td>
                <td>{{ v.used_by|length }} / {{ '∞' if v.limit_users == -1 else v.limit_users }}</td>
                <td>{{ v.limit_time if v.limit_time else 'Lifetime' }}</td>
                <td>
                    <form action="/admin/action" method="POST" style="display:inline;">
                        <input type="hidden" name="action" value="del_key">
                        <input type="hidden" name="key" value="{{ k }}">
                        <button class="del">Del</button>
                    </form>
                </td>
            </tr>
            {% endfor %}
        </table>
    </div>

    <!-- 2. ENDPOINTS -->
    <div class="panel">
        <h2>🔗 Endpoints Management</h2>
        <form action="/admin/action" method="POST">
            <input type="hidden" name="action" value="add_endpoint">
            <div class="row">
                <input type="text" name="route" placeholder="Route (e.g. ai)" required style="flex:1;">
                <input type="text" name="target" placeholder="Target URL (e.g. https://api.com?q={ask})" required style="flex:3;">
            </div>
            <div class="row">
                <input type="text" name="title" placeholder="Title (e.g. AI Chat)" required>
                <input type="text" name="desc" placeholder="Short Description">
            </div>
            <label style="display:inline-block;padding:10px;">
                <input type="checkbox" name="req_key" style="width:auto;"> Require API Key?
            </label>
            <button>Save / Update Endpoint</button>
        </form>
        <br>
        <table>
            <tr><th>Route</th><th>Title</th><th>Security</th><th>Hits</th><th>Action</th></tr>
            {% for r, v in data.endpoints.items() %}
            <tr>
                <td>/api/{{ r }}</td>
                <td>{{ v.title }}</td>
                <td>{{ '🔒 Private' if v.require_key else '🌍 Public' }}</td>
                <td>{{ v.requests }}</td>
                <td>
                    <form action="/admin/action" method="POST" style="display:inline;">
                        <input type="hidden" name="action" value="del_endpoint">
                        <input type="hidden" name="route" value="{{ r }}">
                        <button class="del">Del</button>
                    </form>
                </td>
            </tr>
            {% endfor %}
        </table>
    </div>

    <!-- 3. PAGE EDITOR -->
    <div class="panel">
        <h2>📝 Page HTML Editor</h2>
        
        <h3>Edit Home Page (/)</h3>
        <form action="/admin/action" method="POST">
            <input type="hidden" name="action" value="save_html">
            <input type="hidden" name="page" value="home_html">
            <textarea name="content" rows="10">{{ data.config.home_html }}</textarea>
            <button>Save Home Page</button>
        </form>
        
        <h3>Edit API Docs Page (/api)</h3>
        <form action="/admin/action" method="POST">
            <input type="hidden" name="action" value="save_html">
            <input type="hidden" name="page" value="api_html">
            <textarea name="content" rows="10">{{ data.config.api_html }}</textarea>
            <button>Save API Page</button>
        </form>
    </div>
</body>
</html>
"""

if __name__ == '__main__':
    app.run()