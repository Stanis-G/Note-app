CREATE TABLE IF NOT EXISTS mainmenu (
    id_menu integer PRIMARY KEY AUTOINCREMENT,
    title text NOT NULL,
    url text NOT NULL
);

CREATE TABLE IF NOT EXISTS profiles (
    id_prof integer PRIMARY KEY AUTOINCREMENT,
    login text NOT NULL UNIQUE,
    password text NOT NULL,
    creation_date text NOT NULL
);

CREATE TABLE IF NOT EXISTS notebooks (
    id_note integer PRIMARY KEY AUTOINCREMENT,
    header text NOT NULL UNIQUE,
    text text NOT NULL,
    creation_date text NOT NULL,
    last_change_date text NOT NULL,
    FOREIGN KEY (id_prof) REFERENCES profiles (id_prof),
    FOREIGN KEY (owner) REFERENCES profiles(login)
);

