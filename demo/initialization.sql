-- Initialize in-memory ConceptNet SQLite database

CREATE TABLE languages (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    code STRING  UNIQUE NOT NULL,
    name STRING
);

CREATE TABLE part_of_speeches (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    code STRING  UNIQUE NOT NULL,
    name STRING
);

CREATE TABLE concepts (
    id     INTEGER PRIMARY KEY AUTOINCREMENT,
    lang   INTEGER NOT NULL,
    text   STRING  NOT NULL,
    speech INTEGER,
    suffix STRING,

    UNIQUE(lang, text, speech, suffix)
);

CREATE TABLE relations (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    relation STRING  UNIQUE NOT NULL,
    directed INTEGER NOT NULL
);

CREATE TABLE datasets (
    id  INTEGER PRIMARY KEY AUTOINCREMENT,
    uri STRING  UNIQUE NOT NULL
);

CREATE TABLE licenses (
    id  INTEGER PRIMARY KEY AUTOINCREMENT,
    uri STRING  UNIQUE NOT NULL
);

CREATE TABLE assertions (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    uri            TEXT    UNIQUE NOT NULL,
    relation       TEXT    NOT NULL,
    source_uri     TEXT    NOT NULL,
    source_lang    TEXT    NOT NULL,
    source_text    TEXT    NOT NULL,
    source_speech  TEXT,
    source_suffix  TEXT,
    target_uri     TEXT    NOT NULL,
    target_lang    TEXT    NOT NULL,
    target_text    TEXT    NOT NULL,
    target_speech  TEXT,
    target_suffix  TEXT,
    dataset        TEXT    NOT NULL,
    license        TEXT    NOT NULL,
    weight         REAL    NOT NULL,
    surface_text   TEXT,
    surface_source TEXT,
    surface_target TEXT
);

CREATE TABLE sources (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    assertion_id INTEGER NOT NULL,
    [index]      INTEGER NOT NULL,
    field        STRING  NOT NULL,
    value        STRING  NOT NULL,

    UNIQUE(assertion_id, [index], field)
);
