# Sample review: checkout

This edited sample records findings from a fresh Codex review agent using the skill on the synthetic checkout fixture. It is not a runtime test result.

## Scope and limits

Inspected `examples/checkout/CONTEXT.md`, `CheckoutController.java`, and `CheckoutService.java`. Scenario facts specify Java 21, Spring Boot 3.3, Spring MVC, JPA, and proxy-based transaction management. Repository/entity implementations and build files are omitted. Findings rely on the explicit fixture facts. Only transactions and request validation were in scope.

## Findings

### C1 · High · High confidence — Inventory failure leaves a committed order

**Evidence:** `examples/checkout/CheckoutService.java:17–24`. The unannotated `checkout()` calls its own `reserveAndSave()`, bypassing proxy transaction advice. The order save occurs first. `CONTEXT.md:6` establishes that no outer transaction exists and each repository save commits independently.

**Trigger and impact:** The order save succeeds, then the inventory save throws. An order remains committed without its required reservation.

**Minimal fix:** Move the transaction boundary to the externally invoked `checkout()` method. Remove the redundant inner annotation unless that method has a separate supported external use.

**Verification — not run:** Invoke through the controller with no enclosing test transaction, force inventory persistence to fail, and check in a new transaction that no order was committed.

### C2 · Medium · High confidence — Amount constraints are never activated

**Evidence:** `examples/checkout/CheckoutController.java:17–19` uses `@RequestBody` without `@Valid`. Constraints exist on the record at lines 24–25. `CONTEXT.md:8` excludes downstream validation.

**Trigger and impact:** Null, zero and negative amounts can reach persistence, violating the strictly positive amount contract.

**Minimal fix:** Import `jakarta.validation.Valid` and use `@Valid @RequestBody CheckoutRequest request`.

**Verification — not run:** MVC tests should reject null, zero and negative amounts with HTTP 400 and no service invocation. A positive fractional amount such as `0.001` should pass validation.

## Validation performed

Static source and context inspection only. No application execution, database queries, compilation, or application tests. These are synthetic excerpts, not a buildable project.

## Separate orders case

The same review agent inspected the orders fixture as a separate scope and reported **No actionable findings in the inspected scope**. It traced ownership through the JWT subject and `findByIdAndOwner`, accepted the explicitly stated bearer-header-only CSRF model, and did not invent an N+1 issue for scalar DTO mapping.
