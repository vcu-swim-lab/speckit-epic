# Feature Specification: User Sign-In

**Feature Branch**: `001-user-sign-in`
**Status**: Draft

## User Scenarios & Testing

### User Story 1 - Sign in (Priority: P1)

A registered user signs in with their email and password to reach their dashboard.

**Acceptance Scenarios**:

1. **Given** a registered user with a correct password, **When** they submit the sign-in form, **Then** they are taken to their dashboard.
2. **Given** a registered user with a wrong password, **When** they submit the sign-in form, **Then** they see the message "Email or password is incorrect" and stay on the sign-in page.
3. **Given** an account that is locked, **When** the user submits the sign-in form with the correct password, **Then** they see the message "This account is temporarily locked" and stay on the sign-in page.

## Requirements

### Functional Requirements

- **FR-001**: Users MUST be able to sign in quickly.
- **FR-002**: System MUST accept an email address and a password as sign-in credentials.
- **FR-003**: System MUST show the message "Email or password is incorrect" when either credential is wrong, without saying which one.
- **FR-004**: After a few failed sign-in attempts in a row, System MUST lock the account for 15 minutes.
- **FR-005**: System MUST send the user an alert email soon after a sign-in from a new device.
- **FR-006**: The sign-in page MUST be user-friendly.
- **FR-007**: System MUST sign the user out after a reasonable period of inactivity.

## Success Criteria

- **SC-001**: 95% of sign-in attempts with correct credentials reach the dashboard without an error message.

## Assumptions

- Users already have accounts; registration is out of scope for this feature.
