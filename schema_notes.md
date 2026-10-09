# Data model notes

## Daily log
One row per day. Keeps fast-entry metrics.

## M3 topic log
One row per chapter/topic session. This is the granular source for chapter-level analysis.

## Agentic topics
One row per topic. Current depth is 0–5.

## X-0 topics
One row per Phase 0 topic. Current depth is 0–5.

## Projects
A project can reference many topics. This avoids pretending that one project equals one learning unit.

## DADS operations
Tracks operational ownership stages rather than time spent.

## Configuration
Stores editable goals and assumptions so formulas do not hard-code targets across the workbook.
