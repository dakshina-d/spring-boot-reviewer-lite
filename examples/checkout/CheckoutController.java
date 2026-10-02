package example.checkout;

import java.math.BigDecimal;
import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.NotNull;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/checkout")
class CheckoutController {
    private final CheckoutService service;

    CheckoutController(CheckoutService service) {
        this.service = service;
    }

    @PostMapping
    String checkout(@RequestBody CheckoutRequest request) {
        service.checkout(request.amount());
        return "accepted";
    }
}

record CheckoutRequest(
        @NotNull @DecimalMin(value = "0", inclusive = false) BigDecimal amount) {}
