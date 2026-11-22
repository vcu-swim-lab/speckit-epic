# Feature Specification: Password Reset

**Feature Branch**: `006-password-reset`
**Status**: Draft

## User Scenarios & Testing

### User Story 1 - Reset a forgotten password (Priority: P1)

A user who forgot their password asks for a reset link by email and uses it to set a new password.

**Acceptance Scenarios**:

1. **Given** a registered email address, **When** the user requests a reset, **Then** a reset link is sent to that address.
2. **Given** a valid reset link, **When** the user opens it and enters a new password twice, **Then** the password is changed and they can sign in with it.
3. **Given** a reset link that was already used, **When** the user opens it again, **Then** they see "This link is no longer valid."

## Requirements

### Functional Requirements

- **FR-001**: System MUST send a password reset link to the email address on the account when a reset is requested.
- **FR-002**: System MUST accept each reset link only once.
- **FR-003**: System MUST let the user set a new password from a valid reset link.
- **FR-004**: System MUST reject expired reset links.

## Success Criteria

- **SC-001**: 95% of reset emails arrive within 2 minutes of the request.

## Assumptions

- An email sending service is already set up for the product.
