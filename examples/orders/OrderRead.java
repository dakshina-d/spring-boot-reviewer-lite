package example.orders;

import java.util.Optional;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.http.HttpStatus;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.oauth2.jwt.Jwt;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

@Configuration
class ApiSecurity {
    @Bean
    SecurityFilterChain api(HttpSecurity http) throws Exception {
        return http.csrf(csrf -> csrf.disable())
                .sessionManagement(s -> s.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
                .authorizeHttpRequests(a -> a.anyRequest().authenticated())
                .oauth2ResourceServer(o -> o.jwt(j -> {}))
                .build();
    }
}

@RestController
@RequestMapping("/orders")
class OrderController {
    private final OrderService service;
    OrderController(OrderService service) { this.service = service; }

    @GetMapping("/{id}")
    OrderView read(@PathVariable("id") long id, @AuthenticationPrincipal Jwt jwt) {
        return service.read(id, jwt.getSubject());
    }
}

@Service
class OrderService {
    private final OrderRepository orders;
    OrderService(OrderRepository orders) { this.orders = orders; }

    @Transactional(readOnly = true)
    public OrderView read(long id, String owner) {
        Order order = orders.findByIdAndOwner(id, owner)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND));
        return new OrderView(order.getId(), order.getStatus());
    }
}

interface OrderRepository extends JpaRepository<Order, Long> {
    Optional<Order> findByIdAndOwner(long id, String owner);
}

record OrderView(long id, String status) {}
