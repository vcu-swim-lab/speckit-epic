# Feature Specification: Shared Shopping List

**Feature Branch**: `013-shared-shopping-list`
**Status**: Draft

## User Scenarios & Testing

### User Story 1 - Add items to a shared list (Priority: P1)

A household member adds an item to the family shopping list, and the other members see it.

**Acceptance Scenarios**:

1. **Given** a shared list with two members, **When** one member adds "Milk", **Then** the other member sees "Milk" on the list after refreshing.
2. **Given** an item on the list, **When** a member marks it as bought, **Then** it moves to the "Bought" section for every member.

## Requirements

### Functional Requirements

- **FR-001**: Users MUST be able to create a shopping list and give it a name of 1 to 40 characters.
- **FR-002**: The list owner MUST be able to invite other users to the list by email address.
- **FR-003**: Any member MUST be able to add an item with a name of 1 to 60 characters.
- **FR-003**: Any member MUST be able to mark an item as bought.
- **REQ-5**: Any member MUST be able to delete an item.
- **FR-006a**: The list owner MUST be able to remove a member from the list.
- **FR-006b**: A removed member MUST no longer see the list.

## Goals

- Members see each other's changes after refreshing the list.
