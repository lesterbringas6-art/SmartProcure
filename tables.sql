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