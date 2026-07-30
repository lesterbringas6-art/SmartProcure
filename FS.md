update this folder structure include history for each user what they did in the system

SmartProcure/
├── main.py
├── tables.sql
├── requirements.txt
├── venv/
│
├── templates/
│
│   ├── auth/
│   │
│   │   ├── login.html
│   │   │      (Login → Redirect to Requester Dashboard or Receiving Dashboard)
│   │   │
│   │   └── register.html
│   │          (Register using Employee ID → Login)
│   │
│   ├── requester_office/
│   │
│   │   ├── dashboard.html
│   │   │      (Requester Home → Manage PR, Track PR, Profile, Settings)
│   │   │
│   │   ├── manage_pr.html
│   │   │      (Draft Purchase Requests)
│   │   │      ├── Create PR
│   │   │      ├── View Draft PR
│   │   │      ├── Edit Draft PR
│   │   │      ├── Delete Draft PR
│   │   │      └── Submit PR
│   │   │           │
│   │   │           └── After Submit → Receiving Office → manage_pr.html
│   │   │
│   │   ├── track_pr.html
│   │   │      (Submitted Purchase Requests)
│   │   │      ├── View PR
│   │   │      ├── View Status Timeline
│   │   │      ├── View PO Status
│   │   │      ├── View Delivery Status
│   │   │      ├── Print PR
│   │   │      └── Confirm Receipt of Goods (Optional)
│   │   │
│   │   ├── profile.html
│   │   │      (Manage User Profile)
│   │   │
│   │   └── settings.html
│   │          (Requester Settings)
│   │
│   ├── receiving_office/
│   │
│   │   ├── dashboard.html
│   │   │      (Receiving Dashboard)
│   │   │      ├── Manage PR
│   │   │      ├── Purchase Orders
│   │   │      ├── Receive Goods
│   │   │      ├── Completed Transactions
│   │   │      ├── Archive
│   │   │      │   └── Search Archive
│   │   │      ├── Profile
│   │   │      └── Settings
│   │   │
│   │   ├── manage_pr.html
│   │   │      (Submitted Purchase Requests from Requester Office)
│   │   │      ├── View PR
│   │   │      ├── Review PR
│   │   │      ├── Approve PR
│   │   │      ├── Return for Revision
│   │   │      ├── Reject PR
│   │   │      └── Delete PR
│   │   │           │
│   │   │           └── Approved PR
│   │   │                  │
│   │   │                  ▼
│   │   │          purchase_orders.html
│   │   │
│   │   ├── purchase_orders.html
│   │   │      (Approved Purchase Requests)
│   │   │      ├── View Approved PR
│   │   │      ├── Generate Purchase Order
│   │   │      ├── Edit Purchase Order
│   │   │      ├── Print Purchase Order
│   │   │      ├── Mark PO as Sent (Manual)
│   │   │      └── Delete Purchase Order
│   │   │           │
│   │   │           └── PO Sent
│   │   │                  │
│   │   │                  ▼
│   │   │          receive_goods.html
│   │   │
│   │   ├── receive_goods.html
│   │   │      (Purchase Orders Waiting for Delivery)
│   │   │      ├── View Purchase Order
│   │   │      ├── Record Delivery
│   │   │      ├── Record Received Quantity
│   │   │      ├── Update Delivery Status
│   │   │      ├── Upload Delivery Receipt
│   │   │      ├── Proof of Receiving
│   │   │      ├── Mark as Received
│   │   │      └── Print Receiving Report
│   │   │           │
│   │   │           └── Goods Received
│   │   │                  │
│   │   │                  ▼
│   │   │          completed_transactions.html
│   │   │
│   │   ├── completed_transactions.html
│   │   │      (Successfully Completed Procurement)
│   │   │      ├── View PR
│   │   │      ├── View PO
│   │   │      ├── View Receiving Report
│   │   │      ├── Print Documents
│   │   │      └── Archive Transaction
│   │   │           │
│   │   │           └── Archive
│   │   │                  │
│   │   │                  ▼
│   │   │          manage_archive.html
│   │   │
│   │   ├── manage_archive.html
│   │   │      (Permanent Document Storage)
│   │   │      ├── Scan Physical Documents
│   │   │      ├── Upload PDF/Image
│   │   │      ├── View Archive
│   │   │      ├── Print Archive
│   │   │      └── Delete Archive
│   │   │
│   │   ├── search_archive.html
│   │   │      (Search Archived Records)
│   │   │      ├── Search by PR Number
│   │   │      ├── Search by PO Number
│   │   │      ├── Search by Department
│   │   │      ├── Search by Supplier
│   │   │      ├── Search by Date
│   │   │      └── Open Archived Record
│   │   │
│   │   ├── profile.html
│   │   │      (Manage Receiving Officer Profile)
│   │   │
│   │   └── settings.html
│   │          (Receiving Office Settings)
│   │
│   └── includes/
│       ├── navbar.html
│       │      (Shared Navigation Bar)
│       │
│       ├── sidebar.html
│       │      (Role-Based Sidebar)
│       │
│       ├── footer.html
│       │      (Shared Footer)
│       │
│       └── flash_messages.html
│              (Success/Error Notifications)
│
├── static/
    ├── style/
    ├── js/
    ├── images/
    ├── uploads/
    └── pdf/
