---
paths:
  - sgept-analytics/**
  - "*/data-queries/**"
  - "**/*.R"
---

# R Code Standards

**Purpose:** Enforce consistent R code quality across all analytical projects in `jf-thought/sgept-analytics/data-queries/`.

---

## Package Management

### Loading Order

```r
# 1. Load packages at top of script
library(tidyverse)     # Data manipulation
library(lubridate)     # Date/time handling
library(gtalibrary)    # GTA database wrappers
library(gtasql)        # SQL helpers
library(RMariaDB)      # Direct database connections
library(openxlsx)      # Excel export

# 2. Set constants
THRESHOLD <- 0.85
MAX_RESULTS <- 1000

# 3. Define functions
# 4. Execute main logic
```

### Package Installation

```r
# Use explicit repository
install.packages("package_name", repos = "https://cloud.r-project.org/")

# For GTA-specific packages
# These are already installed in the standard environment
```

---

## Naming Conventions

### Variables and Functions

| Type | Convention | Example |
|------|------------|---------|
| **Variables** | snake_case | `trade_value`, `intervention_count` |
| **Functions** | snake_case | `calculate_trade_coverage()`, `clean_firm_names()` |
| **Constants** | UPPER_SNAKE_CASE | `MAX_RESULTS`, `JARO_WINKLER_THRESHOLD` |
| **Boolean** | is_/has_/should_ prefix | `is_active`, `has_data`, `should_filter` |

### File Naming

| Type | Convention | Example |
|------|------------|---------|
| **Scripts** | Numbered prefix for execution order | `0 data prep.R`, `1 Analysis.R` |
| **Data files** | Descriptive, lowercase, underscores | `trade_data_2024.csv`, `processed_interventions.Rdata` |
| **Output files** | Descriptive with type suffix | `summary_table.xlsx`, `trend_chart.png` |

---

## Code Style

### Pipe Operator

```r
# ✅ CORRECT: One operation per line
processed <- raw_data %>%
  filter(!is.na(value)) %>%
  mutate(year = year(date)) %>%
  group_by(country, year) %>%
  summarize(total = sum(value), .groups = "drop")

# ❌ WRONG: Multiple operations on one line
processed <- raw_data %>% filter(!is.na(value)) %>% mutate(year = year(date))
```

### Function Definition

```r
# ✅ CORRECT: Clear documentation, typed-like comments
#' Calculate trade coverage for interventions
#'
#' @param interventions tibble with intervention data
#' @param trade_data tibble with trade flows
#' @return tibble with coverage statistics
calculate_trade_coverage <- function(interventions, trade_data) {
  # Early return for invalid input
  if (nrow(interventions) == 0) {
    return(tibble())
  }

  # Main logic
  result <- interventions %>%
    left_join(trade_data, by = "hs_code") %>%
    summarize(coverage = sum(trade_value, na.rm = TRUE))

  return(result)
}
```

### Assignments

```r
# ✅ CORRECT: Use <- for assignment
x <- 5
my_data <- read_csv("data.csv")

# ❌ WRONG: Don't use = for assignment (except in function arguments)
x = 5
```

---

## Error Handling

### Database Operations

```r
# Always wrap database calls in tryCatch
tryCatch({
  gta_sql_pool_open(pool.name = "main", db.title = "gta_main")
  result <- gta_sql_get_value(query, "main")
  gta_sql_pool_close("main")
}, error = function(e) {
  message(paste("Database error:", e$message))
  message("Check GTA_HOST, GTA_PORT, GTA_USER, GTA_DB_KEY in .env")
  return(NULL)
}, finally = {
  # Ensure connection is closed even on error
  tryCatch(gta_sql_pool_close("main"), error = function(e) NULL)
})
```

### Input Validation

```r
# Validate required columns
required_cols <- c("id", "value", "date")
missing_cols <- setdiff(required_cols, names(data))
if (length(missing_cols) > 0) {
  stop(paste("Missing required columns:", paste(missing_cols, collapse = ", ")))
}

# Use stopifnot for assertions
stopifnot(
  "Data must have required columns" =
    all(c("id", "value", "date") %in% names(data))
)
```

### Missing Value Handling

```r
# Explicit NA handling
data <- data %>%
  filter(!is.na(value)) %>%                    # Remove NA values
  mutate(date = coalesce(date, Sys.Date()))   # Default for NA dates

# Document NA strategy in comments
# Strategy: Remove rows with NA in key columns, impute NA in optional columns
```

---

## Data Manipulation

### Joins

```r
# ✅ CORRECT: Explicit join columns
result <- interventions %>%
  left_join(trade_data, by = c("hs_code" = "product_code"))

# ✅ CORRECT: Multiple join columns
result <- data_a %>%
  inner_join(data_b, by = c("country", "year", "product"))

# ❌ WRONG: Relying on automatic column matching
result <- interventions %>%
  left_join(trade_data)  # Ambiguous, may fail silently
```

### Grouping

```r
# Always specify .groups in summarize
result <- data %>%
  group_by(country, year) %>%
  summarize(
    total = sum(value),
    count = n(),
    .groups = "drop"  # or "keep", "drop_last"
  )
```

### Type Coercion

```r
# Be explicit about type conversions
data <- data %>%
  mutate(
    date = as.Date(date_string, format = "%Y-%m-%d"),
    value = as.numeric(value_string),
    year = as.integer(year(date))
  )
```

---

## Database Queries

### GTA Database Pattern

```r
library(gtalibrary)
library(gtasql)

# Open connection pool (do once at start)
gta_sql_pool_open(pool.name = "main", db.title = "gta_main")

# Execute parameterized query (prevents SQL injection)
interventions <- gta_sql_get_value(
  "SELECT id, title, implementing_jurisdiction
   FROM gta_intervention
   WHERE implementing_jurisdiction = ?
     AND date_implemented >= ?",
  "main",
  params = list("USA", "2020-01-01")
)

# Close connection pool (do at end)
gta_sql_pool_close("main")
```

### Query Best Practices

```r
# ✅ CORRECT: Use parameterized queries
gta_sql_get_value(
  "SELECT * FROM table WHERE id = ?",
  "main",
  params = list(my_id)
)

# ❌ WRONG: String interpolation (SQL injection risk)
gta_sql_get_value(
  paste0("SELECT * FROM table WHERE id = ", my_id),
  "main"
)
```

---

## Output Formatting

### Excel Export

```r
library(openxlsx)

# Create workbook with styling
wb <- createWorkbook()
addWorksheet(wb, "Results")

# Write data with table formatting
writeDataTable(
  wb, "Results", data,
  tableStyle = "TableStyleMedium2",
  headerStyle = createStyle(textDecoration = "bold")
)

# Freeze header row
freezePane(wb, "Results", firstRow = TRUE)

# Auto-width columns
setColWidths(wb, "Results", cols = 1:ncol(data), widths = "auto")

# Save
saveWorkbook(wb, "results/output.xlsx", overwrite = TRUE)
```

### Visualization

GTA charts use a **cowplot composition** with the plot area, title, legend, logo, and decorative elements assembled externally. Do NOT use ggplot's `labs(title=...)` for publication charts.

```r
library(ggplot2)
library(cowplot)
library(magick)   # Required by cowplot::draw_image
library(png)
library(grid)

# --- GTA Colour Palette ---
gta_colors <- list(
  navy = "#003366",              # Dark navy (top bar, emphasis lines)
  dark_blue = "#002A5C",         # Darker navy variant
  light_blue = "#6BAED6",       # Light blue (secondary lines)
  equity_stake = "#1f77b4",     # Blue
  debt_purchase = "#2ca02c",    # Green
  state_loan = "#ff7f0e",       # Orange
  loan_guarantee = "#d62728",   # Red
  financial_grant = "#9467bd",  # Purple
  neutral_grey = "#D3D3D3",     # Light grey for de-emphasis
  text_dark = "#1a1a2e",        # Near-black for titles
  text_grey = "grey40",
  bg = "#E8EEF5"                # Light blue chart background
)

# --- GTA Logo ---
# Located at: jf-ceo/sgept-backoffice/assets/gta-logos/
# Use "GTA Logo Color light.png" for light backgrounds
# Use "GTA Logo Color dark.png" for dark backgrounds

# --- Typography ---
# Roboto is the GTA/SGEPT standard typeface.
# Install once per session:
library(sysfonts)
library(showtext)
font_add_google("Roboto", "Roboto")
showtext_auto()

# --- GTA Base Theme (for the inner ggplot only) ---
# Title, subtitle, legend, source, and logo are added by cowplot externally.
theme_gta <- theme_minimal(base_size = 12, base_family = "Roboto") +
  theme(
    plot.background = element_rect(fill = "#E8EEF5", colour = NA),
    panel.background = element_rect(fill = "#E8EEF5", colour = NA),
    axis.text = element_text(size = 10, color = "grey30", family = "Roboto"),
    axis.title = element_text(size = 10, color = "grey40", family = "Roboto"),
    axis.line.x.bottom = element_line(color = "grey30", linewidth = 0.5),
    axis.ticks = element_blank(),
    panel.grid.minor = element_blank(),
    panel.grid.major.x = element_blank(),
    panel.grid.major.y = element_line(color = "grey85", linewidth = 0.3),
    legend.position = "none",         # Legend placed by cowplot
    plot.margin = margin(5, 15, 5, 10)
  )

# --- Publication-Ready Chart Template ---
# Step 1: Create ggplot WITHOUT title/subtitle/caption (cowplot handles these)
main_chart <- ggplot(data, aes(x = year, y = value)) +
  geom_line(color = gta_colors$navy, linewidth = 1.5) +
  scale_y_continuous(position = "right") +    # Y-axis on the RIGHT
  labs(x = NULL, y = NULL) +
  theme_gta

# Step 2: Compose with cowplot
logo_path <- "/path/to/GTA Logo Color light.png"

final <- ggdraw() +
  # Background
  draw_grob(rectGrob(gp = gpar(fill = "#E8EEF5", col = NA))) +
  # Full-width navy bar at top (edge to edge)
  draw_line(x = c(0, 1), y = c(0.96, 0.96),
            color = "#003366", size = 3) +
  # Title (large bold, single line, ~24pt, Roboto Medium)
  draw_label("Key Finding as Active Statement",
             x = 0.04, y = 0.91, hjust = 0, vjust = 1,
             fontface = "bold", size = 24, color = "#1a1a2e",
             fontfamily = "Roboto") +
  # Subtitle (grey, ~11pt, Roboto Light)
  draw_label("Descriptive context, variable, time period",
             x = 0.04, y = 0.855, hjust = 0, vjust = 1,
             size = 11, color = "grey40",
             fontfamily = "Roboto") +
  # Legend (manual line segments + labels)
  draw_line(x = c(0.06, 0.12), y = c(0.82, 0.82),
            color = "#003366", size = 1.5) +
  draw_label("Series A", x = 0.13, y = 0.82,
             hjust = 0, size = 9, color = "grey30") +
  # Main chart
  draw_plot(main_chart, x = 0, y = 0.06, width = 1, height = 0.73) +
  # Source (bottom-left)
  draw_label("Source: Global Trade Alert",
             x = 0.04, y = 0.025, hjust = 0,
             size = 9, color = "grey40") +
  # GTA logo (bottom-right)
  draw_image(logo_path, x = 0.68, y = 0.005,
             width = 0.28, height = 0.05)

# Step 3: Save at publication resolution
ggsave("results/chart.png", final, width = 10, height = 7, dpi = 300,
       bg = "#E8EEF5")
```

**Key conventions:**
- Full-width dark navy bar (#003366) at the top, edge to edge (x = 0 to 1)
- Title: ~24pt bold, single line, below the bar, black text
- Subtitle: ~11pt grey, below title
- Y-axis on the RIGHT (percentage charts especially)
- Legend: manual line segments via `draw_line` + `draw_label`, positioned below subtitle
- Source caption: bottom-left
- GTA logo: bottom-right (use `GTA Logo Color light.png`)
- Background: #E8EEF5 throughout
- Reference chart: `chart_intermediary_actions.R`

---

## Code Organization

### Script Structure

```r
# ============================================================================
# Script: 0 data prep.R
# Purpose: Load and clean intervention data for analysis
# Author: [Analyst Name]
# Date: YYYY-MM-DD
# ============================================================================

# --- 1. Setup ---------------------------------------------------------------
library(tidyverse)
library(gtalibrary)

# --- 2. Constants -----------------------------------------------------------
START_DATE <- "2020-01-01"
END_DATE <- "2024-12-31"

# --- 3. Functions -----------------------------------------------------------
clean_intervention_data <- function(data) {
  # ... function implementation
}

# --- 4. Data Loading --------------------------------------------------------
gta_sql_pool_open(pool.name = "main", db.title = "gta_main")
raw_data <- gta_sql_get_value(query, "main")
gta_sql_pool_close("main")

# --- 5. Processing ----------------------------------------------------------
cleaned_data <- clean_intervention_data(raw_data)

# --- 6. Output --------------------------------------------------------------
save(cleaned_data, file = "data/cleaned_interventions.Rdata")
message(paste("Saved", nrow(cleaned_data), "records"))
```

### Modular Code

```r
# Prefer small, focused functions over long scripts
# Each function should do ONE thing

# ❌ WRONG: 200-line monolithic function
process_everything <- function(data) {
  # ... 200 lines of everything
}

# ✅ CORRECT: Composable functions
process_data <- function(data) {
  data %>%
    validate_input() %>%
    clean_values() %>%
    transform_structure() %>%
    calculate_metrics()
}
```

---

## Common Anti-Patterns

### Avoid These Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| `attach()` | Pollutes namespace, causes bugs | Use explicit `data$column` or pipe |
| `setwd()` in scripts | Breaks portability | Use project-relative paths |
| `rm(list=ls())` | Hides environment issues | Restart R session instead |
| `T` and `F` for booleans | Can be overwritten | Use `TRUE` and `FALSE` |
| Nested `for` loops | Slow, hard to read | Use `purrr::map()` or vectorized ops |
| `sapply()` | Unpredictable return type | Use `vapply()` or `map_*()` |

### Example Corrections

```r
# ❌ WRONG: Using setwd
setwd("/path/to/project")
data <- read_csv("data/input.csv")

# ✅ CORRECT: Use here package or relative paths
library(here)
data <- read_csv(here("data", "input.csv"))

# ❌ WRONG: Using T/F
if (condition == T) { ... }

# ✅ CORRECT: Use TRUE/FALSE
if (condition == TRUE) { ... }
# Or better:
if (condition) { ... }
```

---

## Performance Guidelines

### Large Data Operations

```r
# Use data.table for very large datasets (>1M rows)
library(data.table)
dt <- fread("large_file.csv")
result <- dt[country == "USA", .(total = sum(value)), by = year]

# Use parallel processing for independent operations
library(furrr)
plan(multisession, workers = 4)
results <- future_map(file_list, process_file)
```

### Memory Management

```r
# Remove large objects when no longer needed
rm(large_data)
gc()  # Force garbage collection

# Read only needed columns
data <- read_csv("large_file.csv", col_select = c(id, value, date))
```

---

## Documentation

### Script Headers

Every script should have a header explaining:
- Purpose of the script
- Inputs (files, parameters)
- Outputs (files created)
- Dependencies (packages, other scripts)

### Inline Comments

```r
# Comment WHY, not WHAT
# ✅ CORRECT: Explains reasoning
# Filter to 2020+ because policy change affected earlier data
data <- data %>% filter(year >= 2020)

# ❌ WRONG: Restates code
# Filter data to years >= 2020
data <- data %>% filter(year >= 2020)
```
