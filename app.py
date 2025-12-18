from flask import Flask, request, Response, render_template_string, session, redirect, url_for
import requests
import datetime

app = Flask(__name__)
# REPLACE THIS WITH A RANDOM SECRET KEY
app.secret_key = "9693290244@gmail"

# --- CONFIGURATION ---
DOMAIN = "https://spidey-pro-tools.vercel.app"
ADMIN_ROUTE = "/admin_734401"
ADMIN_PASS = "7344010091@gmail"
TG_CREDIT = "\n\nCredit: https://t.me/spidey_abd"

# --- DEFAULT HTML TEMPLATES ---

# 1. MAIN PAGE (Professional Description & About Us)
DEFAULT_HOME = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Spidey Pro Tools</title>
    <style>
        body { background-color: #0d1117; color: #c9d1d9; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 0; line-height: 1.6; }
        header { background: #161b22; padding: 40px 20px; text-align: center; border-bottom: 1px solid #30363d; }
        h1 { color: #00ff99; margin: 0; font-size: 2.5em; letter-spacing: 2px; }
        .subtitle { color: #8b949e; margin-top: 10px; font-size: 1.1em; }
        .container { max-width: 900px; margin: 40px auto; padding: 0 20px; }
        .section { background: #161b22; padding: 30px; border-radius: 8px; border: 1px solid #30363d; margin-bottom: 30px; }
        h2 { color: #58a6ff; border-bottom: 1px solid #30363d; padding-bottom: 10px; margin-top: 0; }
        .btn-group { text-align: center; margin: 30px 0; }
        .btn { display: inline-block; padding: 12px 30px; font-size: 1.1em; font-weight: bold; text-decoration: none; border-radius: 6px; margin: 10px; transition: 0.3s; }
        .btn-green { background: #238636; color: white; }
        .btn-green:hover { background: #2ea043; }
        .btn-blue { background: #1f6feb; color: white; }
        .btn-blue:hover { background: #388bfd; }
        footer { text-align: center; padding: 20px; border-top: 1px solid #30363d; color: #8b949e; font-size: 0.9em; margin-top: 50px; }
        a { color: #58a6ff; text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <header>
        <h1>SPIDEY PRO TOOLS</h1>
        <div class="subtitle">Premium API Solutions for Developers & Gamers</div>
    </header>

    <div class="container">
        <!-- Action Buttons -->
        <div class="btn-group">
            <a href="/api" class="btn btn-green">🚀 Visit API Page</a>
            <a href="https://spidyai.rf.gd/I2U" class="btn btn-blue">🖼️ Image To URL</a>
        </div>

        <!-- Description Section -->
        <div class="section">
            <h2>Description</h2>
            <p>Welcome to <strong>Spidey Pro Tools</strong>. This platform provides high-performance, low-latency APIs designed for Free Fire tools, gaming utilities, and automation tasks. Our endpoints are secured, reliable, and constantly updated to ensure 99.9% uptime.</p>
        </div>

        <!-- About Us Section -->
        <div class="section">
            <h2>About Us</h2>
            <p>We are a team of passionate developers dedicated to creating open and accessible tools for the community. With years of experience in backend development and reverse engineering, we bring you the best tools in the market.</p>
            <p>
                <strong>Admin:</strong> Spidey Abd<br>
                <strong>Contact:</strong> <a href="https://t.me/spidey_abd">@spidey_abd</a>
            </p>
        </div>
    </div>

    <footer>
        &copy; 2025 Spidey Pro Tools. All Rights Reserved.<br>
        Powered by Vercel & Python.
    </footer>
</body>
</html>
"""

# 2. API PAGE (Dark Hacker Theme with Full URLs)
DEFAULT_API_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Spidey API Documentation</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { background-color: #0d1117; color: #c9d1d9; font-family: 'Consolas', 'Monaco', monospace; margin: 0; padding: 20px; }
        .container { max-width: 950px; margin: auto; }
        h1 { color: #00ff99; text-align: center; text-transform: uppercase; border-bottom: 2px solid #30363d; padding-bottom: 15px; margin-bottom: 30px; }
        .back-link { display: block; text-align: center; margin-bottom: 30px; color: #58a6ff; text-decoration: none; }
        
        .endpoint-card { background: #161b22; border: 1px solid #30363d; border-radius: 8px; margin-bottom: 25px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
        .card-header { background: #21262d; padding: 12px 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #30363d; }
        .method { background: #00ff99; color: #000; padding: 3px 8px; border-radius: 4px; font-weight: bold; font-size: 0.8em; margin-right: 10px; }
        .ep-title { color: #fff; font-weight: bold; font-size: 1.1em; }
        .security { font-size: 0.8em; font-weight: bold; padding: 3px 8px; border-radius: 4px; }
        .sec-key { background: #da3633; color: white; }
        .sec-free { background: #238636; color: white; }
        
        .card-body { padding: 20px; }
        .desc { color: #8b949e; margin-bottom: 15px; font-family: sans-serif; }
        .label { font-size: 0.75em; text-transform: uppercase; color: #58a6ff; letter-spacing: 1px; margin-bottom: 5px; }
        .url-box { background: #000; color: #00ff99; padding: 12px; border-radius: 6px; border: 1px solid #333; word-break: break-all; font-size: 0.95em; position: relative; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Available Endpoints</h1>
        <a href="/" class="back-link">&larr; Back to Main Website</a>

        {% for route, data in endpoints.items() %}
        <div class="endpoint-card">
            <div class="card-header">
                <div>
                    <span class="method">GET</span>
                    <span class="ep-title">{{ data.title }}</span>
                </div>
                <div>
                    {% if data.require_key %}
                        <span class="security sec-key">KEY REQUIRED</span>
                    {% else %}
                        <span class="security sec-free">FREE ACCESS</span>
                    {% endif %}
                </div>
            </div>
            <div class="card-body">
                <div class="desc">{{ data.desc }}</div>
                
                <div class="label">Request URL</div>
                <div class="url-box">
                    {{ domain }}/api/{{ route }}?{{ data.params }}{% if data.require_key %}&key={apikey}{% endif %}
                </div>
            </div>
        </div>
        {% endfor %}
        
        <p style="text-align:center; color:#58a6ff; margin-top:50px;">
            <a href="{{ admin_route }}" style="color:#30363d; text-decoration:none;">Admin Login</a>
        </p>
    </div>
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
        "SpideyTCPTools": {
            "requests": 0,
            "limit_req": -1,       
            "limit_users": -1,     
            "limit_time": None,    
            "used_by": []          
        }
    },
    "endpoints": {
        # Format: "route": {target, title, desc, params, require_key, requests}
        "info": {
            "target": "https://danger-info-alpha.vercel.app/accinfo?uid={uid}&key=DANGERxINFO",
            "title": "Account Info",
            "desc": "Retrieve Full Account Details via UID.",
            "params": "uid={uid}",
            "require_key": True,
            "requests": 0
        }
    }
}

# --- HELPER FUNCTIONS ---

def check_key(key, uid_or_ip):
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
            if len(k_data['used_by']) >= k_data['limit_users']:
                return False, "User Limit Reached for this Key"
            k_data['used_by'].append(uid_or_ip)

    k_data['requests'] += 1
    return True, "OK"

# --- ROUTES: PUBLIC ---

@app.route('/')
def index():
    return render_template_string(DATA['config']['home_html'])

@app.route('/api')
def api_docs():
    return render_template_string(
        DATA['config']['api_html'], 
        endpoints=DATA['endpoints'], 
        domain=DOMAIN,
        admin_route=ADMIN_ROUTE
    )

@app.route('/api/<path:route>')
def proxy(route):
    ep = DATA['endpoints'].get(route)
    if not ep:
        return Response("Error: Endpoint not found.", status=404, mimetype='text/plain')

    if ep['require_key']:
        key = request.args.get('key')
        if not key:
            return Response("Error: API Key Required.", status=401, mimetype='text/plain')
        
        user_id = request.args.get('uid') or request.remote_addr
        valid, msg = check_key(key, user_id)
        if not valid:
            return Response(f"Error: {msg}", status=403, mimetype='text/plain')

    ep['requests'] += 1

    try:
        target_url = ep['target'].format(**request.args.to_dict())
        r = requests.get(target_url)
        return Response(r.text + TG_CREDIT, mimetype='text/plain')
    except Exception as e:
        return Response(f"Request Error: {str(e)}", status=500, mimetype='text/plain')

# --- ROUTES: ADMIN ---

@app.route(ADMIN_ROUTE, methods=['GET', 'POST'])
def admin_panel():
    if session.get('logged_in'):
        return render_template_string(HTML_ADMIN, data=DATA, domain=DOMAIN)
    
    if request.method == 'POST':
        if request.form.get('password') == ADMIN_PASS:
            session['logged_in'] = True
            return redirect(ADMIN_ROUTE)
    
    return render_template_string(HTML_LOGIN)

@app.route('/admin/action', methods=['POST'])
def admin_action():
    if not session.get('logged_in'): return redirect(ADMIN_ROUTE)
    
    act = request.form.get('action')
    
    if act == 'add_endpoint':
        route = request.form.get('route').strip('/')
        DATA['endpoints'][route] = {
            "target": request.form.get('target'),
            "title": request.form.get('title'),
            "desc": request.form.get('desc'),
            "params": request.form.get('params'), # New field
            "require_key": request.form.get('req_key') == 'on',
            "requests": 0
        }
    elif act == 'del_endpoint':
        route = request.form.get('route')
        if route in DATA['endpoints']: del DATA['endpoints'][route]
    elif act == 'add_key':
        k = request.form.get('key_name')
        l_req = int(request.form.get('limit_req')) if request.form.get('limit_req') else -1
        l_users = int(request.form.get('limit_users')) if request.form.get('limit_users') else -1
        l_time = request.form.get('limit_time') if request.form.get('limit_time') else None
        DATA['api_keys'][k] = {"requests": 0, "limit_req": l_req, "limit_users": l_users, "limit_time": l_time, "used_by": []}
    elif act == 'del_key':
        k = request.form.get('key')
        if k in DATA['api_keys']: del DATA['api_keys'][k]
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
        .url-preview{font-size:0.8em;color:#888;}
    </style>
</head>
<body>
    <div style="display:flex;justify-content:space-between;">
        <h1>SPIDEY PRO ADMIN</h1>
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
            <button>Add Key</button>
        </form>
        <br>
        <table>
            <tr><th>Key</th><th>Requests</th><th>User Limit</th><th>Expiry</th><th>Action</th></tr>
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
                        <button class="del">Delete</button>
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
                <input type="text" name="params" placeholder="Usage Params (e.g. prompt={text})" style="flex:2;">
                <input type="text" name="target" placeholder="Target External URL" required style="flex:3;">
            </div>
            <div class="row">
                <input type="text" name="title" placeholder="Title (e.g. AI Chat)" required>
                <input type="text" name="desc" placeholder="Short Description">
            </div>
            <label style="display:inline-block;padding:10px;">
                <input type="checkbox" name="req_key" style="width:auto;"> Require API Key?
            </label>
            <br>
            <button>Add Endpoint</button>
        </form>
        <br>
        <table>
            <tr><th>Route</th><th>Title</th><th>Preview</th><th>Hits</th><th>Action</th></tr>
            {% for r, v in data.endpoints.items() %}
            <tr>
                <td>{{ r }}</td>
                <td>{{ v.title }}</td>
                <td class="url-preview">
                    {{ domain }}/api/{{ r }}?{{ v.params }}{{ '&key={key}' if v.require_key else '' }}
                </td>
                <td>{{ v.requests }}</td>
                <td>
                    <form action="/admin/action" method="POST" style="display:inline;">
                        <input type="hidden" name="action" value="del_endpoint">
                        <input type="hidden" name="route" value="{{ r }}">
                        <button class="del">Delete</button>
                    </form>
                </td>
            </tr>
            {% endfor %}
        </table>
    </div>

    <!-- 3. PAGE EDITOR -->
    <div class="panel">
        <h2>📝 HTML Editor</h2>
        <h3>Home Page (/)</h3>
        <form action="/admin/action" method="POST">
            <input type="hidden" name="action" value="save_html">
            <input type="hidden" name="page" value="home_html">
            <textarea name="content" rows="6">{{ data.config.home_html }}</textarea>
            <button>Save Home</button>
        </form>
        <h3>API Page (/api)</h3>
        <form action="/admin/action" method="POST">
            <input type="hidden" name="action" value="save_html">
            <input type="hidden" name="page" value="api_html">
            <textarea name="content" rows="6">{{ data.config.api_html }}</textarea>
            <button>Save Docs</button>
        </form>
    </div>
</body>
</html>
"""

if __name__ == '__main__':
    app.run()