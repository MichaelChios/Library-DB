DROP TABLE IF EXISTS login_signin;
CREATE TABLE IF NOT EXISTS login_signin (
	username varchar(255) NOT NULL,
	password_hashed varchar(255) NOT NULL,
	member_admin INTEGER NOT NULL,

	PRIMARY KEY (username)
);

DROP INDEX IF EXISTS index_username;
CREATE INDEX index_username ON login_signin(username);
