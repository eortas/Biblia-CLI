CREATE TABLE annotations (
  id          SERIAL PRIMARY KEY,
  translation TEXT    NOT NULL,
  book_id     INT     NOT NULL,
  chapter     INT     NOT NULL,
  verse       INT     NOT NULL,
  text        TEXT    NOT NULL,
  created_at  TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE (translation, book_id, chapter, verse)
);
ALTER TABLE annotations ENABLE ROW LEVEL SECURITY;
CREATE POLICY "read_public" ON annotations FOR SELECT USING (true);
CREATE INDEX idx_ann_lookup ON annotations (translation, book_id, chapter, verse);