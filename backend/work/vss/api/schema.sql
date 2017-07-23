DROP TABLE IF EXISTS posts;
CREATE TABLE posts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  text TEXT NOT NULL
);
INSERT INTO posts (title, text) VALUES ('First entry', 'This is a text');
INSERT INTO posts (title, text) VALUES ('Second entry', 'This is more text');
INSERT INTO posts (title, text) VALUES ('Third entry', 'This is more text(again');
