#  Multi-Tenant Edge OS Isolator

A low-level, high-security Web-to-Kernel administrative bridge designed to provision, isolate, and audit user environments directly on shared Edge computing and IoT hardware. 

This project completely bypasses traditional software-level database architectures, treating the **Windows Security Accounts Manager (SAM)** registry as its absolute, live data source.

---

##  Core Features

- **Direct OS Kernel Provisioning:** Dynamically creates authentic Windows local user accounts with administrative privilege validation in real-time.
- **Hardware-Level Access Isolation:** Instantly suspends or restores tenant privileges using native OS flags (`/active:no` and `/active:yes`) without damaging or purging local user profiles/directories.
- **Deep Inspection Console:** Queries low-level OS telemetry on-demand (`net user <username>`) to fetch live user account state, password age, and expiration rules directly from the host machine.
- **Command Injection Firewall:** Implements a strict Regular Expression sanitization layer (`^[a-zA-Z0-9_]*$`) to block terminal exploits (e.g., `;`, `&`, `|`) before they touch the OS shell.
- **Immutable System Auditing:** Maintains an isolated, read-only system event log to register all administrative lifecycle actions for compliance tracking.

---

##  System Directory Structure

```text
edge_os_isolator/
│
├── core/                       # Operational Application Layer
│   ├── templates/
│   │   └── index.html          # Supervisor Frontend Console
│   ├── admin.py                # Read-Only Audit Log Dashboard
│   ├── models.py               # System Audit Trail Database Schema
│   ├── tests.py                # Automated Security Validation Tests
│   └── views.py                # Main OS Bridge Controller (Subprocess Logic)
│
├── edge_os_project/            # Project Core Configuration
│   ├── settings.py             # Security Framework & App Registrations
│   └── urls.py                 # Network Routing Rules
│
├── db.sqlite3                  # Lightweight Audit Log Ledger
└── manage.py                   # Django Command-Line Utility
