# Feature Specification: Newsletter Unsubscribe

**Feature Branch**: `007-newsletter-unsubscribe`
**Status**: Draft

## User Scenarios & Testing

### User Story 1 - Unsubscribe from the newsletter (Priority: P1)

A subscriber clicks the unsubscribe link at the bottom of a newsletter email and stops receiving the newsletter.

**Independent Test**: Send a newsletter to a test subscriber, click the link, and confirm the next newsletter is not sent to them.

**Acceptance Scenarios**:

1. **Given** a subscribed email address, **When** the subscriber opens the unsubscribe link from a newsletter, **Then** they see "You have been unsubscribed." and the address is marked as unsubscribed.
2. **Given** an address that is already unsubscribed, **When** the subscriber opens the same link again, **Then** they see "You have been unsubscribed." and nothing else changes.
3. **Given** an unsubscribe link whose token does not match any subscriber, **When** it is opened, **Then** the page shows "This link is not valid." and no address is changed.

### Edge Cases

- The subscriber opens the link on a different device from the one that received the email: the link still works, because it does not depend on a sign-in.

## Requirements

### Functional Requirements

- **FR-001**: Every newsletter email MUST contain an unsubscribe link unique to the recipient's address.
- **FR-002**: Opening a valid unsubscribe link MUST mark the recipient's address as unsubscribed without asking the subscriber to sign in.
- **FR-003**: System MUST NOT send newsletters to addresses marked as unsubscribed.
- **FR-004**: Opening the unsubscribe link for an address that is already unsubscribed MUST show the same confirmation message and change nothing.
- **FR-005**: Opening an unsubscribe link whose token matches no subscriber MUST show "This link is not valid." and change no address.

### Key Entities

- **Subscriber**: an email address with a status of either `subscribed` or `unsubscribed`.

## Success Criteria

- **SC-001**: 100% of addresses marked as unsubscribed receive no newsletter sent after the moment they were marked.
- **SC-002**: The unsubscribe confirmation page appears within 3 seconds of opening the link, for 95% of requests.

## Assumptions

- Newsletters are already sent by an existing mailing system that can skip addresses by status.

## Out of Scope

- Re-subscribing, and choosing between different newsletter topics.
