CREATE TABLE IF NOT EXISTS utilisateurs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pseudo VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO utilisateurs (pseudo, email) VALUES
('Along', 'Along@example.com'),
('Tom', 'Tom@example.com'),
('Noah', 'Noah@example.com'),
('Adrien', 'Adrien@example.com');