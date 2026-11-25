# Feature Specification: Dark Mode Setting

**Feature Branch**: `017-dark-mode-setting`
**Status**: Draft

## User Scenarios & Testing

### User Story 1 - Switch to dark mode (Priority: P1)

A signed-in user turns on dark mode in their settings, and the app uses dark colors on every device where they are signed in.

**Independent Test**: Sign in on two devices, turn on dark mode on one, reload the other, and confirm both show dark colors.

**Acceptance Scenarios**:

1. **Given** a signed-in user with the theme set to Light, **When** they select Dark on the settings page, **Then** the current page switches to dark colors without reloading.
2. **Given** a user who selected Dark on one device, **When** they open the app on a second device where they are signed in, **Then** the app shows dark colors.
3. **Given** a user who has never changed the theme, **When** they open the app, **Then** the app shows light colors.

### Edge Cases

- The user is signed out: the app shows light colors, because the theme is stored with the account and no account is known.

## Requirements

### Functional Requirements

- **FR-001**: The settings page MUST offer a theme choice with exactly two options: Light and Dark.
- **FR-002**: Selecting a theme MUST apply it to the current page without a page reload.
- **FR-003**: System MUST save the selected theme to the user's account.
- **FR-004**: When a signed-in user opens the app, System MUST show the theme saved to their account.
- **FR-005**: A user who has never selected a theme MUST see the Light theme.

### Key Entities

- **Theme**: a setting stored with the user's account, with the value `Light` or `Dark`. The default is `Light`.

## Success Criteria

- **SC-001**: In 100% of tests, selecting Dark on one device and then opening the app on a second signed-in device shows dark colors on the second device.
- **SC-002**: The theme change on the current page completes within 1 second of the selection, for 95% of selections.

## Assumptions

- Users can already sign in on more than one device with the same account.

## Out of Scope

- An automatic theme that follows the device setting. Reason: deferred to a later feature; this feature only stores an explicit choice.
- Custom colors. Reason: permanently out of scope; the product offers only the two built-in themes.
