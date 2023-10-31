CREATE TABLE IF NOT EXISTS profiles (
    id_profile integer PRIMARY KEY AUTOINCREMENT,
    login text NOT NULL UNIQUE,
    username text NOT NULL UNIQUE,
    password text NOT NULL,
    creation_date text NOT NULL
);

CREATE TABLE IF NOT EXISTS notebooks (
    id_note integer PRIMARY KEY AUTOINCREMENT,
    header text NOT NULL UNIQUE,
    content text NOT NULL,
    creation_date text NOT NULL,
    last_change_date text NOT NULL,
    deadline text,
    id_owner integer,
    owner username,
    FOREIGN KEY (id_owner) REFERENCES profiles (id_profile),
    FOREIGN KEY (owner) REFERENCES profiles (username)
);

CREATE TABLE IF NOT EXISTS lectures (
    id_lectured integer PRIMARY KEY AUTOINCREMENT,
    header text NOT NULL UNIQUE,
    content text NOT NULL,
    creation_date text NOT NULL,
    last_change_date text NOT NULL,
    id_owner integer,
    owner username,
    FOREIGN KEY (id_owner) REFERENCES profiles (id_profile),
    FOREIGN KEY (owner) REFERENCES profiles (username)
);

