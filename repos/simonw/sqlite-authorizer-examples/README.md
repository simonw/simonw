# SQLite authorizer examples

SQLite has a mechanism for authorizing access to database objects using an authorizer callback function, [documented here](https://www.sqlite.org/c3ref/c_alter_table.html).

This document demonstrates the different actions and arguments that are checked for different types of queries.

## Usage

You can regenerate these examples by running:

```bash
python generate.py > examples.md
```

For each example a new in-memory database is created, the setup SQL is executed against it, then an authorizer callback is registered that logs the operations that are performed against the database while the main SQL is executed.

### SQLITE_CREATE_INDEX

Setup SQL:
```sql
CREATE TABLE demo_table (name TEXT);
INSERT INTO demo_table (name) VALUES ('Alice')
```

SQL:
```sql
CREATE INDEX demo_index ON demo_table (name)
```

Operations:

```
SQLITE_INSERT	arg1="sqlite_master", dbname="main"
SQLITE_CREATE_INDEX	arg1="demo_index", arg2="demo_table", dbname="main"
SQLITE_READ	arg1="demo_table", arg2="name", dbname="main"
SQLITE_INSERT	arg1="sqlite_master", dbname="main"
SQLITE_REINDEX	arg1="demo_index", dbname="main"
```

### SQLITE_CREATE_TABLE

SQL:
```sql
CREATE TABLE demo_table (name TEXT)
```

Operations:

```
SQLITE_INSERT	arg1="sqlite_master", dbname="main"
SQLITE_CREATE_TABLE	arg1="demo_table", dbname="main"
SQLITE_UPDATE	arg1="sqlite_master", arg2="type", dbname="main"
SQLITE_UPDATE	arg1="sqlite_master", arg2="name", dbname="main"
SQLITE_UPDATE	arg1="sqlite_master", arg2="tbl_name", dbname="main"
SQLITE_UPDATE	arg1="sqlite_master", arg2="rootpage", dbname="main"
SQLITE_UPDATE	arg1="sqlite_master", arg2="sql", dbname="main"
SQLITE_READ	arg1="sqlite_master", arg2="ROWID", dbname="main"
```

### SQLITE_CREATE_TEMP_TABLE

SQL:
```sql
CREATE TEMP TABLE demo_table (name TEXT)
```

Operations:

```
SQLITE_INSERT	arg1="sqlite_temp_master", dbname="temp"
SQLITE_CREATE_TEMP_TABLE	arg1="demo_table", dbname="temp"
SQLITE_UPDATE	arg1="sqlite_temp_master", arg2="type", dbname="temp"
SQLITE_UPDATE	arg1="sqlite_temp_master", arg2="name", dbname="temp"
SQLITE_UPDATE	arg1="sqlite_temp_master", arg2="tbl_name", dbname="temp"
SQLITE_UPDATE	arg1="sqlite_temp_master", arg2="rootpage", dbname="temp"
SQLITE_UPDATE	arg1="sqlite_temp_master", arg2="sql", dbname="temp"
SQLITE_READ	arg1="sqlite_temp_master", arg2="ROWID", dbname="temp"
```

### SQLITE_CREATE_TEMP_TRIGGER

Setup SQL:
```sql
CREATE TABLE demo_table (name TEXT)
```

SQL:
```sql
CREATE TEMP TRIGGER demo_trigger AFTER INSERT ON demo_table
  BEGIN
    INSERT INTO demo_table (name) VALUES ('Alice');
  END
```

Operations:

```
SQLITE_CREATE_TEMP_TRIGGER	arg1="demo_trigger", arg2="demo_table", dbname="temp"
SQLITE_INSERT	arg1="sqlite_master", dbname="main"
SQLITE_INSERT	arg1="sqlite_temp_master", dbname="temp"
```

### SQLITE_CREATE_TEMP_VIEW

SQL:
```sql
CREATE TEMP VIEW demo_view AS SELECT 1
```

Operations:

```
SQLITE_INSERT	arg1="sqlite_temp_master", dbname="temp"
SQLITE_CREATE_TEMP_VIEW	arg1="demo_view", dbname="temp"
SQLITE_UPDATE	arg1="sqlite_temp_master", arg2="type", dbname="temp"
SQLITE_UPDATE	arg1="sqlite_temp_master", arg2="name", dbname="temp"
SQLITE_UPDATE	arg1="sqlite_temp_master", arg2="tbl_name", dbname="temp"
SQLITE_UPDATE	arg1="sqlite_temp_master", arg2="rootpage", dbname="temp"
SQLITE_UPDATE	arg1="sqlite_temp_master", arg2="sql", dbname="temp"
SQLITE_READ	arg1="sqlite_temp_master", arg2="ROWID", dbname="temp"
```

### SQLITE_CREATE_TRIGGER

Setup SQL:
```sql
CREATE TABLE demo_table (name TEXT)
```

SQL:
```sql
CREATE TRIGGER demo_trigger AFTER INSERT ON demo_table
  BEGIN
    INSERT INTO demo_table (name) VALUES ('Alice');
  END
```

Operations:

```
SQLITE_CREATE_TRIGGER	arg1="demo_trigger", arg2="demo_table", dbname="main"
SQLITE_INSERT	arg1="sqlite_master", dbname="main"
SQLITE_INSERT	arg1="sqlite_master", dbname="main"
```

### SQLITE_CREATE_VIEW

SQL:
```sql
CREATE VIEW demo_view AS SELECT 1
```

Operations:

```
SQLITE_INSERT	arg1="sqlite_master", dbname="main"
SQLITE_CREATE_VIEW	arg1="demo_view", dbname="main"
SQLITE_UPDATE	arg1="sqlite_master", arg2="type", dbname="main"
SQLITE_UPDATE	arg1="sqlite_master", arg2="name", dbname="main"
SQLITE_UPDATE	arg1="sqlite_master", arg2="tbl_name", dbname="main"
SQLITE_UPDATE	arg1="sqlite_master", arg2="rootpage", dbname="main"
SQLITE_UPDATE	arg1="sqlite_master", arg2="sql", dbname="main"
SQLITE_READ	arg1="sqlite_master", arg2="ROWID", dbname="main"
```

### SQLITE_DELETE

Setup SQL:
```sql
CREATE TABLE demo_table (name TEXT);
INSERT INTO demo_table (name) VALUES ('Alice')
```

SQL:
```sql
DELETE FROM demo_table WHERE name='Alice'
```

Operations:

```
SQLITE_DELETE	arg1="demo_table", dbname="main"
SQLITE_READ	arg1="demo_table", arg2="name", dbname="main"
```

### SQLITE_DROP_INDEX

Setup SQL:
```sql
CREATE TABLE demo_table (name TEXT);
CREATE INDEX demo_index ON demo_table (name)
```

SQL:
```sql
DROP INDEX demo_index
```

Operations:

```
SQLITE_DELETE	arg1="sqlite_master", dbname="main"
SQLITE_DROP_INDEX	arg1="demo_index", arg2="demo_table", dbname="main"
SQLITE_DELETE	arg1="sqlite_master", dbname="main"
SQLITE_READ	arg1="sqlite_master", arg2="name", dbname="main"
SQLITE_READ	arg1="sqlite_master", arg2="type", dbname="main"
SQLITE_UPDATE	arg1="sqlite_master", arg2="rootpage", dbname="main"
SQLITE_READ	arg1="sqlite_master", arg2="rootpage", dbname="main"
```

### SQLITE_DROP_TABLE

Setup SQL:
```sql
CREATE TABLE demo_table (name TEXT)
```

SQL:
```sql
DROP TABLE demo_table
```

Operations:

```
SQLITE_DELETE	arg1="sqlite_master", dbname="main"
SQLITE_DROP_TABLE	arg1="demo_table", dbname="main"
SQLITE_DELETE	arg1="demo_table", dbname="main"
SQLITE_DELETE	arg1="sqlite_master", dbname="main"
SQLITE_READ	arg1="sqlite_master", arg2="tbl_name", dbname="main"
SQLITE_READ	arg1="sqlite_master", arg2="type", dbname="main"
SQLITE_UPDATE	arg1="sqlite_master", arg2="rootpage", dbname="main"
SQLITE_READ	arg1="sqlite_master", arg2="rootpage", dbname="main"
```

### SQLITE_DROP_TEMP_TABLE

Setup SQL:
```sql
CREATE TEMP TABLE demo_table (name TEXT)
```

SQL:
```sql
DROP TABLE demo_table
```

Operations:

```
SQLITE_DELETE	arg1="sqlite_temp_master", dbname="temp"
SQLITE_DROP_TEMP_TABLE	arg1="demo_table", dbname="temp"
SQLITE_DELETE	arg1="demo_table", dbname="temp"
SQLITE_DELETE	arg1="sqlite_temp_master", dbname="temp"
SQLITE_READ	arg1="sqlite_temp_master", arg2="tbl_name", dbname="temp"
SQLITE_READ	arg1="sqlite_temp_master", arg2="type", dbname="temp"
SQLITE_UPDATE	arg1="sqlite_temp_master", arg2="rootpage", dbname="temp"
SQLITE_READ	arg1="sqlite_temp_master", arg2="rootpage", dbname="temp"
```

### SQLITE_DROP_TEMP_TRIGGER

Setup SQL:
```sql
CREATE TABLE demo_table (name TEXT);
CREATE TEMP TRIGGER demo_trigger AFTER INSERT ON demo_table
  BEGIN
    INSERT INTO demo_table (name) VALUES ('Alice');
  END
```

SQL:
```sql
DROP TRIGGER demo_trigger
```

Operations:

```
SQLITE_DROP_TEMP_TRIGGER	arg1="demo_trigger", arg2="demo_table", dbname="temp"
SQLITE_DELETE	arg1="sqlite_temp_master", dbname="temp"
SQLITE_DELETE	arg1="sqlite_temp_master", dbname="temp"
SQLITE_READ	arg1="sqlite_temp_master", arg2="name", dbname="temp"
SQLITE_READ	arg1="sqlite_temp_master", arg2="type", dbname="temp"
```

### SQLITE_DROP_TEMP_VIEW

Setup SQL:
```sql
CREATE TEMP VIEW demo_view AS SELECT 1
```

SQL:
```sql
DROP VIEW demo_view
```

Operations:

```
SQLITE_DELETE	arg1="sqlite_temp_master", dbname="temp"
SQLITE_DROP_TEMP_VIEW	arg1="demo_view", dbname="temp"
SQLITE_DELETE	arg1="demo_view", dbname="temp"
SQLITE_DELETE	arg1="sqlite_temp_master", dbname="temp"
SQLITE_READ	arg1="sqlite_temp_master", arg2="tbl_name", dbname="temp"
SQLITE_READ	arg1="sqlite_temp_master", arg2="type", dbname="temp"
```

### SQLITE_DROP_TRIGGER

Setup SQL:
```sql
CREATE TABLE demo_table (name TEXT);
CREATE TRIGGER demo_trigger AFTER INSERT ON demo_table
  BEGIN
    INSERT INTO demo_table (name) VALUES ('Alice');
  END
```

SQL:
```sql
DROP TRIGGER demo_trigger
```

Operations:

```
SQLITE_DROP_TRIGGER	arg1="demo_trigger", arg2="demo_table", dbname="main"
SQLITE_DELETE	arg1="sqlite_master", dbname="main"
SQLITE_DELETE	arg1="sqlite_master", dbname="main"
SQLITE_READ	arg1="sqlite_master", arg2="name", dbname="main"
SQLITE_READ	arg1="sqlite_master", arg2="type", dbname="main"
```

### SQLITE_DROP_VIEW

Setup SQL:
```sql
CREATE VIEW demo_view AS SELECT 1
```

SQL:
```sql
DROP VIEW demo_view
```

Operations:

```
SQLITE_DELETE	arg1="sqlite_master", dbname="main"
SQLITE_DROP_VIEW	arg1="demo_view", dbname="main"
SQLITE_DELETE	arg1="demo_view", dbname="main"
SQLITE_DELETE	arg1="sqlite_master", dbname="main"
SQLITE_READ	arg1="sqlite_master", arg2="tbl_name", dbname="main"
SQLITE_READ	arg1="sqlite_master", arg2="type", dbname="main"
```

### SQLITE_INSERT

Setup SQL:
```sql
CREATE TABLE demo_table (name TEXT)
```

SQL:
```sql
INSERT INTO demo_table (name) VALUES ('Alice')
```

Operations:

```
SQLITE_INSERT	arg1="demo_table", dbname="main"
```

### SQLITE_PRAGMA

SQL:
```sql
PRAGMA foreign_keys; PRAGMA foreign_keys = ON
```

Operations:

```
SQLITE_PRAGMA	arg1="foreign_keys"
SQLITE_PRAGMA	arg1="foreign_keys", arg2="ON"
```

### SQLITE_READ

Setup SQL:
```sql
CREATE TABLE demo_table (name TEXT);
INSERT INTO demo_table (name) VALUES ('Alice')
```

SQL:
```sql
SELECT name FROM demo_table
```

Operations:

```
SQLITE_SELECT	
SQLITE_READ	arg1="demo_table", arg2="name", dbname="main"
```

### SQLITE_SELECT

Setup SQL:
```sql
CREATE TABLE demo_table (name TEXT);
INSERT INTO demo_table (name) VALUES ('Alice')
```

SQL:
```sql
SELECT name FROM demo_table
```

Operations:

```
SQLITE_SELECT	
SQLITE_READ	arg1="demo_table", arg2="name", dbname="main"
```

### SQLITE_TRANSACTION

Setup SQL:
```sql
CREATE TABLE demo_table (name TEXT)
```

SQL:
```sql
BEGIN TRANSACTION;
  INSERT INTO demo_table (name) VALUES ('Alice');
COMMIT
```

Operations:

```
SQLITE_TRANSACTION	arg1="BEGIN"
SQLITE_INSERT	arg1="demo_table", dbname="main"
SQLITE_TRANSACTION	arg1="COMMIT"
```

### SQLITE_UPDATE

Setup SQL:
```sql
CREATE TABLE demo_table (name TEXT);
INSERT INTO demo_table (name) VALUES ('Alice')
```

SQL:
```sql
UPDATE demo_table SET name='Bob' WHERE name='Alice'
```

Operations:

```
SQLITE_UPDATE	arg1="demo_table", arg2="name", dbname="main"
SQLITE_READ	arg1="demo_table", arg2="name", dbname="main"
```

### SQLITE_ATTACH

SQL:
```sql
ATTACH DATABASE ':memory:' AS second
```

Operations:

```
SQLITE_ATTACH	arg1=":memory:"
```

### SQLITE_DETACH

Setup SQL:
```sql
ATTACH DATABASE ':memory:' AS second
```

SQL:
```sql
DETACH DATABASE second
```

Operations:

```
SQLITE_DETACH	arg1="second"
```

### SQLITE_ALTER_TABLE

Setup SQL:
```sql
CREATE TABLE demo_table (name TEXT)
```

SQL:
```sql
ALTER TABLE demo_table ADD COLUMN age INTEGER
```

Operations:

```
SQLITE_ALTER_TABLE	arg1="main", arg2="demo_table"
SQLITE_FUNCTION	arg2="printf"
SQLITE_READ	arg1="sqlite_master", arg2="sql", dbname="main"
SQLITE_FUNCTION	arg2="substr"
SQLITE_READ	arg1="sqlite_master", arg2="sql", dbname="main"
SQLITE_FUNCTION	arg2="length"
SQLITE_FUNCTION	arg2="printf"
SQLITE_READ	arg1="sqlite_master", arg2="sql", dbname="main"
SQLITE_UPDATE	arg1="sqlite_master", arg2="sql", dbname="main"
SQLITE_READ	arg1="sqlite_master", arg2="type", dbname="main"
SQLITE_READ	arg1="sqlite_master", arg2="name", dbname="main"
```

SQL:
```sql
ALTER TABLE demo_table RENAME TO new_table
```

Operations:

```
SQLITE_ALTER_TABLE	arg1="main", arg2="demo_table"
SQLITE_FUNCTION	arg2="sqlite_rename_table"
SQLITE_READ	arg1="sqlite_master", arg2="type", dbname="main"
SQLITE_READ	arg1="sqlite_master", arg2="name", dbname="main"
SQLITE_READ	arg1="sqlite_master", arg2="sql", dbname="main"
SQLITE_UPDATE	arg1="sqlite_master", arg2="sql", dbname="main"
SQLITE_READ	arg1="sqlite_master", arg2="type", dbname="main"
SQLITE_READ	arg1="sqlite_master", arg2="tbl_name", dbname="main"
SQLITE_FUNCTION	arg2="like"
SQLITE_READ	arg1="sqlite_master", arg2="name", dbname="main"
SQLITE_UPDATE	arg1="sqlite_master", arg2="tbl_name", dbname="main"
SQLITE_READ	arg1="sqlite_master", arg2="type", dbname="main"
SQLITE_FUNCTION	arg2="like"
SQLITE_READ	arg1="sqlite_master", arg2="name", dbname="main"
SQLITE_READ	arg1="sqlite_master", arg2="type", dbname="main"
SQLITE_FUNCTION	arg2="substr"
SQLITE_READ	arg1="sqlite_master", arg2="name", dbname="main"
SQLITE_READ	arg1="sqlite_master", arg2="name", dbname="main"
SQLITE_UPDATE	arg1="sqlite_master", arg2="name", dbname="main"
SQLITE_READ	arg1="sqlite_master", arg2="tbl_name", dbname="main"
SQLITE_READ	arg1="sqlite_master", arg2="type", dbname="main"
SQLITE_READ	arg1="sqlite_master", arg2="type", dbname="main"
SQLITE_READ	arg1="sqlite_master", arg2="type", dbname="main"
SQLITE_FUNCTION	arg2="sqlite_rename_table"
SQLITE_READ	arg1="sqlite_temp_master", arg2="type", dbname="temp"
SQLITE_READ	arg1="sqlite_temp_master", arg2="name", dbname="temp"
SQLITE_READ	arg1="sqlite_temp_master", arg2="sql", dbname="temp"
SQLITE_UPDATE	arg1="sqlite_temp_master", arg2="sql", dbname="temp"
SQLITE_READ	arg1="sqlite_temp_master", arg2="tbl_name", dbname="temp"
SQLITE_FUNCTION	arg2="sqlite_rename_test"
SQLITE_READ	arg1="sqlite_temp_master", arg2="sql", dbname="temp"
SQLITE_READ	arg1="sqlite_temp_master", arg2="type", dbname="temp"
SQLITE_READ	arg1="sqlite_temp_master", arg2="name", dbname="temp"
SQLITE_READ	arg1="sqlite_temp_master", arg2="tbl_name", dbname="temp"
SQLITE_UPDATE	arg1="sqlite_temp_master", arg2="tbl_name", dbname="temp"
SQLITE_READ	arg1="sqlite_temp_master", arg2="type", dbname="temp"
SQLITE_SELECT	
SQLITE_FUNCTION	arg2="like"
SQLITE_READ	arg1="sqlite_master", arg2="name", dbname="main"
SQLITE_FUNCTION	arg2="like"
SQLITE_READ	arg1="sqlite_master", arg2="sql", dbname="main"
SQLITE_FUNCTION	arg2="sqlite_rename_test"
SQLITE_READ	arg1="sqlite_master", arg2="sql", dbname="main"
SQLITE_READ	arg1="sqlite_master", arg2="type", dbname="main"
SQLITE_READ	arg1="sqlite_master", arg2="name", dbname="main"
SQLITE_SELECT	
SQLITE_FUNCTION	arg2="like"
SQLITE_READ	arg1="sqlite_temp_master", arg2="name", dbname="temp"
SQLITE_FUNCTION	arg2="like"
SQLITE_READ	arg1="sqlite_temp_master", arg2="sql", dbname="temp"
SQLITE_FUNCTION	arg2="sqlite_rename_test"
SQLITE_READ	arg1="sqlite_temp_master", arg2="sql", dbname="temp"
SQLITE_READ	arg1="sqlite_temp_master", arg2="type", dbname="temp"
SQLITE_READ	arg1="sqlite_temp_master", arg2="name", dbname="temp"
```

### SQLITE_REINDEX

Setup SQL:
```sql
CREATE TABLE demo_table (name TEXT);
CREATE INDEX demo_index ON demo_table (name)
```

SQL:
```sql
REINDEX demo_index
```

Operations:

```
SQLITE_REINDEX	arg1="demo_index", dbname="main"
```

### SQLITE_ANALYZE

Setup SQL:
```sql
CREATE TABLE demo_table (name TEXT);
CREATE INDEX demo_index ON demo_table (name)
```

SQL:
```sql
ANALYZE
```

Operations:

```
SQLITE_INSERT	arg1="sqlite_master", dbname="main"
SQLITE_CREATE_TABLE	arg1="sqlite_stat1", dbname="main"
SQLITE_UPDATE	arg1="sqlite_master", arg2="type", dbname="main"
SQLITE_UPDATE	arg1="sqlite_master", arg2="name", dbname="main"
SQLITE_UPDATE	arg1="sqlite_master", arg2="tbl_name", dbname="main"
SQLITE_UPDATE	arg1="sqlite_master", arg2="rootpage", dbname="main"
SQLITE_UPDATE	arg1="sqlite_master", arg2="sql", dbname="main"
SQLITE_READ	arg1="sqlite_master", arg2="ROWID", dbname="main"
SQLITE_ANALYZE	arg1="demo_table", dbname="main"
SQLITE_SELECT	
SQLITE_READ	arg1="sqlite_stat1", arg2="tbl", dbname="main"
SQLITE_READ	arg1="sqlite_stat1", arg2="idx", dbname="main"
SQLITE_READ	arg1="sqlite_stat1", arg2="stat", dbname="main"
```

### SQLITE_CREATE_VTABLE

SQL:
```sql
CREATE VIRTUAL TABLE demo_table USING fts5(name)
```

Operations:

```
SQLITE_INSERT	arg1="sqlite_master", dbname="main"
SQLITE_CREATE_VTABLE	arg1="demo_table", arg2="fts5", dbname="main"
SQLITE_UPDATE	arg1="sqlite_master", arg2="type", dbname="main"
SQLITE_UPDATE	arg1="sqlite_master", arg2="name", dbname="main"
SQLITE_UPDATE	arg1="sqlite_master", arg2="tbl_name", dbname="main"
SQLITE_UPDATE	arg1="sqlite_master", arg2="rootpage", dbname="main"
SQLITE_UPDATE	arg1="sqlite_master", arg2="sql", dbname="main"
SQLITE_READ	arg1="sqlite_master", arg2="ROWID", dbname="main"
SQLITE_INSERT	arg1="sqlite_master", dbname="main"
SQLITE_CREATE_TABLE	arg1="demo_table_data", dbname="main"
SQLITE_UPDATE	arg1="sqlite_master", arg2="type", dbname="main"
SQLITE_UPDATE	arg1="sqlite_master", arg2="name", dbname="main"
SQLITE_UPDATE	arg1="sqlite_master", arg2="tbl_name", dbname="main"
SQLITE_UPDATE	arg1="sqlite_master", arg2="rootpage", dbname="main"
SQLITE_UPDATE	arg1="sqlite_master", arg2="sql", dbname="main"
SQLITE_READ	arg1="sqlite_master", arg2="ROWID", dbname="main"
SQLITE_INSERT	arg1="sqlite_master", dbname="main"
SQLITE_CREATE_TABLE	arg1="demo_table_idx", dbname="main"
SQLITE_INSERT	arg1="sqlite_master", dbname="main"
SQLITE_CREATE_INDEX	arg1="sqlite_autoindex_demo_table_idx_1", arg2="demo_table_idx", dbname="main"
SQLITE_READ	arg1="demo_table_idx", arg2="segid", dbname="main"
SQLITE_READ	arg1="demo_table_idx", arg2="term", dbname="main"
SQLITE_INSERT	arg1="sqlite_master", dbname="main"
SQLITE_UPDATE	arg1="sqlite_master", arg2="type", dbname="main"
SQLITE_UPDATE	arg1="sqlite_master", arg2="name", dbname="main"
SQLITE_UPDATE	arg1="sqlite_master", arg2="tbl_name", dbname="main"
SQLITE_UPDATE	arg1="sqlite_master", arg2="rootpage", dbname="main"
SQLITE_UPDATE	arg1="sqlite_master", arg2="sql", dbname="main"
SQLITE_READ	arg1="sqlite_master", arg2="ROWID", dbname="main"
SQLITE_INSERT	arg1="demo_table_data", dbname="main"
SQLITE_INSERT	arg1="sqlite_master", dbname="main"
SQLITE_CREATE_TABLE	arg1="demo_table_content", dbname="main"
SQLITE_UPDATE	arg1="sqlite_master", arg2="type", dbname="main"
SQLITE_UPDATE	arg1="sqlite_master", arg2="name", dbname="main"
SQLITE_UPDATE	arg1="sqlite_master", arg2="tbl_name", dbname="main"
SQLITE_UPDATE	arg1="sqlite_master", arg2="rootpage", dbname="main"
SQLITE_UPDATE	arg1="sqlite_master", arg2="sql", dbname="main"
SQLITE_READ	arg1="sqlite_master", arg2="ROWID", dbname="main"
SQLITE_INSERT	arg1="sqlite_master", dbname="main"
SQLITE_CREATE_TABLE	arg1="demo_table_docsize", dbname="main"
SQLITE_UPDATE	arg1="sqlite_master", arg2="type", dbname="main"
SQLITE_UPDATE	arg1="sqlite_master", arg2="name", dbname="main"
SQLITE_UPDATE	arg1="sqlite_master", arg2="tbl_name", dbname="main"
SQLITE_UPDATE	arg1="sqlite_master", arg2="rootpage", dbname="main"
SQLITE_UPDATE	arg1="sqlite_master", arg2="sql", dbname="main"
SQLITE_READ	arg1="sqlite_master", arg2="ROWID", dbname="main"
SQLITE_INSERT	arg1="sqlite_master", dbname="main"
SQLITE_CREATE_TABLE	arg1="demo_table_config", dbname="main"
SQLITE_INSERT	arg1="sqlite_master", dbname="main"
SQLITE_CREATE_INDEX	arg1="sqlite_autoindex_demo_table_config_1", arg2="demo_table_config", dbname="main"
SQLITE_READ	arg1="demo_table_config", arg2="k", dbname="main"
SQLITE_INSERT	arg1="sqlite_master", dbname="main"
SQLITE_UPDATE	arg1="sqlite_master", arg2="type", dbname="main"
SQLITE_UPDATE	arg1="sqlite_master", arg2="name", dbname="main"
SQLITE_UPDATE	arg1="sqlite_master", arg2="tbl_name", dbname="main"
SQLITE_UPDATE	arg1="sqlite_master", arg2="rootpage", dbname="main"
SQLITE_UPDATE	arg1="sqlite_master", arg2="sql", dbname="main"
SQLITE_READ	arg1="sqlite_master", arg2="ROWID", dbname="main"
SQLITE_INSERT	arg1="demo_table_config", dbname="main"
SQLITE_PRAGMA	arg1="data_version", dbname="main"
SQLITE_SELECT	
SQLITE_READ	arg1="demo_table_config", arg2="k", dbname="main"
SQLITE_READ	arg1="demo_table_config", arg2="v", dbname="main"
```

### SQLITE_DROP_VTABLE

Setup SQL:
```sql
CREATE VIRTUAL TABLE demo_table USING fts5(name)
```

SQL:
```sql
DROP TABLE demo_table
```

Operations:

```
SQLITE_DELETE	arg1="sqlite_master", dbname="main"
SQLITE_DROP_VTABLE	arg1="demo_table", arg2="fts5", dbname="main"
SQLITE_DELETE	arg1="demo_table", dbname="main"
SQLITE_DELETE	arg1="sqlite_master", dbname="main"
SQLITE_READ	arg1="sqlite_master", arg2="tbl_name", dbname="main"
SQLITE_READ	arg1="sqlite_master", arg2="type", dbname="main"
SQLITE_DELETE	arg1="sqlite_master", dbname="main"
SQLITE_DROP_TABLE	arg1="demo_table_data", dbname="main"
SQLITE_DELETE	arg1="demo_table_data", dbname="main"
SQLITE_DELETE	arg1="sqlite_master", dbname="main"
SQLITE_READ	arg1="sqlite_master", arg2="tbl_name", dbname="main"
SQLITE_READ	arg1="sqlite_master", arg2="type", dbname="main"
SQLITE_UPDATE	arg1="sqlite_master", arg2="rootpage", dbname="main"
SQLITE_READ	arg1="sqlite_master", arg2="rootpage", dbname="main"
SQLITE_DELETE	arg1="sqlite_master", dbname="main"
SQLITE_DROP_TABLE	arg1="demo_table_idx", dbname="main"
SQLITE_DELETE	arg1="demo_table_idx", dbname="main"
SQLITE_DELETE	arg1="sqlite_master", dbname="main"
SQLITE_READ	arg1="sqlite_master", arg2="tbl_name", dbname="main"
SQLITE_READ	arg1="sqlite_master", arg2="type", dbname="main"
SQLITE_UPDATE	arg1="sqlite_master", arg2="rootpage", dbname="main"
SQLITE_READ	arg1="sqlite_master", arg2="rootpage", dbname="main"
SQLITE_DELETE	arg1="sqlite_master", dbname="main"
SQLITE_DROP_TABLE	arg1="demo_table_config", dbname="main"
SQLITE_DELETE	arg1="demo_table_config", dbname="main"
SQLITE_DELETE	arg1="sqlite_master", dbname="main"
SQLITE_READ	arg1="sqlite_master", arg2="tbl_name", dbname="main"
SQLITE_READ	arg1="sqlite_master", arg2="type", dbname="main"
SQLITE_UPDATE	arg1="sqlite_master", arg2="rootpage", dbname="main"
SQLITE_READ	arg1="sqlite_master", arg2="rootpage", dbname="main"
SQLITE_DELETE	arg1="sqlite_master", dbname="main"
SQLITE_DROP_TABLE	arg1="demo_table_docsize", dbname="main"
SQLITE_DELETE	arg1="demo_table_docsize", dbname="main"
SQLITE_DELETE	arg1="sqlite_master", dbname="main"
SQLITE_READ	arg1="sqlite_master", arg2="tbl_name", dbname="main"
SQLITE_READ	arg1="sqlite_master", arg2="type", dbname="main"
SQLITE_UPDATE	arg1="sqlite_master", arg2="rootpage", dbname="main"
SQLITE_READ	arg1="sqlite_master", arg2="rootpage", dbname="main"
SQLITE_DELETE	arg1="sqlite_master", dbname="main"
SQLITE_DROP_TABLE	arg1="demo_table_content", dbname="main"
SQLITE_DELETE	arg1="demo_table_content", dbname="main"
SQLITE_DELETE	arg1="sqlite_master", dbname="main"
SQLITE_READ	arg1="sqlite_master", arg2="tbl_name", dbname="main"
SQLITE_READ	arg1="sqlite_master", arg2="type", dbname="main"
SQLITE_UPDATE	arg1="sqlite_master", arg2="rootpage", dbname="main"
SQLITE_READ	arg1="sqlite_master", arg2="rootpage", dbname="main"
```

### SQLITE_FUNCTION

SQL:
```sql
SELECT upper('Alice')
```

Operations:

```
SQLITE_SELECT	
SQLITE_FUNCTION	arg2="upper"
```

### SQLITE_SAVEPOINT

Setup SQL:
```sql
CREATE TABLE demo_table (name TEXT)
```

SQL:
```sql
SAVEPOINT demo_savepoint
```

Operations:

```
SQLITE_SAVEPOINT	arg1="BEGIN", arg2="demo_savepoint"
```

### SQLITE_RECURSIVE

SQL:
```sql
WITH RECURSIVE counter(n) AS (
  SELECT 1 UNION ALL
  SELECT n+1 FROM counter WHERE n<5
)
SELECT n FROM counter;
```

Operations:

```
SQLITE_SELECT	
SQLITE_SELECT	innermost_trigger_or_view="counter"
SQLITE_RECURSIVE	innermost_trigger_or_view="counter"
SQLITE_SELECT	innermost_trigger_or_view="counter"
SQLITE_SELECT	innermost_trigger_or_view="counter"
```

## Operation constants

| ID | Operation |
| --- | --- |
| 1 | SQLITE_CREATE_INDEX |
| 2 | SQLITE_CREATE_TABLE |
| 3 | SQLITE_CREATE_TEMP_INDEX |
| 4 | SQLITE_CREATE_TEMP_TABLE |
| 5 | SQLITE_CREATE_TEMP_TRIGGER |
| 6 | SQLITE_CREATE_TEMP_VIEW |
| 7 | SQLITE_CREATE_TRIGGER |
| 8 | SQLITE_CREATE_VIEW |
| 9 | SQLITE_DELETE |
| 10 | SQLITE_DROP_INDEX |
| 11 | SQLITE_DROP_TABLE |
| 12 | SQLITE_DROP_TEMP_INDEX |
| 13 | SQLITE_DROP_TEMP_TABLE |
| 14 | SQLITE_DROP_TEMP_TRIGGER |
| 15 | SQLITE_DROP_TEMP_VIEW |
| 16 | SQLITE_DROP_TRIGGER |
| 17 | SQLITE_DROP_VIEW |
| 18 | SQLITE_INSERT |
| 19 | SQLITE_PRAGMA |
| 20 | SQLITE_READ |
| 21 | SQLITE_SELECT |
| 22 | SQLITE_TRANSACTION |
| 23 | SQLITE_UPDATE |
| 24 | SQLITE_ATTACH |
| 25 | SQLITE_DETACH |
| 26 | SQLITE_ALTER_TABLE |
| 27 | SQLITE_REINDEX |
| 28 | SQLITE_ANALYZE |
| 29 | SQLITE_CREATE_VTABLE |
| 30 | SQLITE_DROP_VTABLE |
| 31 | SQLITE_FUNCTION |
| 32 | SQLITE_SAVEPOINT |
| 33 | SQLITE_RECURSIVE |
