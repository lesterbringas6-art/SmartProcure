WORKING 

CREATE TABLE `users` (
  `username` varchar(50) NOT NULL,
  `employee_id` varchar(50) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `employees` (
  `employee_id` varchar(50) NOT NULL,
  `first_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `office` varchar(100) DEFAULT NULL,
  `role` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `archives` (
  `id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `pr_po_number` varchar(100) DEFAULT NULL,
  `filename` varchar(255) NOT NULL,
  `qr_filename` varchar(255) DEFAULT NULL,
  `uploaded_by` varchar(100) NOT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

RECENTLY ADDED TABLES:

CREATE TABLE purchase_requests(
pr_id INT AUTO_INCREMENT PRIMARY KEY,
pr_number VARCHAR(50) UNIQUE NOT NULL,
requester_id INT NOT NULL,
department VARCHAR(150),
purpose TEXT,
total_amount DECIMAL(12,2) DEFAULT 0,
status ENUM('Draft','Submitted','Under Review','Returned','Approved','Rejected','PO Generated','Delivered','Completed','Archived') DEFAULT 'Draft',
remarks TEXT,
submitted_at DATETIME,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY(requester_id) REFERENCES users(user_id)
);

CREATE TABLE purchase_request_items(
item_id INT AUTO_INCREMENT PRIMARY KEY,
pr_id INT NOT NULL,
item_name VARCHAR(255),
description TEXT,
quantity INT,
unit VARCHAR(50),
unit_price DECIMAL(12,2),
total_price DECIMAL(12,2),
FOREIGN KEY(pr_id) REFERENCES purchase_requests(pr_id) ON DELETE CASCADE
);

CREATE TABLE pr_attachments(
attachment_id INT AUTO_INCREMENT PRIMARY KEY,
pr_id INT,
filename VARCHAR(255),
original_filename VARCHAR(255),
uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY(pr_id) REFERENCES purchase_requests(pr_id) ON DELETE CASCADE
);

CREATE TABLE purchase_orders(
po_id INT AUTO_INCREMENT PRIMARY KEY,
po_number VARCHAR(50) UNIQUE,
pr_id INT NOT NULL,
generated_by INT,
supplier_name VARCHAR(200),
supplier_address TEXT,
supplier_contact VARCHAR(100),
total_amount DECIMAL(12,2),
status ENUM('Draft','Sent','Waiting Delivery','Partially Received','Received','Completed') DEFAULT 'Draft',
generated_date DATETIME,
FOREIGN KEY(pr_id) REFERENCES purchase_requests(pr_id),
FOREIGN KEY(generated_by) REFERENCES users(user_id)
);

CREATE TABLE purchase_order_items(
po_item_id INT AUTO_INCREMENT PRIMARY KEY,
po_id INT,
item_name VARCHAR(255),
description TEXT,
quantity INT,
unit VARCHAR(50),
unit_price DECIMAL(12,2),
total_price DECIMAL(12,2),
FOREIGN KEY(po_id) REFERENCES purchase_orders(po_id) ON DELETE CASCADE
);

CREATE TABLE receiving_reports(
receive_id INT AUTO_INCREMENT PRIMARY KEY,
po_id INT,
received_by INT,
delivery_receipt VARCHAR(255),
proof_of_receiving VARCHAR(255),
received_date DATETIME,
remarks TEXT,
status ENUM('Pending','Received','Completed') DEFAULT 'Pending',
FOREIGN KEY(po_id) REFERENCES purchase_orders(po_id),
FOREIGN KEY(received_by) REFERENCES users(user_id)
);

CREATE TABLE receiving_items(
receive_item_id INT AUTO_INCREMENT PRIMARY KEY,
receive_id INT,
item_name VARCHAR(255),
ordered_quantity INT,
received_quantity INT,
remarks TEXT,
FOREIGN KEY(receive_id) REFERENCES receiving_reports(receive_id) ON DELETE CASCADE
);

CREATE TABLE archives(
archive_id INT AUTO_INCREMENT PRIMARY KEY,
pr_id INT,
po_id INT,
receive_id INT,
archive_file VARCHAR(255),
archived_by INT,
archived_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
remarks TEXT,
FOREIGN KEY(pr_id) REFERENCES purchase_requests(pr_id),
FOREIGN KEY(po_id) REFERENCES purchase_orders(po_id),
FOREIGN KEY(receive_id) REFERENCES receiving_reports(receive_id),
FOREIGN KEY(archived_by) REFERENCES users(user_id)
);

CREATE TABLE activity_logs(
log_id INT AUTO_INCREMENT PRIMARY KEY,
user_id INT,
activity TEXT,
module VARCHAR(100),
ip_address VARCHAR(100),
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY(user_id) REFERENCES users(user_id)
);

CREATE TABLE notifications(
notification_id INT AUTO_INCREMENT PRIMARY KEY,
user_id INT,
title VARCHAR(255),
message TEXT,
is_read BOOLEAN DEFAULT FALSE,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY(user_id) REFERENCES users(user_id)
);

CREATE TABLE system_settings(
setting_id INT AUTO_INCREMENT PRIMARY KEY,
setting_name VARCHAR(100) UNIQUE,
setting_value TEXT
);

INSERT INTO system_settings(setting_name,setting_value)VALUES
('system_name','SmartProcure'),
('version','1.0'),
('allow_registration','true');

