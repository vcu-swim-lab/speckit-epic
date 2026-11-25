# Feature Specification: Checkout Payment

**Feature Branch**: `005-checkout-payment`
**Status**: Draft

## User Scenarios & Testing

### User Story 1 - Pay for an order (Priority: P1)

At checkout, a shopper enters their address, sees the shipping cost and tax, and pays.

**Acceptance Scenarios**:

1. **Given** a cart with items and a valid address, **When** the shopper reaches the payment step, **Then** the shipping cost and tax are shown and added to the order total.
2. **Given** a cart with items and a valid address, **When** the TaxCalc API does not respond within 10 seconds, **Then** checkout is blocked and the shopper sees "Tax can't be calculated right now. Please try again."

## Requirements

### Functional Requirements

- **FR-001**: System MUST ask for a shipping address before the payment step.
- **FR-002**: System MUST get the shipping cost from the shipping rate service using the cart weight and the destination address.
- **FR-003**: System MUST charge the order total using Stripe.
- **FR-004**: Shoppers MUST be able to pay with their saved card.
- **FR-005**: System MUST calculate sales tax using the TaxCalc API.
- **FR-006**: When the TaxCalc API does not respond within 10 seconds, System MUST block checkout and show "Tax can't be calculated right now. Please try again."

## Success Criteria

- **SC-001**: 99% of shoppers with a valid address see the shipping cost on the payment step.

## Assumptions

- Cart items already have a weight in kilograms.
- The TaxCalc API (version 2) is already contracted and reachable from the checkout service.
