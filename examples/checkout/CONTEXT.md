# Checkout source-review excerpt

This synthetic example is a source-review fixture, not a runnable application.
Assume Java 21, Spring Boot 3.3, Spring MVC, Hibernate/JPA, and ordinary proxy-based transaction management (no AspectJ).

`CheckoutController` is the only caller of `CheckoutService.checkout`. There is no surrounding transaction. Each repository is a standard Spring Data JPA repository. No custom advice, cross-cutting authorization, or exception handlers exist. Repository save calls each use their own default transaction when no outer transaction exists. An inventory save may throw a runtime persistence exception. An order must never be persisted unless its matching inventory reservation succeeds.

A separate security configuration authenticates requests. Ownership/payment processing and retries are outside this small example's scope. Do not infer a vulnerability from their omission. The amount must be strictly positive by contract, with no minimum currency-unit requirement. The bean-validation provider is present. No additional validation exists in services, entities, or database constraints for the amount.

Review only the transaction and input-validation paths. Do not execute this example.
