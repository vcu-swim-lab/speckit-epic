# Feature Specification: Product Search

**Feature Branch**: `003-product-search`
**Status**: Draft

## User Scenarios & Testing

### User Story 1 - Search by name (Priority: P1)

A shopper types part of a product name into the search box and sees the matching products.

**Acceptance Scenarios**:

1. **Given** a product named "Blue Mug", **When** the shopper searches for "mug", **Then** "Blue Mug" appears in the results.
2. **Given** no product name contains "xyz", **When** the shopper searches for "xyz", **Then** the message "No products found" is shown.

### User Story 2 - Relevant results first (Priority: P2)

A shopper sees the most useful products at the top of the results.

## Requirements

### Functional Requirements

- **FR-001**: System MUST return products whose name contains the search text, ignoring letter case.
- **FR-002**: System MUST show the message "No products found" when nothing matches.
- **FR-003**: System MUST order search results so that the best results appear first.

## Success Criteria

- **SC-001**: Shoppers are satisfied with the search results.

## Assumptions

- The product catalog already exists and each product has a name.
