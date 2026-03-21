---
paths:
  - sgept-analytics/**
  - "*/data-queries/**"
---

# Data Handling Rules

**Purpose:** Ensure data quality, reproducibility, and accuracy across all analytical projects in `jf-thought/sgept-analytics/data-queries/`.

---

## Data Validation Requirements

### Required Checks (Before Analysis)

Every dataset must pass these validation checks before proceeding with analysis:

| Check | Description | Threshold | Action if Failed |
|-------|-------------|-----------|------------------|
| **Row count** | Verify expected data volume | ±10% of expected | Investigate source |
| **Missing values** | Identify columns with gaps | Flag if >20% missing | Document or impute |
| **Duplicate keys** | Check for duplicate primary keys | 0 duplicates allowed | Deduplicate with logic |
| **Date ranges** | Verify temporal coverage | No unexpected gaps | Document gaps |
| **Outliers** | Flag extreme values | >3× IQR from median | Review individually |

### Implementation

```r
#' Validate dataset before analysis
#' @param data tibble to validate
#' @param expected_rows expected row count (optional)
#' @param key_cols primary key columns for duplicate check
#' @return validation report
validate_dataset <- function(data, expected_rows = NULL, key_cols = NULL) {
  report <- list()

  # Row count check
  actual_rows <- nrow(data)
  report$row_count <- actual_rows
  if (!is.null(expected_rows)) {
    deviation <- abs(actual_rows - expected_rows) / expected_rows
    report$row_count_ok <- deviation <= 0.10
    if (!report$row_count_ok) {
      warning(paste("Row count deviation:", round(deviation * 100, 1), "%"))
    }
  }

  # Missing value check
  missing_pct <- sapply(data, function(x) sum(is.na(x)) / length(x) * 100)
  report$missing_values <- missing_pct[missing_pct > 0]
  high_missing <- names(missing_pct[missing_pct > 20])
  if (length(high_missing) > 0) {
    warning(paste("High missing values (>20%):", paste(high_missing, collapse = ", ")))
  }

  # Duplicate check
  if (!is.null(key_cols)) {
    duplicates <- data %>%
      group_by(across(all_of(key_cols))) %>%
      filter(n() > 1) %>%
      nrow()
    report$duplicates <- duplicates
    if (duplicates > 0) {
      warning(paste("Duplicate keys found:", duplicates))
    }
  }

  # Outlier detection for numeric columns
  numeric_cols <- data %>% select(where(is.numeric)) %>% names()
  report$outliers <- list()
  for (col in numeric_cols) {
    values <- data[[col]]
    q1 <- quantile(values, 0.25, na.rm = TRUE)
    q3 <- quantile(values, 0.75, na.rm = TRUE)
    iqr <- q3 - q1
    outlier_count <- sum(values < (q1 - 3*iqr) | values > (q3 + 3*iqr), na.rm = TRUE)
    if (outlier_count > 0) {
      report$outliers[[col]] <- outlier_count
    }
  }

  return(report)
}
```

---

## Statistical Sanity Checks ("Smell Tests")

### The "Laugh Test" Protocol

Before finalizing any analysis, verify these common-sense checks:

| Check | Question | Example Failure |
|-------|----------|-----------------|
| **Magnitude** | Does this number make sense? | Trade value of $500 trillion (world GDP ~$100T) |
| **Sign** | Is the direction correct? | Tariff increase → imports increased |
| **Proportion** | Are percentages reasonable? | 150% of total imports |
| **Comparison** | How does this compare to known benchmarks? | China-US trade = $50B (actual ~$600B) |
| **Historical** | Does this align with historical patterns? | 2020 trade up 50% (COVID year) |

### Implementation

```r
#' Perform magnitude sanity check
#' @param value numeric value to check
#' @param label description of the value
#' @param expected_order_of_magnitude expected magnitude (e.g., 9 for billions)
#' @return TRUE if reasonable, FALSE with warning if not
check_magnitude <- function(value, label, expected_order_of_magnitude) {
  actual_magnitude <- floor(log10(abs(value)))
  difference <- abs(actual_magnitude - expected_order_of_magnitude)

  if (difference > 2) {
    warning(paste0(
      "MAGNITUDE CHECK FAILED: ", label, "\n",
      "  Value: ", format(value, scientific = TRUE, digits = 3), "\n",
      "  Expected order: 10^", expected_order_of_magnitude, "\n",
      "  Actual order: 10^", actual_magnitude
    ))
    return(FALSE)
  }
  return(TRUE)
}

#' Check percentage bounds
#' @param value percentage to check
#' @param label description
#' @return TRUE if valid (0-100 or documented exception)
check_percentage <- function(value, label) {
  if (any(value < 0 | value > 100, na.rm = TRUE)) {
    warning(paste0(
      "PERCENTAGE CHECK FAILED: ", label, "\n",
      "  Values outside 0-100% range detected\n",
      "  Range: ", min(value, na.rm = TRUE), " to ", max(value, na.rm = TRUE)
    ))
    return(FALSE)
  }
  return(TRUE)
}

#' Check for sign consistency (direction)
#' @param cause factor that should affect outcome
#' @param effect observed outcome
#' @param expected_direction "positive" or "negative" relationship
check_direction <- function(cause, effect, expected_direction) {
  correlation <- cor(cause, effect, use = "complete.obs")

  if (expected_direction == "positive" && correlation < 0) {
    warning("DIRECTION CHECK: Expected positive relationship but correlation is negative")
    return(FALSE)
  }
  if (expected_direction == "negative" && correlation > 0) {
    warning("DIRECTION CHECK: Expected negative relationship but correlation is positive")
    return(FALSE)
  }
  return(TRUE)
}
```

---

## Data Transformation Rules

### Unit Normalization

```r
#' Normalize values to standard units
#' @param value raw value
#' @param from_unit source unit
#' @param to_unit target unit
normalize_units <- function(value, from_unit, to_unit) {
  # Define conversion factors
  conversions <- list(
    # Weight
    "kg_to_tonnes" = 0.001,
    "lb_to_kg" = 0.453592,
    "tonnes_to_kg" = 1000,

    # Currency (requires exchange rate)
    "eur_to_usd" = 1.10,  # Update as needed
    "gbp_to_usd" = 1.27,

    # Trade value scales
    "millions_to_units" = 1e6,
    "billions_to_units" = 1e9,
    "units_to_millions" = 1e-6,
    "units_to_billions" = 1e-9
  )

  key <- paste(from_unit, "to", to_unit, sep = "_")
  if (key %in% names(conversions)) {
    return(value * conversions[[key]])
  } else {
    stop(paste("Unknown conversion:", key))
  }
}
```

### Date Handling

```r
#' Standardize date formats
#' @param date_string raw date string
#' @param formats vector of possible formats to try
#' @return Date object
parse_date_flexible <- function(date_string,
                                 formats = c("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y",
                                            "%Y/%m/%d", "%d-%m-%Y", "%B %d, %Y")) {
  for (fmt in formats) {
    parsed <- suppressWarnings(as.Date(date_string, format = fmt))
    if (!is.na(parsed)) {
      return(parsed)
    }
  }
  warning(paste("Could not parse date:", date_string))
  return(NA)
}

# Always use ISO 8601 for output
format_date_iso <- function(date) {
  format(date, "%Y-%m-%d")
}
```

### Text Cleaning

```r
#' Clean text for matching
#' @param text raw text
#' @return cleaned text
clean_text_for_matching <- function(text) {
  text %>%
    str_to_lower() %>%
    str_trim() %>%
    str_replace_all("[[:punct:]]", " ") %>%
    str_replace_all("\\s+", " ") %>%
    str_trim()
}

#' Remove common corporate suffixes
#' @param company_name raw company name
#' @return cleaned company name
remove_corporate_suffixes <- function(company_name) {
  suffixes <- c(
    "\\s+(inc|corp|ltd|llc|plc|gmbh|ag|sa|bv|nv|pty|co)\\s*\\.?$",
    "\\s+(incorporated|corporation|limited|company)$",
    "\\s+(the|a|an)$"
  )

  result <- str_to_lower(str_trim(company_name))
  for (suffix in suffixes) {
    result <- str_remove(result, regex(suffix, ignore_case = TRUE))
  }
  str_trim(result)
}
```

---

## Fuzzy Matching Protocol

### Tiered Matching Strategy

```r
#' Multi-tier entity matching
#' @param source_entities tibble with 'name' column
#' @param target_entities tibble with 'name' column
#' @param thresholds list of thresholds for each tier
#' @return matched entities with match quality indicators
match_entities_tiered <- function(source_entities,
                                   target_entities,
                                   thresholds = list(fuzzy = 0.85, token = 0.70)) {
  library(stringdist)

  # Prepare clean names
  source <- source_entities %>%
    mutate(
      name_clean = clean_text_for_matching(name),
      name_normalized = remove_corporate_suffixes(name_clean)
    )

  target <- target_entities %>%
    mutate(
      name_clean = clean_text_for_matching(name),
      name_normalized = remove_corporate_suffixes(name_clean)
    )

  results <- tibble()

  # Tier 1: Exact match on clean name
  tier1 <- source %>%
    inner_join(target, by = "name_clean", suffix = c("_source", "_target")) %>%
    mutate(match_tier = "exact", match_score = 1.0)
  results <- bind_rows(results, tier1)

  remaining <- source %>% anti_join(tier1, by = "name_clean")

  # Tier 2: Exact match on normalized name
  tier2 <- remaining %>%
    inner_join(target, by = "name_normalized", suffix = c("_source", "_target")) %>%
    mutate(match_tier = "normalized", match_score = 0.95)
  results <- bind_rows(results, tier2)

  remaining <- remaining %>% anti_join(tier2, by = "name_normalized")

  # Tier 3: Fuzzy match (Jaro-Winkler)
  if (nrow(remaining) > 0) {
    tier3 <- remaining %>%
      rowwise() %>%
      mutate(
        best_match_idx = which.max(
          stringsim(name_normalized, target$name_normalized, method = "jw")
        ),
        match_score = max(
          stringsim(name_normalized, target$name_normalized, method = "jw")
        )
      ) %>%
      filter(match_score >= thresholds$fuzzy) %>%
      mutate(
        name_target = target$name[best_match_idx],
        match_tier = "fuzzy"
      )
    results <- bind_rows(results, tier3 %>% select(-best_match_idx))

    remaining <- remaining %>% anti_join(tier3, by = "name_clean")
  }

  # Tier 4: Token containment (all source words appear in target)
  if (nrow(remaining) > 0) {
    tier4 <- remaining %>%
      rowwise() %>%
      mutate(
        source_tokens = list(str_split(name_normalized, "\\s+")[[1]]),
        best_match = find_token_match(source_tokens, target$name_normalized),
        match_score = best_match$score
      ) %>%
      filter(match_score >= thresholds$token) %>%
      mutate(
        name_target = best_match$name,
        match_tier = "token"
      )
    results <- bind_rows(results, tier4 %>% select(-source_tokens, -best_match))
  }

  return(results)
}

#' Tier 5: LLM-Augmented Matching
#' Escalate to LLM when Tiers 1-4 leave >20% of entities in grey zone (score 0.30-0.70)
#'
#' Decision rule: After Tiers 1-4, if remaining unmatched entities have best
#' traditional scores in the 0.30-0.70 range, these are too similar to reject
#' but too dissimilar to accept algorithmically. LLM adjudication resolves them.
#'
#' Pattern: pre-filter with traditional tiers to generate candidate shortlists,
#' then LLM adjudicates ambiguous cases using semantic understanding.
#'
#' Architecture:
#'   Pass 1: Traditional pre-filter (Tiers 1-4 above) → candidate shortlists
#'   Pass 2: LLM adjudication of grey-zone candidates (GPT-4o, temperature 0)
#'   Pass 3: False-negative sweep on unmatched entities (Gemini Flash)
#'
#' Full protocol: .claude/protocols/llm-pipeline-standards.md
#' Skill: .claude/skills/entity-matching/SKILL.md

#' Find best token-based match
find_token_match <- function(source_tokens, target_names) {
  best_score <- 0
  best_name <- NA

  for (target in target_names) {
    target_tokens <- str_split(target, "\\s+")[[1]]
    # Score = proportion of source tokens found in target
    matches <- sum(source_tokens %in% target_tokens)
    score <- matches / length(source_tokens)

    if (score > best_score) {
      best_score <- score
      best_name <- target
    }
  }

  list(score = best_score, name = best_name)
}
```

---

## Data Output Standards

### File Formats

| Format | Use Case | Encoding | Notes |
|--------|----------|----------|-------|
| **CSV** | Data exchange, import/export | UTF-8 | Include BOM for Excel compatibility |
| **Excel** | Final deliverables, formatted tables | - | Use openxlsx with styling |
| **Rdata** | Intermediate results, pipeline data | - | Preserves R types exactly |
| **PNG** | Charts for publication | - | 300 DPI minimum |

### CSV Export

```r
# Write CSV with UTF-8 BOM for Excel compatibility
write_csv_for_excel <- function(data, path) {
  # Write BOM
  con <- file(path, "wb")
  writeBin(charToRaw("\xef\xbb\xbf"), con)
  close(con)

  # Append CSV data
  write.table(
    data,
    file = path,
    append = TRUE,
    sep = ",",
    row.names = FALSE,
    col.names = TRUE,
    quote = TRUE,
    fileEncoding = "UTF-8"
  )
}
```

### Rdata Naming Convention

```r
# Save with descriptive object names
trade_data_2024 <- process_trade_data(raw_data)
save(trade_data_2024, file = "data/trade_data_2024.Rdata")

# Load explicitly to avoid namespace pollution
env <- new.env()
load("data/trade_data_2024.Rdata", envir = env)
data <- env$trade_data_2024
```

---

## Reproducibility Requirements

### Random Seed

```r
# Always set seed for reproducible sampling/modeling
set.seed(42)

# Document seed in script header
# Note: Random seed 42 used for reproducibility
```

### Session Info

```r
# Log session info at end of analysis
sessionInfo() %>%
  capture.output() %>%
  writeLines("results/session_info.txt")
```

### Data Provenance

Every output should document:
1. **Source data** - Where raw data came from
2. **Processing steps** - What transformations were applied
3. **Date processed** - When the analysis was run
4. **Analyst** - Who performed the analysis

```r
# Add provenance metadata to output
provenance <- list(
  source = "GTA database (gta_intervention table)",
  query_date = Sys.Date(),
  analyst = Sys.getenv("USER"),
  processing = "Filtered to 2020+, normalized units to USD billions",
  git_commit = system("git rev-parse HEAD", intern = TRUE)
)

# Save provenance with data
save(results, provenance, file = "results/analysis_results.Rdata")
```

---

## Quality Gate Checklist

Before marking any analysis as complete, verify:

### Data Validation
- [ ] Row counts match expectations (±10%)
- [ ] No unexpected missing values (>20% in key columns)
- [ ] No duplicate keys
- [ ] Date ranges are correct

### Statistical Sanity
- [ ] Magnitudes are plausible (billions not trillions)
- [ ] Signs are correct (direction matches expectation)
- [ ] Distributions are reasonable (no unexpected skewness)
- [ ] No unexplained outliers

### Output Verification
- [ ] Excel files open correctly with formatting
- [ ] Charts are readable (labels, legend, units)
- [ ] CSV exports have correct encoding (UTF-8)
- [ ] All source data documented

### Reproducibility
- [ ] Random seeds set where applicable
- [ ] Session info logged
- [ ] Data provenance documented
- [ ] Processing steps traceable
