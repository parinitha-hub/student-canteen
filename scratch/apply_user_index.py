import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
index_path = os.path.join(ROOT, "index.html")
frontend_index_path = os.path.join(ROOT, "frontend", "index.html")

with open(index_path, "r", encoding="utf-8") as f:
    html = f.read()

# Replace the student login panel with user-specific Sign In & Register tabs
old_student_panel = """        <!-- Student Login Panel -->
        <div id="login-panel-student" class="login-panel">
          <form id="student-portal-form" onsubmit="handlePortalStudentLogin(event); return false;" novalidate
            class="simple-login-form">
            <div class="simple-input-group" style="margin-bottom:12px; text-align:left;">
              <label for="login-student-name" class="simple-label"
                style="display:block; font-size:0.82rem; font-weight:700; margin-bottom:4px; color:var(--text-main);">Your
                Full Name</label>
              <input type="text" id="login-student-name" class="simple-input" placeholder="Enter your full name"
                autocomplete="off" required
                style="width:100%; padding:10px 12px; border:1.5px solid var(--border); border-radius:10px; font-size:0.92rem; outline:none; transition:border 0.2s;"
                onkeydown="if(event.key==='Enter'){handlePortalStudentLogin(event); return false;}">
            </div>

            <div class="simple-input-group" style="margin-bottom:12px; text-align:left;">
              <label for="login-student-year" class="simple-label"
                style="display:block; font-size:0.82rem; font-weight:700; margin-bottom:4px; color:var(--text-main);">College
                Year / Department</label>
              <select id="login-student-year" class="simple-select"
                style="width:100%; padding:10px 12px; border:1.5px solid var(--border); border-radius:10px; font-size:0.92rem; outline:none; background:#ffffff;">
                <option value="1st Year" selected>1st Year</option>
                <option value="2nd Year">2nd Year</option>
                <option value="3rd Year">3rd Year</option>
                <option value="4th Year (Final Year)">4th Year (Final Year)</option>
                <option value="Faculty / Staff">Faculty / Staff</option>
              </select>
            </div>

            <div class="simple-input-group" style="margin-bottom:16px; text-align:left;">
              <label for="login-student-phone" class="simple-label"
                style="display:block; font-size:0.82rem; font-weight:700; margin-bottom:4px; color:var(--text-main);">Mobile
                Number (Optional)</label>
              <input type="tel" id="login-student-phone" class="simple-input" placeholder="e.g. 10-digit mobile number"
                maxlength="10"
                style="width:100%; padding:10px 12px; border:1.5px solid var(--border); border-radius:10px; font-size:0.92rem; outline:none;"
                onkeydown="if(event.key==='Enter'){handlePortalStudentLogin(event); return false;}">
            </div>

            <button type="button" class="btn-simple-submit btn-student-submit" id="btn-login-student-submit"
              onclick="handlePortalStudentLogin(event)"
              style="width:100%; padding:13px; font-size:1rem; font-weight:800; background:linear-gradient(135deg, #4f46e5 0%, #6366f1 100%); color:#ffffff; border:none; border-radius:12px; cursor:pointer; box-shadow:0 4px 14px rgba(79, 70, 229, 0.3); display:flex; align-items:center; justify-content:center; gap:8px; transition:transform 0.2s, box-shadow 0.2s;">
              <span>🍽️</span> Login &amp; Order Now
            </button>
          </form>

          <div class="login-card-footer"
            style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-top:16px; border-top:1px solid var(--border); padding-top:12px;">
            <button type="button" class="btn-guest-link" onclick="navigateToSection('about')"
              style="background:transparent; border:none; color:var(--text-muted); font-size:0.84rem; cursor:pointer;">
              <span>←</span> About Website
            </button>
            <button type="button" class="btn-guest-link" id="link-toggle-staff" onclick="toggleStaffLoginForm()"
              style="background:transparent; border:none; color:var(--primary); font-size:0.84rem; font-weight:700; cursor:pointer;">
              <span>👨‍🍳</span> Kitchen Staff Login →
            </button>
          </div>
        </div>"""

new_student_panel = """        <!-- Student Login Panel with User-Specific Account Support -->
        <div id="login-panel-student" class="login-panel">
          <!-- Submode Toggle: Sign In vs Register -->
          <div style="display:flex; background:#f1f5f9; border-radius:10px; padding:3px; margin-bottom:16px;">
            <button type="button" id="subtab-auth-signin" onclick="switchStudentAuthMode('signin')"
              style="flex:1; padding:8px 12px; font-size:0.84rem; font-weight:800; border-radius:8px; border:none; background:#ffffff; color:var(--primary); cursor:pointer; box-shadow:0 1px 3px rgba(0,0,0,0.1); transition:all 0.2s;">
              🔑 Sign In
            </button>
            <button type="button" id="subtab-auth-register" onclick="switchStudentAuthMode('register')"
              style="flex:1; padding:8px 12px; font-size:0.84rem; font-weight:800; border-radius:8px; border:none; background:transparent; color:var(--text-muted); cursor:pointer; transition:all 0.2s;">
              📝 Register New Account
            </button>
          </div>

          <!-- 1. SIGN IN FORM -->
          <form id="student-signin-form" onsubmit="handleStudentSignIn(event); return false;" novalidate class="simple-login-form">
            <!-- Hidden backward-compatibility fields -->
            <input type="hidden" id="login-student-name" value="">
            <input type="hidden" id="login-student-year" value="1st Year">
            <input type="hidden" id="login-student-phone" value="">

            <div class="simple-input-group" style="margin-bottom:12px; text-align:left;">
              <label for="login-student-username" class="simple-label"
                style="display:block; font-size:0.82rem; font-weight:700; margin-bottom:4px; color:var(--text-main);">
                Student ID / Username
              </label>
              <input type="text" id="login-student-username" class="simple-input" placeholder="e.g. SAV101 or srinath"
                autocomplete="username" required
                style="width:100%; padding:10px 12px; border:1.5px solid var(--border); border-radius:10px; font-size:0.92rem; outline:none;"
                onkeydown="if(event.key==='Enter'){handleStudentSignIn(event); return false;}">
            </div>

            <div class="simple-input-group" style="margin-bottom:14px; text-align:left;">
              <label for="login-student-password" class="simple-label"
                style="display:block; font-size:0.82rem; font-weight:700; margin-bottom:4px; color:var(--text-main);">
                Account Password
              </label>
              <div style="position:relative;">
                <input type="password" id="login-student-password" class="simple-input" placeholder="Enter password (e.g. pass123)"
                  autocomplete="current-password" required
                  style="width:100%; padding:10px 38px 10px 12px; border:1.5px solid var(--border); border-radius:10px; font-size:0.92rem; outline:none;"
                  onkeydown="if(event.key==='Enter'){handleStudentSignIn(event); return false;}">
                <button type="button" onclick="togglePasswordVisibility('login-student-password', this)"
                  style="position:absolute; right:10px; top:50%; transform:translateY(-50%); background:transparent; border:none; cursor:pointer; font-size:1rem; color:var(--text-muted);"
                  title="Toggle password">👁️</button>
              </div>
            </div>

            <!-- Demo Quick Fill Accounts for instant testing -->
            <div style="background:#f8fafc; border:1px dashed #cbd5e1; border-radius:8px; padding:8px 10px; margin-bottom:14px;">
              <div style="font-size:0.72rem; font-weight:800; color:var(--text-muted); text-transform:uppercase; margin-bottom:4px;">
                ⚡ Instant Test Accounts (1-Click Fill):
              </div>
              <div style="display:flex; gap:6px; flex-wrap:wrap;">
                <button type="button" class="btn-stock-adjust" onclick="fillDemoStudent('SAV101', 'pass123')"
                  style="font-size:0.75rem; padding:4px 8px; font-weight:800;">🎓 Srinath (SAV101)</button>
                <button type="button" class="btn-stock-adjust" onclick="fillDemoStudent('SAV102', 'pass123')"
                  style="font-size:0.75rem; padding:4px 8px; font-weight:800;">🎓 Divya (SAV102)</button>
                <button type="button" class="btn-stock-adjust" onclick="fillDemoStudent('SAV103', 'pass123')"
                  style="font-size:0.75rem; padding:4px 8px; font-weight:800;">🎓 Aarav (SAV103)</button>
              </div>
            </div>

            <button type="button" class="btn-simple-submit btn-student-submit" id="btn-login-student-submit"
              onclick="handleStudentSignIn(event)"
              style="width:100%; padding:13px; font-size:1rem; font-weight:800; background:linear-gradient(135deg, #4f46e5 0%, #6366f1 100%); color:#ffffff; border:none; border-radius:12px; cursor:pointer; box-shadow:0 4px 14px rgba(79, 70, 229, 0.3); display:flex; align-items:center; justify-content:center; gap:8px;">
              <span>🔐</span> Sign In to My Account
            </button>
          </form>

          <!-- 2. REGISTER NEW ACCOUNT FORM (Hidden by default) -->
          <form id="student-register-form" onsubmit="handleStudentRegister(event); return false;" novalidate class="simple-login-form" style="display:none;">
            <div class="simple-input-group" style="margin-bottom:10px; text-align:left;">
              <label for="register-student-name" class="simple-label"
                style="display:block; font-size:0.82rem; font-weight:700; margin-bottom:3px; color:var(--text-main);">
                Full Name
              </label>
              <input type="text" id="register-student-name" class="simple-input" placeholder="e.g. Srinath Kumar" required
                style="width:100%; padding:9px 12px; border:1.5px solid var(--border); border-radius:10px; font-size:0.9rem; outline:none;">
            </div>

            <div class="simple-input-group" style="margin-bottom:10px; text-align:left;">
              <label for="register-student-username" class="simple-label"
                style="display:block; font-size:0.82rem; font-weight:700; margin-bottom:3px; color:var(--text-main);">
                Student ID / Roll No (Your Login Username)
              </label>
              <input type="text" id="register-student-username" class="simple-input" placeholder="e.g. SAV105" required
                style="width:100%; padding:9px 12px; border:1.5px solid var(--border); border-radius:10px; font-size:0.9rem; outline:none; text-transform:uppercase;">
            </div>

            <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-bottom:10px; text-align:left;">
              <div>
                <label for="register-student-year" class="simple-label"
                  style="display:block; font-size:0.82rem; font-weight:700; margin-bottom:3px; color:var(--text-main);">Year / Dept</label>
                <select id="register-student-year" class="simple-select"
                  style="width:100%; padding:9px 10px; border:1.5px solid var(--border); border-radius:10px; font-size:0.88rem; outline:none; background:#ffffff;">
                  <option value="1st Year">1st Year</option>
                  <option value="2nd Year">2nd Year</option>
                  <option value="3rd Year" selected>3rd Year</option>
                  <option value="4th Year">4th Year</option>
                  <option value="Faculty / Staff">Faculty</option>
                </select>
              </div>
              <div>
                <label for="register-student-phone" class="simple-label"
                  style="display:block; font-size:0.82rem; font-weight:700; margin-bottom:3px; color:var(--text-main);">Mobile (Optional)</label>
                <input type="tel" id="register-student-phone" class="simple-input" placeholder="10-digit phone" maxlength="10"
                  style="width:100%; padding:9px 10px; border:1.5px solid var(--border); border-radius:10px; font-size:0.88rem; outline:none;">
              </div>
            </div>

            <div class="simple-input-group" style="margin-bottom:14px; text-align:left;">
              <label for="register-student-password" class="simple-label"
                style="display:block; font-size:0.82rem; font-weight:700; margin-bottom:3px; color:var(--text-main);">
                Create Password
              </label>
              <input type="password" id="register-student-password" class="simple-input" placeholder="Minimum 4 characters" required
                style="width:100%; padding:9px 12px; border:1.5px solid var(--border); border-radius:10px; font-size:0.9rem; outline:none;">
            </div>

            <button type="button" class="btn-simple-submit btn-student-submit" id="btn-register-student-submit"
              onclick="handleStudentRegister(event)"
              style="width:100%; padding:12px; font-size:1rem; font-weight:800; background:linear-gradient(135deg, #10b981 0%, #059669 100%); color:#ffffff; border:none; border-radius:12px; cursor:pointer; box-shadow:0 4px 14px rgba(16, 185, 129, 0.3); display:flex; align-items:center; justify-content:center; gap:8px;">
              <span>✨</span> Create Account &amp; Sign In
            </button>
          </form>

          <div class="login-card-footer"
            style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-top:16px; border-top:1px solid var(--border); padding-top:12px;">
            <button type="button" class="btn-guest-link" onclick="navigateToSection('about')"
              style="background:transparent; border:none; color:var(--text-muted); font-size:0.84rem; cursor:pointer;">
              <span>←</span> About Website
            </button>
            <button type="button" class="btn-guest-link" id="link-toggle-staff" onclick="toggleStaffLoginForm()"
              style="background:transparent; border:none; color:var(--primary); font-size:0.84rem; font-weight:700; cursor:pointer;">
              <span>👨‍🍳</span> Kitchen Staff Login →
            </button>
          </div>
        </div>"""

if old_student_panel in html:
    html = html.replace(old_student_panel, new_student_panel)
    print("Replaced student login panel with user-specific Sign In & Register tabs.")
else:
    print("Warning: old_student_panel did not match exactly, searching...")

# Add User Profile Modal right after cancel-order-modal
profile_modal_html = """  <!-- User Profile & Account Modal -->
  <div id="profile-modal" class="modal-overlay">
    <div class="modal-box" style="max-width:440px;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px; border-bottom:1px solid var(--border); padding-bottom:10px;">
        <div style="display:flex; align-items:center; gap:8px;">
          <span style="font-size:1.35rem;">👤</span>
          <div>
            <h2 style="font-size:1.25rem; font-weight:800; color:var(--text-main); margin:0;">User Profile</h2>
            <p style="font-size:0.78rem; color:var(--text-muted); margin:0;">Your private account &amp; dining records</p>
          </div>
        </div>
        <button type="button" onclick="closeProfileModal()"
          style="background:transparent; border:none; font-size:1.35rem; cursor:pointer; color:var(--text-muted); line-height:1;"
          aria-label="Close profile">✕</button>
      </div>

      <div id="profile-modal-body">
        <!-- Dynamically rendered by app.js -->
      </div>
    </div>
  </div>
"""

if 'id="profile-modal"' not in html:
    cancel_marker = '<div id="cancel-order-modal"'
    if cancel_marker in html:
        html = html.replace(cancel_marker, profile_modal_html + '\n\n  ' + cancel_marker)
        print("Added profile-modal to index.html.")

with open(index_path, "w", encoding="utf-8") as f:
    f.write(html)

with open(frontend_index_path, "w", encoding="utf-8") as f:
    f.write(html)

print("Updated index.html and frontend/index.html with user-specific login UI!")
