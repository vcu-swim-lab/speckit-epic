# Feature Specification: Export Orders to CSV

**Feature Branch**: `016-export-orders-csv`
**Status**: Draft

## User Scenarios & Testing

### User Story 1 - Export orders (Priority: P1)

A store manager downloads the orders from a chosen date range as a CSV file to open in a spreadsheet.

**Acceptance Scenarios**:

1. **Given** 3 orders between March 1 and March 31, **When** the manager exports that range, **Then** they download a CSV file with a header row and 3 order rows.
2. **Given** no orders in the chosen range, **When** the manager exports it, **Then** they download a CSV file with only the header row.

## Requirements

### Functional Requirements

- **FR-001**: Managers MUST be able to choose a start date and an end date for the export.
- **FR-002**: The CSV file MUST contain one row per order placed between the start date and the end date, both included.
- **FR-003**: The CSV file MUST have these columns, in this order: order number, order date, customer email, total amount.
- **FR-004**: Only users with the manager role MUST be able to export orders.

## Success Criteria

- **SC-001**: An export of up to 10,000 orders finishes downloading within 30 seconds.

## Assumptions

- The order database already stores order number, order date, customer email and total amount.
