# /query-gta Command

Execute SQL queries against the GTA/DPA database.

## Usage

```
/query-gta [sql_query]
/query-gta SELECT * FROM gta_intervention LIMIT 10
/query-gta SHOW TABLES
```

## Examples

### List all tables
```
/query-gta SHOW TABLES
```

### Get intervention by ID
```
/query-gta SELECT * FROM gta_intervention WHERE id = 12345
```

### Count interventions by country
```
/query-gta SELECT implementing_jurisdiction, COUNT(*) as count FROM gta_intervention GROUP BY implementing_jurisdiction ORDER BY count DESC LIMIT 20
```

### Describe table structure
```
/query-gta DESCRIBE gta_intervention
```

## Behavior

1. Loads database credentials from `.env` file (in `jf-thought/sgept-analytics/data-queries/`)
2. Connects to GTA database (read-only by default)
3. Executes the provided SQL query
4. Returns results as formatted table
5. Automatically limits to 1000 rows if no LIMIT specified

## Safety

- Uses read-only credentials by default
- Parameterized queries prevent SQL injection
- Maximum 10,000 rows per query
- Connection timeout: 30 seconds

## Prerequisites

Ensure `.env` file exists in `jf-thought/sgept-analytics/data-queries/` with database credentials:
```
GTA_DB_HOST=...
GTA_DB_USER=...
GTA_DB_PASSWORD=...
GTA_DB_NAME=gtaapi
GTA_DB_PORT=3306
```
