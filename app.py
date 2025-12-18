from flask import Flask, request, Response, render_template_string, session, redirect, url_for
import requests

app = Flask(__name__)
app.secret_key = "SPIDEY_SECRET_KEY_7344"

# --- CONFIGURATION ---
ADMIN_ROUTE = "/admin_734401" # The Secret URL
ADMIN_PASS = "7344010091"     # Your Password
TG_CONTACT = "https://t.me/spidey_abd"

# --- IN-MEMORY DATA STORAGE ---
# WARNING: On Vercel Free Tier, keys added via the panel will be reset
# when the server sleeps (approx 10-15 mins of inactivity).
# To make a key PERMANENT, add it inside this dictionary code.

DATA = {
    "api_keys": {
        "SpideyTCPTools": {"requests": 0, "active": True} 
    },
    "endpoints": {
        "info": "https://danger-info-alpha.vercel.app/accinfo?uid={uid}&key=DANGERxINFO",
        "emote": "https://proapi.sumittools.shop/emote?key=ShadowProTCP&region={region}&tc={teamcode}&uid1={uid}&emote_id={emote_id}",
        "lag": "https://proapi.sumittools.shop/lag?key=ShadowProTCP&region={region}&tc={teamcode}",
        "5group": "https://proapi.sumittools.shop/5group?key=ShadowProTCP&region={region}&uid={uid}",
        "6group": "https://proapi.sumittools.shop/6group?key=ShadowProTCP&region={region}&uid={uid}"
    }
}

# --- HTML: PUBLIC PAGE (Clean, No Admin Link) ---
HTML_PUBLIC = """
<!DOCTYPE html>
<html>
<head>
    <title>Spidey FF Tools</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body{background:#0d1117;color:#c9d1d9;font-family:monospace;padding:20px;max-width:800px;margin:auto;}
        h1{color:#00ff99;text-align:center;border-bottom:1px solid #30363d;padding-bottom:10px;}
        .card{background:#161b22;border:1px solid #30363d;padding:15px;margin-bottom:20px;border-radius:6px;}
        .label{color:#8b949e;font-size:0.9em;margin-bottom:5px;}
        .url{background:#000;color:#58a6ff;padding:10px;word-break:break-all;border-radius:4px;border:1px solid #333;}
        .footer{text-align:center;margin-top:40px;border-top:1px solid #30363d;padding-top:20px;color:#8b949e;}
        a{color:#00ff99;text-decoration:none;}
    </style>
</head>
<body>
    <h1>SPIDEY FF TOOLS API</h1>
    <p style="text-align:center;">Status: <span style="color:#2ea043;">ONLINE</span></p>

    {% for name, target in endpoints.items() %}
    <div class="card">
        <div class="label">ENDPOINT: <strong>/api/{{ name }}</strong></div>
        <div class="url">https://spidey-ff-tools.vercel.app/api/{{ name }}?key=YOUR_KEY&...</div>
    </div>
    {% endfor %}

    <div class="footer">
        Contact Admin: <a href="{{ contact }}">{{ contact }}</a>
    </div>
</body>
</html>
"""

# --- HTML: SECRET ADMIN LOGIN ---
HTML_LOGIN = """
<!DOCTYPE html>
<html>
<head>
    <title>Restricted Access</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body{background:#000;color:#0f0;display:flex;justify-content:center;align-items:center;height:100vh;font-family:monospace;margin:0;}
        .box{border:1px solid #0f0;padding:40px;text-align:center;box-shadow:0 0 20px #0f0;}
        input{background:#111;border:1px solid #0f0;color:#fff;padding:10px;width:200px;text-align:center;}
        button{background:#0f0;color:#000;border:none;padding:10px 20px;font-weight:bold;cursor:pointer;margin-top:10px;}
    </style>
</head>
<body>
    <div class="box">
        <h2>SYSTEM LOCKED</h2>
        <form method="POST">
            <input type="password" name="password" placeholder="ENTER PASSWORD" required>
            <br>
            <button>UNLOCK</button>
        </form>
    </div>
</body>
</html>
"""

# --- HTML: ADMIN DASHBOARD (Manage Keys/Endpoints) ---
HTML_DASHBOARD = """
<!DOCTYPE html>
<html>
<head>
    <title>Admin Control Panel</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body{background:#111;color:#eee;font-family:sans-serif;padding:20px;max-width:1000px;margin:auto;}
        h1{color:#00ccff;}
        .panel{background:#222;padding:20px;border-radius:8px;margin-bottom:20px;border:1px solid #333;}
        input{padding:8px;background:#000;border:1px solid #555;color:#fff;border-radius:4px;}
        button{padding:8px 15px;cursor:pointer;background:#0070f3;color:#fff;border:none;border-radius:4px;font-weight:bold;}
        .del-btn{background:#e00;}
        table{width:100%;border-collapse:collapse;margin-top:15px;}
        th,td{border:1px solid #444;padding:10px;text-align:left;}
        th{background:#1a1a1a;color:#00ccff;}
        code{background:#000;color:#0ff;padding:2px 4px;}
        .logout{float:right;color:#e00;text-decoration:none;border:1px solid #e00;padding:5px 10px;border-radius:4px;}
    </style>
</head>
<body>
    <a href="/admin/logout" class="logout">Logout</a>
    <h1>ADMIN DASHBOARD</h1>

    <!-- SECTION 1: API KEYS -->
    <div class="panel">
        <h3>🔑 API Keys</h3>
        <form action="/admin/add_key" method="POST">
            <input type="text" name="key_name" placeholder="New Key Name" required>
            <button>+ Add Key</button>
        </form>
        <table>
            <tr><th>Key</th><th>Requests</th><th>Action</th></tr>
            {% for key, info in data.api_keys.items() %}
            <tr>
                <td>{{ key }}</td>
                <td>{{ info.requests }}</td>
                <td>
                    <form action="/admin/del_key" method="POST" style="display:inline;">
                        <input type="hidden" name="key" value="{{ key }}">
                        <button class="del-btn">Remove</button>
                    </form>
                </td>
            </tr>
            {% endfor %}
        </table>
    </div>

    <!-- SECTION 2: ENDPOINTS -->
    <div class="panel">
        <h3>🔗 Dynamic Endpoints</h3>
        <p style="font-size:0.9em;color:#aaa;">
            Use <code>{param}</code> placeholders.<br>
            Ex: <code>https://api.com?uid={uid}</code>
        </p>
        <form action="/admin/add_endpoint" method="POST" style="display:flex; gap:10px;">
            <input type="text" name="route" placeholder="Route (e.g. skin)" required style="flex:1;">
            <input type="text" name="target" placeholder="Target URL" required style="flex:3;">
            <button>+ Add Endpoint</button>
        </form>
        <table>
            <tr><th>Route Name</th><th>Target URL</th><th>Action</th></tr>
            {% for route, url in data.endpoints.items() %}
            <tr>
                <td><span style="color:#0f0;">/api/{{ route }}</span></td>
                <td style="font-size:0.85em;word-break:break-all;">{{ url }}</td>
                <td>
                    <form action="/admin/del_endpoint" method="POST" style="display:inline;">
                        <input type="hidden" name="route" value="{{ route }}">
                        <button class="del-btn">Remove</button>
                    </form>
                </td>
            </tr>
            {% endfor %}
        </table>
    </div>
</body>
</html>
"""

# --- ROUTES: PUBLIC ---

@app.route('/')
def home():
    # Shows the clean public page
    return render_template_string(HTML_PUBLIC, endpoints=DATA['endpoints'], contact=TG_CONTACT)

# --- ROUTES: ADMIN ---

@app.route(ADMIN_ROUTE, methods=['GET', 'POST'])
def admin_page():
    if session.get('logged_in'):
        return render_template_string(HTML_DASHBOARD, data=DATA)
    
    if request.method == 'POST':
        if request.form.get('password') == ADMIN_PASS:
            session['logged_in'] = True
            return redirect(ADMIN_ROUTE)
    
    return render_template_string(HTML_LOGIN)

@app.route('/admin/logout')
def logout():
    session.pop('logged_in', None)
    return redirect('/')

# --- ROUTES: ADMIN ACTIONS ---

@app.route('/admin/add_key', methods=['POST'])
def add_key():
    if not session.get('logged_in'): return redirect(ADMIN_ROUTE)
    k = request.form.get('key_name')
    if k: DATA['api_keys'][k] = {"requests": 0, "active": True}
    return redirect(ADMIN_ROUTE)

@app.route('/admin/del_key', methods=['POST'])
def del_key():
    if not session.get('logged_in'): return redirect(ADMIN_ROUTE)
    k = request.form.get('key')
    if k in DATA['api_keys']: del DATA['api_keys'][k]
    return redirect(ADMIN_ROUTE)

@app.route('/admin/add_endpoint', methods=['POST'])
def add_endpoint():
    if not session.get('logged_in'): return redirect(ADMIN_ROUTE)
    r = request.form.get('route')
    t = request.form.get('target')
    if r and t: DATA['endpoints'][r] = t
    return redirect(ADMIN_ROUTE)

@app.route('/admin/del_endpoint', methods=['POST'])
def del_endpoint():
    if not session.get('logged_in'): return redirect(ADMIN_ROUTE)
    r = request.form.get('route')
    if r in DATA['endpoints']: del DATA['endpoints'][r]
    return redirect(ADMIN_ROUTE)

# --- ROUTES: API PROXY LOGIC ---

@app.route('/api/<path:endpoint>')
def proxy_handler(endpoint):
    # 1. Validate Endpoint
    target = DATA['endpoints'].get(endpoint)
    if not target:
        return Response("Error: Endpoint not found.", status=404, mimetype='text/plain')

    # 2. Validate Key
    key = request.args.get('key')
    if not key or key not in DATA['api_keys']:
        return Response(f"Error: Invalid API Key.\nContact: {TG_CONTACT}", status=403, mimetype='text/plain')

    # 3. Increment Count
    DATA['api_keys'][key]['requests'] += 1

    # 4. Format URL
    params = request.args.to_dict()
    try:
        final_url = target.format(**params)
    except Exception as e:
        return Response(f"Error: Missing parameter {str(e)}", status=400, mimetype='text/plain')

    # 5. Fetch
    try:
        r = requests.get(final_url)
        return Response(r.text + f"\n\nJSON credit: {TG_CONTACT}", mimetype='text/plain')
    except Exception as e:
        return Response(f"Internal Error: {str(e)}", status=500, mimetype='text/plain')

# --- SECURITY ---
@app.route('/app.py')
@app.route('/vercel.json')
def block_thief():
    return Response("You are Thief", status=403, mimetype='text/plain')

if __name__ == '__main__':
    app.run()