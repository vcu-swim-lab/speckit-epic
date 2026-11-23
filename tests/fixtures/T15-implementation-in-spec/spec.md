# Feature Specification: Profile Photo Upload

**Feature Branch**: `015-profile-photo`
**Status**: Draft

## User Scenarios & Testing

### User Story 1 - Set a profile photo (Priority: P1)

A user uploads a photo from their device, and it appears as their profile picture.

**Acceptance Scenarios**:

1. **Given** a signed-in user with a 2 MB JPEG file, **When** they upload it on the profile page, **Then** it appears as their profile photo.
2. **Given** a signed-in user with a 7 MB PNG file, **When** they try to upload it, **Then** they see "Photos must be 5 MB or smaller." and their profile photo does not change.

## Requirements

### Functional Requirements

- **FR-001**: Users MUST be able to upload a profile photo from the profile page.
- **FR-002**: System MUST store uploaded photos in an AWS S3 bucket named `profile-photos`.
- **FR-003**: System MUST resize each photo to 256 by 256 pixels using the Sharp image library.
- **FR-004**: System MUST accept JPEG and PNG files up to 5 MB.
- **FR-005**: The upload endpoint MUST be implemented by Ali by Friday, November 28.

## Success Criteria

- **SC-001**: 95% of valid uploads show the new photo on the profile page within 5 seconds.

## Assumptions

- Users are already signed in when they open the profile page.
