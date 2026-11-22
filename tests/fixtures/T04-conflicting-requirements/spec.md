# Feature Specification: Account Deletion

**Feature Branch**: `004-account-deletion`
**Status**: Draft

## User Scenarios & Testing

### User Story 1 - Delete my account (Priority: P1)

A signed-in user deletes their account from the settings page.

**Acceptance Scenarios**:

1. **Given** a signed-in user on the settings page, **When** they press "Delete account" and confirm, **Then** they are signed out and see "Your account has been deleted."
2. **Given** a user whose account was deleted, **When** they try to sign in with their old credentials, **Then** they see "Email or password is incorrect."

## Requirements

### Functional Requirements

- **FR-001**: System MUST ask the user to confirm before deleting the account.
- **FR-002**: System MUST permanently erase all of the user's personal data immediately when the account is deleted.
- **FR-003**: System MUST keep a deleted user's personal data for 30 days so the account can be restored if the user changes their mind.
- **FR-004**: System MUST sign the user out of all devices when the account is deleted.

## Success Criteria

- **SC-001**: 100% of confirmed deletions sign the user out of all devices within 1 minute.

## Assumptions

- Only the account owner can delete their own account.
