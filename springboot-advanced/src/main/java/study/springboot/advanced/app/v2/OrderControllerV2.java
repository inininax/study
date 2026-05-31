package study.springboot.advanced.app.v2;

import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import study.springboot.advanced.trace.TraceStatus;
import study.springboot.advanced.trace.hellotrace.HelloTraceV2;

@RestController
@RequiredArgsConstructor
public class OrderControllerV2 {
    private final OrderServiceV2 orderService;
    private final HelloTraceV2 trace;

    @GetMapping("/v2/request")
    public String request(String itemId) {
        TraceStatus status = trace.begin("OrderController.request()");

        try {
            orderService.orderItem(status.getTraceId(), itemId);
            trace.end(status);
            return "ok";

        } catch (Exception e) {
            trace.exception(status, e);
            throw e;
        }
    }
}
