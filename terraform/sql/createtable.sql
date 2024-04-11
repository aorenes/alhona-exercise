CREATE SEQUENCE payload_id_sequence;

CREATE TABLE payload (
    id          integer PRIMARY KEY NOT NULL DEFAULT nextval('payload_id_sequence'),
    signal      varchar(100) NOT NULL,
    concurrence integer NOT NULL
);

INSERT INTO payload VALUES
    (default, 'Bool_11_o(001)_15', 2);
