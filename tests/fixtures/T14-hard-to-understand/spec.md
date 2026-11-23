# Feature Specification: Expense Report Approval

**Feature Branch**: `014-expense-approval`
**Status**: Draft

## User Scenarios & Testing

### User Story 1 - Submit an expense for approval (Priority: P1)

An employee submits an expense with a receipt photo, and it is routed for approval.

**Acceptance Scenarios**:

1. **Given** an employee with a $40 taxi receipt, **When** they submit it, **Then** it goes to their manager for approval.
2. **Given** a submitted expense, **When** the manager approves it, **Then** its status changes to S3.

## Requirements

### Functional Requirements

- **FR-001**: Employees MUST be able to submit an expense with an amount, a date, a category and a receipt photo.
- **FR-002**: Expenses above the AL MUST be routed to L2 instead of the employee's manager.
- **FR-003**: System MUST reject a receipt photo taken more than 90 days before the expense is submitted.
- **FR-004**: An approved expense MUST move from S2 to S3.
- **FR-005**: Managers MUST NOT be able to approve their own expenses, so that nobody can approve money paid to themselves.

## Success Criteria

- **SC-001**: 95% of expenses under $100 are approved or rejected within 2 business days of submission.

## Assumptions

- Each employee has exactly one manager in the company directory.
