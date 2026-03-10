# Refactoring Triage Report

**Generated:** 2026-03-09
**Scan Root:** c:\git\open-fi-portal

## Executive Summary

- **Total Files Scanned:** 22
- **Total Files with Smells:** 1
- **Total Smells:** 2

### Top Smell Types

- **exception_swallowing**: 2

## Top 30 Projects by Refactoring Value

### 1. pages

- **Refactoring Value Score:** 119.0
- **Category:** unknown
- **Layer:** N/A
- **Fan-in:** 0, **Fan-out:** 0
- **Has Tests:** ❌ No
- **Total Files:** 7, **Total Lines:** 1694
- **Complexity Score:** 49
- **Total Smells:** 2

**Top Smells:**

- exception_swallowing: 2

**Key Files:**

- `pages\markets.py` (complexity: 12, smells: 0)
- `pages\credit.py` (complexity: 9, smells: 0)
- `pages\macro.py` (complexity: 7, smells: 0)

### 2. components

- **Refactoring Value Score:** 19.0
- **Category:** unknown
- **Layer:** N/A
- **Fan-in:** 0, **Fan-out:** 0
- **Has Tests:** ❌ No
- **Total Files:** 2, **Total Lines:** 195
- **Complexity Score:** 7
- **Total Smells:** 0

**Top Smells:**


**Key Files:**

- `components\dataset_card.py` (complexity: 4, smells: 0)
- `components\navbar.py` (complexity: 3, smells: 0)

### 3. config

- **Refactoring Value Score:** 17.0
- **Category:** unknown
- **Layer:** N/A
- **Fan-in:** 0, **Fan-out:** 0
- **Has Tests:** ❌ No
- **Total Files:** 2, **Total Lines:** 124
- **Complexity Score:** 6
- **Total Smells:** 0

**Top Smells:**


**Key Files:**

- `config\settings.py` (complexity: 3, smells: 0)
- `config\theme.py` (complexity: 3, smells: 0)

### 4. _unknown

- **Refactoring Value Score:** 13.0
- **Category:** unknown
- **Layer:** N/A
- **Fan-in:** 0, **Fan-out:** 0
- **Has Tests:** ❌ No
- **Total Files:** 1, **Total Lines:** 72
- **Complexity Score:** 4
- **Total Smells:** 0

**Top Smells:**


**Key Files:**

- `app.py` (complexity: 4, smells: 0)

### 5. data

- **Refactoring Value Score:** 11.0
- **Category:** unknown
- **Layer:** N/A
- **Fan-in:** 0, **Fan-out:** 0
- **Has Tests:** ❌ No
- **Total Files:** 1, **Total Lines:** 163
- **Complexity Score:** 3
- **Total Smells:** 0

**Top Smells:**


**Key Files:**

- `data\fetcher.py` (complexity: 3, smells: 0)

### 6. scripts

- **Refactoring Value Score:** 11.0
- **Category:** unknown
- **Layer:** N/A
- **Fan-in:** 0, **Fan-out:** 0
- **Has Tests:** ❌ No
- **Total Files:** 1, **Total Lines:** 54
- **Complexity Score:** 3
- **Total Smells:** 0

**Top Smells:**


**Key Files:**

- `scripts\prefetch_yfinance.py` (complexity: 3, smells: 0)

## Claude Code Session Plan

### Tier 1: Critical Refactoring Targets (Immediate Focus)

#### pages

**Why:** Refactoring value: 119.0. 2 exception_swallowing. no test coverage.

**Suggested Prompt:**

> Review pages for refactoring. Focus on: exception swallowing. This project has no test coverage.

**Estimated Effort:** high

**Key Files:**

- pages\markets.py
- pages\credit.py
- pages\macro.py
- pages\mbs_em.py
- pages\risk.py

### Tier 2: High-Value Refactoring (Next Phase)


### Tier 3: Medium-Value Refactoring (Opportunistic)
