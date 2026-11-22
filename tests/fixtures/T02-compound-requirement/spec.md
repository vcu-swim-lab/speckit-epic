# Feature Specification: Contact Form

**Feature Branch**: `002-contact-form`
**Status**: Draft

## User Scenarios & Testing

### User Story 1 - Send a message (Priority: P1)

A visitor fills in their name, email address and message, and sends it to the support team.

**Acceptance Scenarios**:

1. **Given** all fields are filled in correctly, **When** the visitor presses Send, **Then** they see "Thanks, we got your message."
2. **Given** the email field is empty, **When** the visitor presses Send, **Then** the message is not sent and the email field shows "Email is required."

## Requirements

### Functional Requirements

- **FR-001**: The form MUST have three fields: name, email address and message.
- **FR-002**: System MUST validate that the email field is not empty and contains an "@" character, and MUST display an error message under the email field and keep the other fields' contents when validation fails.
- **FR-003**: System MUST deliver each sent message to the support inbox.

## Success Criteria

- **SC-001**: 100% of messages sent with valid fields arrive in the support inbox.

## Assumptions

- The support inbox already exists and is managed by the support team.
