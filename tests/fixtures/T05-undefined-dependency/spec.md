# Feature Specification: Shipping Cost at Checkout

**Feature Branch**: `005-shipping-cost`
**Status**: Draft

## User Scenarios & Testing

### User Story 1 - See shipping cost (Priority: P1)

At checkout, a shopper enters their address and sees the shipping cost before paying.

**Acceptance Scenarios**:

1. **Given** a cart with items and a valid address, **When** the shopper reaches the payment step, **Then** the shipping cost is shown and added to the order total.

## Requirements

### Functional Requirements

- **FR-001**: System MUST ask for a shipping address before the payment step.
- **FR-002**: System MUST get the shipping cost from the shipping rate service using the cart weight and the destination address.
- **FR-003**: System MUST add the shipping cost to the order total shown on the payment step.

## Success Criteria

- **SC-001**: 99% of shoppers with a valid address see a shipping cost before the payment step.

## Assumptions

- Cart items already have a weight in kilograms.
