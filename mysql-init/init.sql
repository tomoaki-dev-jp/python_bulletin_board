CREATE TABLE IF NOT EXISTS candidates (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name   VARCHAR(100) NOT NULL,
  age    INT,
  email  VARCHAR(120),
  skills VARCHAR(255),
  status VARCHAR(50)  DEFAULT '求職中',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO candidates (name, age, email, skills, status) VALUES
('山田 太郎', 28, 'taro@example.com', 'Python, Django', '求職中'),
('佐藤 花子', 31, 'hanako@example.com', 'JavaScript, React', '稼働中'),
('鈴木 次郎', 25, 'jiro@example.com', 'PHP, MySQL', '保留');
