package example.checkout;

import java.math.BigDecimal;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
class CheckoutService {
    private final OrderRepository orders;
    private final InventoryRepository inventory;

    CheckoutService(OrderRepository orders, InventoryRepository inventory) {
        this.orders = orders;
        this.inventory = inventory;
    }

    public void checkout(BigDecimal amount) {
        reserveAndSave(amount);
    }

    @Transactional
    public void reserveAndSave(BigDecimal amount) {
        orders.save(new Order(amount));
        inventory.save(new InventoryReservation(amount));
    }
}
