# Spring Boot source review checklist

Use this as an investigation guide. A checklist item is not itself a finding.

## API contracts and validation

- Trace request binding and validation, including nested DTOs and method-level constraints. Verify that constraints are actually invoked in this controller/framework version.
- Check nullability, numeric bounds, paging limits, enum handling, and invalid input responses against the API contract. Check downstream guards before claiming input is unchecked.
- Verify that missing resources and business conflicts produce intended statuses without leaking internal details.
- Flag entity exposure only when it reveals sensitive fields, permits unintended writes, causes demonstrated serialization trouble, or breaks a stated contract. Do not insist every entity requires a DTO.

## Authorization and sensitive data

- Trace URL rules, method security enablement, principal-to-resource ownership, and repository tenant filters. Authentication alone does not enforce object ownership. Conversely, lack of `@PreAuthorize` is not a defect if authorization is enforced elsewhere.
- Check mass assignment and trust in client-supplied owner IDs or privileged fields against actual bindings and service guards.
- Evaluate CSRF from the credential transport and browser threat model. Stateless sessions alone do not establish safety. Cookie/session or other automatically attached credentials need analysis; an explicit bearer-header-only API should not be flagged just for disabling CSRF.
- Treat CORS separately from authorization. Determine whether the configured origin/credential policy exposes sensitive responses before assigning severity.
- Identify source-level sensitive logging or secret exposure with redacted evidence. A placeholder or test-only dummy secret is not a production credential.
- Examine actuator exposure and the applicable security chain/configuration, rather than assuming a property alone makes an endpoint public.

## Transactions and consistency

- Trace the caller and transaction boundary, including proxy mode, visibility, self-invocation, propagation, and exception handling. A self-call bypasses proxy advice; do not claim there is no transaction if an outer transaction already covers it or AspectJ weaving is configured.
- Check rollback rules for checked exceptions and customized defaults, caught exceptions, and independent repository transactions before claiming a multi-step operation is atomic.
- For concurrent mutations, identify the actual race and business invariant. Look for atomic updates, conditional writes, database constraints, or locks before recommending them.
- For retries of state-changing operations, determine whether repeated effects can occur and how the API handles duplicates. Do not require an idempotency key for every endpoint.
- Database transactions do not atomically cover remote calls. Identify a real partial-failure path before suggesting an outbox or compensating action.

## JPA and database access

- Look for unbounded reads in reachable request paths and check actual data-size bounds and response requirements. Do not assume every `findAll` is inappropriate.
- Trace association traversal and fetch strategy before calling something N+1. If generated SQL/query counts are unavailable, describe the risk and request a query-count test rather than inventing observed queries.
- Check whether pagination over collection fetches can produce wrong results or in-memory pagination for the actual provider/version.
- Check SQL parameter binding. Distinguish constant query construction from untrusted values interpolated into executable SQL.
- Inspect migrations and constraints. Do not declare a missing index solely from an entity annotation. Request query plans/cardinality when an index recommendation lacks evidence.
- Check pool sizing/timeouts against known workload and database limits. Never prescribe arbitrary pool sizes or “add an index” as a measured fix.

## Errors and basic operations

- Trace swallowed exceptions, success responses after failure, and exception messages returned to clients.
- Inspect remote-call timeouts and retry limits only when that integration is in scope; check shared client configuration first.
- Check logs for useful diagnostic context without secret or personal-data exposure.
- Match tests to the defect: negative validation cases, unauthorized access, partial failure rollback, bounded query counts, or concurrent invariant preservation.

## References

Consult documentation for the project's detected version; these are entry points, not claims about every version.

- [Spring transaction annotations](https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative/annotations.html)
- [Spring MVC validation](https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-controller/ann-validation.html)
- [Spring Security CSRF](https://docs.spring.io/spring-security/reference/servlet/exploits/csrf.html)
- [Spring Data JPA query methods](https://docs.spring.io/spring-data/jpa/reference/jpa/query-methods.html)
