DROP TABLE IF EXISTS book;
CREATE TABLE book (
	ISBN INTEGER PRIMARY KEY NOT NULL,
	title varchar(255) NOT NULL,
	publisher varchar(255),
	publish_date DATE,
	publish_location varchar(255),
	subject_of_book varchar(255),
	description_of_book varchar(255),
	number_of_pages INTEGER,
	status_of_book varchar(255) NOT NULL,
	number_of_copies INTEGER NOT NULL
);

DROP INDEX IF EXISTS index_ISBN;
CREATE INDEX index_ISBN ON book(ISBN);
DROP INDEX IF EXISTS index_title;
CREATE INDEX index_title ON book(title);
DROP INDEX IF EXISTS index_publisher;
CREATE INDEX index_publisher ON book(publisher);
DROP INDEX IF EXISTS index_publish_date;
CREATE INDEX index_publish_date ON book(publish_date);
DROP INDEX IF EXISTS index_publish_location;
CREATE INDEX index_publish_location ON book(publish_location);
DROP INDEX IF EXISTS index_number_of_pages;
CREATE INDEX index_number_of_pages ON book(number_of_pages);
DROP INDEX IF EXISTS index_status_of_book;
CREATE INDEX index_status_of_book ON book(status_of_book);
DROP INDEX IF EXISTS index_number_of_copies;
CREATE INDEX index_number_of_copies ON book(number_of_copies);


DROP TABLE IF EXISTS author;
CREATE TABLE author (
	author_id INTEGER PRIMARY KEY AUTOINCREMENT,
	first_name varchar(255) NOT NULL,
	last_name varchar(255)
);

DROP INDEX IF EXISTS index_author_id;
CREATE INDEX index_author_id ON author(author_id);
DROP INDEX IF EXISTS index_first_name;
CREATE INDEX index_first_name ON author(first_name);
DROP INDEX IF EXISTS index_last_name;
CREATE INDEX index_last_name ON author(last_name);


DROP TABLE IF EXISTS book_author;
CREATE TABLE book_author (
	author_id INTEGER NOT NULL,
	book_id INTEGER NOT NULL,
	
	PRIMARY KEY(book_id, author_id),
	
	FOREIGN KEY (book_id) REFERENCES book(ISBN)
	ON DELETE CASCADE ON UPDATE CASCADE,

	FOREIGN KEY (author_id) REFERENCES author(Author_ID)
	ON DELETE CASCADE ON UPDATE CASCADE
);

DROP INDEX IF EXISTS index_author_id_2;
CREATE INDEX index_author_id_2 ON book_author(author_id);
DROP INDEX IF EXISTS index_book_id;
CREATE INDEX index_book_id ON book_author(book_id);


DROP TABLE IF EXISTS membership;
CREATE TABLE membership (
	membership_id INTEGER PRIMARY KEY AUTOINCREMENT,
	number_of_books INTEGER NOT NULL,
	number_of_renewals INTEGER NOT NULL,
	cost varchar(255) NOT NULL,
	eudoxus INTEGER,
	renting_dates INTEGER NOT NULL,
	number_of_bookings INTEGER NOT NULL
);


DROP TABLE IF EXISTS library;
CREATE TABLE library (
	library_id INTEGER PRIMARY KEY AUTOINCREMENT,
	library_name varchar(255) NOT NULL
);


DROP TABLE IF EXISTS location;
CREATE TABLE location (
	location_id INTEGER PRIMARY KEY AUTOINCREMENT,
	country varchar(255) NOT NULL,
	city varchar(255) NOT NULL,
	street varchar(255) NOT NULL,
	street_number INTEGER NOT NULL,
	postal_code INTEGER NOT NULL
);


DROP TABLE IF EXISTS penalty;
CREATE TABLE penalty (
	penalty_id INTEGER PRIMARY KEY AUTOINCREMENT,
	penalty varchar(255) NOT NULL
);


DROP TABLE IF EXISTS member;
CREATE TABLE member (
	AFM varchar(255) PRIMARY KEY NOT NULL,
	first_name varchar(255) NOT NULL,
	last_name varchar(255) NOT NULL,
	gender varchar(255) NOT NULL,
	email varchar(255) NOT NULL,
	phone_number INTEGER NOT NULL,
	birthdate DATE NOT NULL,
	type_of_membership INTEGER NOT NULL,
	penalty_id INTEGER,
	location_id INTEGER NOT NULL,

	FOREIGN KEY(type_of_membership) REFERENCES membership (membership_id)
	ON DELETE CASCADE ON UPDATE CASCADE,

	FOREIGN KEY(penalty_id) REFERENCES penalty (penalty_id)
	ON DELETE SET NULL ON UPDATE CASCADE,

	FOREIGN KEY(location_id) REFERENCES location (location_id)
	ON DELETE CASCADE ON UPDATE CASCADE
);


DROP TABLE IF EXISTS library_member;
CREATE TABLE library_member (
	member_id varchar(255) NOT NULL,
	library_id INTEGER NOT NULL,

	PRIMARY KEY(member_id, library_id)

	FOREIGN KEY(member_id) REFERENCES member (AFM)
	ON DELETE CASCADE ON UPDATE CASCADE,

	FOREIGN KEY(library_id) REFERENCES library (library_id)
	ON DELETE CASCADE ON UPDATE CASCADE
);


DROP TABLE IF EXISTS holding;
CREATE TABLE holding (
	holding_id INTEGER PRIMARY KEY AUTOINCREMENT,
	book_id INTEGER NOT NULL,
	status_of_holding varchar(255) NOT NULL,
	edition_of_holding varchar(255) NOT NULL,
	language_written varchar(255) NOT NULL,
	date_last_checked_out DATE,
	total_checkouts INTEGER,
	total_renewals INTEGER,
	AFM varchar(255),
	date_of_borrowing DATE,
	date_of_return DATE,
	library_id_returning INTEGER,
	library_id_receiving INTEGER,
	courier varchar(255),
	date_sent DATE,
	date_received DATE,
	library_id INTEGER,
	member_id varchar(255),
	library_id_returned INTEGER,
	date_of_holding_return DATE,

	FOREIGN KEY (book_id) REFERENCES book (ISBN)
	ON DELETE CASCADE ON UPDATE CASCADE,

	FOREIGN KEY (AFM) REFERENCES member (AFM)
	ON DELETE SET NULL ON UPDATE CASCADE,

	FOREIGN KEY (library_id_returning) REFERENCES library (library_id)
	ON DELETE SET NULL ON UPDATE CASCADE,	

	FOREIGN KEY (library_id_receiving) REFERENCES library (library_id)
	ON DELETE SET NULL ON UPDATE CASCADE,

	FOREIGN KEY (library_id) REFERENCES library (library_id)
	ON DELETE SET NULL ON UPDATE CASCADE,

	FOREIGN KEY (member_id) REFERENCES member (AFM)
	ON DELETE SET NULL ON UPDATE CASCADE,

	FOREIGN KEY (library_id_returned) REFERENCES library (library_id)
	ON DELETE SET NULL ON UPDATE CASCADE
);

DROP INDEX IF EXISTS index_holding_id;
CREATE INDEX index_holding_id ON holding(holding_id);
DROP INDEX IF EXISTS index_book_id_2;
CREATE INDEX index_book_id_2 ON holding(book_id);
DROP INDEX IF EXISTS index_status_of_holding;
CREATE INDEX index_status_of_holding ON holding(status_of_holding);
DROP INDEX IF EXISTS index_edition_of_holding;
CREATE INDEX index_edition_of_holding ON holding(edition_of_holding);
DROP INDEX IF EXISTS index_date_last_checked_out;
CREATE INDEX index_date_last_checked_out ON holding(date_last_checked_out);
DROP INDEX IF EXISTS index_total_checkouts;
CREATE INDEX index_total_checkouts ON holding(total_checkouts);
DROP INDEX IF EXISTS index_total_renewals;
CREATE INDEX index_total_renewals ON holding(total_renewals);
DROP INDEX IF EXISTS index_AFM;
CREATE INDEX index_AFM ON holding(AFM);
DROP INDEX IF EXISTS index_date_of_borrowing;
CREATE INDEX index_date_of_borrowing ON holding(date_of_borrowing);
DROP INDEX IF EXISTS index_date_of_return;
CREATE INDEX index_date_of_return ON holding(date_of_return);


DROP TABLE IF EXISTS position;
CREATE TABLE position (
	position_id INTEGER PRIMARY KEY AUTOINCREMENT,
	library_id INTEGER NOT NULL,
	holding_id INTEGER NOT NULL,
	corridor INTEGER NOT NULL,
	shelf INTEGER NOT NULL,

	FOREIGN KEY(library_id) REFERENCES library (library_id)
	ON DELETE SET NULL ON UPDATE CASCADE,

	FOREIGN KEY(holding_id) REFERENCES holding (holding_id)
	ON DELETE SET NULL ON UPDATE CASCADE
);

DROP INDEX IF EXISTS index_position_id;
CREATE INDEX index_position_id oN position(position_id);
DROP INDEX IF EXISTS index_library_id;
CREATE INDEX index_library_id oN position(library_id);
DROP INDEX IF EXISTS index_holding_id;
CREATE INDEX index_holding_id oN position(holding_id);
DROP INDEX IF EXISTS index_corridor;
CREATE INDEX index_corridor oN position(corridor);
DROP INDEX IF EXISTS index_shelf;
CREATE INDEX index_shelf oN position(shelf);


DROP TABLE IF EXISTS share;
CREATE TABLE share (
	share_id INTEGER PRIMARY KEY AUTOINCREMENT,
	library_id_sharing INTEGER NOT NULL,
	holding_id INTEGER NOT NULL,
	library_id_receiving INTEGER NOT NULL,
	courier varchar(255) NOT NULL,
	date_sent DATE NOT NULL,
	date_received DATE,
	shipment_time TIME NOT NULL,

	FOREIGN KEY(library_id_sharing) REFERENCES library (library_id)
	ON DELETE CASCADE ON UPDATE CASCADE,

	FOREIGN KEY(holding_id) REFERENCES holding (holding_id)
	ON DELETE CASCADE ON UPDATE CASCADE,

	FOREIGN KEY(library_id_receiving) REFERENCES library (library_id)
	ON DELETE CASCADE ON UPDATE CASCADE
);

DROP INDEX IF EXISTS index_library_id_sharing;
CREATE INDEX index_library_id_sharing ON share(library_id_sharing);
DROP INDEX IF EXISTS index_holding_id_2;
CREATE INDEX index_holding_id_2 ON share(holding_id);
DROP INDEX IF EXISTS index_library_id_receiving;
CREATE INDEX index_library_id_receiving ON share(library_id_receiving);
DROP INDEX IF EXISTS index_courier;
CREATE INDEX index_courier ON share(courier);
DROP INDEX IF EXISTS index_date_sent;
CREATE INDEX index_date_sent ON share(date_sent);
DROP INDEX IF EXISTS index_date_received;
CREATE INDEX index_date_received ON share(date_received);
DROP INDEX IF EXISTS index_shipment_time;
CREATE INDEX index_shipment_time ON share(shipment_time);


DROP TABLE IF EXISTS location_house;
