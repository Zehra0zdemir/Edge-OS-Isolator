from django.shortcuts import render
import subprocess
import re
from .models import SystemAuditLog

def get_windows_users():
    """Fetches Windows local users using 'net user' and parses the stdout cleanly."""
    try:
        result = subprocess.run(['net', 'user'], capture_output=True, text=True, encoding='cp857', errors='ignore')
        lines = result.stdout.split('\n')
        
        users = []
        start_parsing = False
        
        for line in lines:
            if '---' in line:
                start_parsing = True
                continue
            if start_parsing:
                # Filter out system success/error messages from the user table
                if 'Komut' in line or 'successfully' in line or 'tamamlandı' in line or not line.strip():
                    continue
                parts = re.split(r'\s{2,}', line.strip())
                for part in parts:
                    if part:
                        users.append(part)
        return users
    except Exception as e:
        print(f"Error fetching users: {e}")
        return []

def get_user_details(username):
    """Fetches internal OS details for a specific SAM user account."""
    try:
        result = subprocess.run(['net', 'user', username], capture_output=True, text=True, encoding='cp857', errors='ignore')
        if result.returncode == 0:
            return result.stdout.strip()
        return "Could not retrieve account details from Windows SAM."
    except Exception as e:
        return f"Error connecting to OS Core: {str(e)}"

def index(request):
    """Main Controller: Handles Ingestion, Validation, Execution, and State Reflection."""
    error_message = None
    success_message = None
    selected_user_details = None
    target_username = request.POST.get('username', '').strip() if request.method == 'POST' else request.GET.get('details_user', '')

    # Handle GET request for viewing raw SAM account details
    if request.method == 'GET' and target_username:
        selected_user_details = get_user_details(target_username)

    if request.method == 'POST':
        action = request.POST.get('action')
        password = request.POST.get('password', '').strip()

        # INPUT SANITIZATION (Security Layer against Command Injection)
        if target_username and not re.match("^[a-zA-Z0-9_]*$", target_username):
            error_message = "Security Alert: Invalid characters detected! Command Injection blocked."
            SystemAuditLog.objects.create(target_username=target_username, action_type='ADD', status='BLOCKED_INJECTION', details=error_message)
        
        else:
            # ACTION: ADD TENANT
            if action == 'add' and target_username and password:
                try:
                    cmd = subprocess.run(['net', 'user', target_username, password, '/add'], capture_output=True, text=True, encoding='cp857', errors='ignore')
                    if cmd.returncode == 0:
                        success_message = f"Tenant '{target_username}' successfully provisioned in Windows SAM."
                        SystemAuditLog.objects.create(target_username=target_username, action_type='ADD', status='SUCCESS', details=success_message)
                    else:
                        error_message = f"OS Error: {cmd.stderr.strip()}"
                        SystemAuditLog.objects.create(target_username=target_username, action_type='ADD', status='FAILED', details=error_message)
                except Exception as e:
                    error_message = str(e)

            # ACTION: DELETE TENANT
            elif action == 'delete' and target_username:
                try:
                    cmd = subprocess.run(['net', 'user', target_username, '/delete'], capture_output=True, text=True, encoding='cp857', errors='ignore')
                    if cmd.returncode == 0:
                        success_message = f"Tenant '{target_username}' successfully purged from the system."
                        SystemAuditLog.objects.create(target_username=target_username, action_type='DELETE', status='SUCCESS', details=success_message)
                    else:
                        error_message = f"OS Error: {cmd.stderr.strip()}"
                        SystemAuditLog.objects.create(target_username=target_username, action_type='DELETE', status='FAILED', details=error_message)
                except Exception as e:
                    error_message = str(e)

            # ACTION: TOGGLE ACTIVE/PASSIVE STATE
            elif action in ['activate', 'deactivate'] and target_username:
                active_flag = "/active:yes" if action == 'activate' else "/active:no"
                log_type = 'ACTIVATE' if action == 'activate' else 'ISOLATE'
                try:
                    cmd = subprocess.run(['net', 'user', target_username, active_flag], capture_output=True, text=True, encoding='cp857', errors='ignore')
                    if cmd.returncode == 0:
                        status_str = "activated" if action == 'activate' else "isolated (deactivated)"
                        success_message = f"Tenant '{target_username}' hardware access state changed to: {status_str}."
                        SystemAuditLog.objects.create(target_username=target_username, action_type=log_type, status='SUCCESS', details=success_message)
                    else:
                        error_message = f"OS Error: {cmd.stderr.strip()}"
                        SystemAuditLog.objects.create(target_username=target_username, action_type=log_type, status='FAILED', details=error_message)
                except Exception as e:
                    error_message = str(e)

    user_list = get_windows_users()
    return render(request, 'index.html', {
        'users': user_list,
        'error_message': error_message,
        'success_message': success_message,
        'selected_user_details': selected_user_details,
        'inspected_user': target_username if selected_user_details else None
    })