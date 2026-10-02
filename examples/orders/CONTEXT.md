# Orders source-review excerpt

This synthetic example is a source-review fixture, not a runnable application.
Assume Java 21, Spring Boot 3.3, Spring MVC and Spring Security 6.3. Spring Data JPA implements the repository interface. The Order entity has scalar id, owner and status fields only, with non-null owner and status; it contains no lazy associations. The DTO uses those scalars only.

The JWT decoder validates signature, expiry, issuer and the configured API audience. Credentials are accepted only through an explicit Authorization bearer header, with no cookies, HTTP Basic, form login, or server sessions. The JWT subject is the trusted owner identifier. Default MVC handling returns 400 for an invalid numeric path parameter, and the service returns 404 for absent or differently owned records. No other filter chains exist.

Review only object authorization, CSRF assumptions, and the single-object read/DTO mapping path. Do not execute this example.
