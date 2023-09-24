CREATE TABLE IF NOT EXISTS mainmenu (
    id integer PRIMARY KEY AUTOINCREMENT,
    title text NOT NULL,
    url text NOT NULL
);

CREATE TABLE IF NOT EXISTS notebooks (
    id integer PRIMARY KEY AUTOINCREMENT,
    header text NOT NULL UNIQUE,
    text text NOT NULL,
    creation_date text NOT NULL,
    last_change_date text NOT NULL
);