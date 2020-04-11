-- Transform in-memory ConceptNet SQLite database
INSERT INTO concepts(lang, text, speech, suffix)
SELECT DISTINCT lang, text, speech, suffix
FROM (SELECT source_lang AS lang,
             source_text AS text,
             source_speech AS speech,
             source_suffix AS suffix,
             source_uri AS uri
      FROM assertions
      UNION
      SELECT target_lang AS lang,
             target_text AS text,
             target_speech AS speech,
             target_suffix AS suffix,
             target_uri AS uri
      FROM assertions)
LEFT JOIN languages ON languages.code == lang
LEFT JOIN part_of_speeches ON part_of_speeches.code == speech
ORDER BY uri;

INSERT INTO datasets(uri)
SELECT DISTINCT dataset
FROM assertions;

INSERT INTO licenses(uri)
SELECT DISTINCT license
FROM assertions;

CREATE TABLE concept_ids (
    id  INTEGER PRIMARY KEY AUTOINCREMENT,
    uri STRING  UNIQUE NOT NULL
);

INSERT INTO concept_ids(uri)
SELECT DISTINCT uri
FROM (SELECT source_uri AS uri FROM assertions 
      UNION
      SELECT target_uri AS uri FROM assertions)
ORDER BY uri;

ALTER TABLE assertions ADD COLUMN relation_id INTEGER;
ALTER TABLE assertions ADD COLUMN source_id INTEGER;
ALTER TABLE assertions ADD COLUMN target_id INTEGER;
ALTER TABLE assertions ADD COLUMN dataset_id INTEGER;
ALTER TABLE assertions ADD COLUMN license_id INTEGER;

UPDATE assertions
SET relation_id = (SELECT relations.id
                   FROM relations
                   WHERE relations.relation == assertions.relation),
    source_id = (SELECT concept_ids.id
                 FROM concept_ids
                 WHERE concept_ids.uri == assertions.source_uri),
    target_id = (SELECT concept_ids.id
                 FROM concept_ids
                 WHERE concept_ids.uri == assertions.target_uri),
    dataset_id = (SELECT datasets.id
                  FROM datasets
                  WHERE datasets.uri == assertions.dataset),
    license_id = (SELECT licenses.id
                  FROM licenses
                  WHERE licenses.uri == assertions.license);

ALTER TABLE assertions RENAME TO assertions_old;

CREATE TABLE assertions (
      id             INTEGER PRIMARY KEY AUTOINCREMENT,
      relation_id    INTEGER NOT NULL,
      source_id      INTEGER NOT NULL,
      target_id      INTEGER NOT NULL,
      dataset_id     INTEGER NOT NULL,
      license_id     INTEGER NOT NULL,
      surface_text   STRING,
      surface_source STRING,
      surface_target STRING,
      weight         FLOAT NOT NULL,

      UNIQUE(relation_id, source_id, target_id)
);

INSERT INTO assertions
SELECT id, relation_id, source_id, target_id, dataset_id, license_id, 
       surface_text, surface_source, surface_target, weight
FROM assertions_old;

--DROP TABLE assertions_old;
