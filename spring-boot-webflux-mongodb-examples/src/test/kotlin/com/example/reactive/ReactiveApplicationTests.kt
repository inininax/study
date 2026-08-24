package com.example.reactive

import com.example.reactive.model.Product
import com.example.reactive.repository.ProductRepository
import org.junit.jupiter.api.Assertions.assertEquals
import org.junit.jupiter.api.Test
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.test.context.SpringBootTest
import org.springframework.test.context.ActiveProfiles
import org.springframework.test.context.DynamicPropertyRegistry
import org.springframework.test.context.DynamicPropertySource
import java.math.BigDecimal
import java.time.Duration

@SpringBootTest
@ActiveProfiles("test")
class ReactiveApplicationTests @Autowired constructor(
    private val productRepository: ProductRepository,
) {

    companion object {
        /**
         * CI 등 외부 MongoDB가 제공되면 그 접속 정보를 사용하고(임베디드 다운로드 생략),
         * 없으면 flapdoodle embedded mongod를 띄운다.
         * NOTE: uri와 host/port를 동시에 바인딩하면 Boot가 거부하므로 host/port로 분해한다.
         */
        private val externalUri: String? = System.getenv("MONGODB_TEST_URI")

        @JvmStatic
        @DynamicPropertySource
        fun mongodbProperties(registry: DynamicPropertyRegistry) {
            if (externalUri != null) {
                val uri = java.net.URI(externalUri.removePrefix("mongodb://"))
                registry.add("spring.data.mongodb.host") { uri.host }
                registry.add("spring.data.mongodb.port") { (if (uri.port > 0) uri.port else 27017).toString() }
                println("[MONGO-TEST] using external MongoDB at ${uri.host}:${uri.port}")
            } else {
                registry.add("spring.data.mongodb.host") { EmbeddedMongo.host }
                registry.add("spring.data.mongodb.port") { EmbeddedMongo.port.toString() }
            }
        }
    }

    @Test
    fun contextLoads() {
    }

    @Test
    fun productRoundTripThroughRealMongo() {
        val timeout = Duration.ofSeconds(30)
        val product = Product(
            name = "embedded-mongo-roundtrip",
            description = "proves the test suite talks to a real MongoDB",
            price = BigDecimal("19.99"),
            category = "verification",
            tags = listOf("test", "embedded"),
            inStock = true,
            stockQuantity = 1,
        )

        val saved = productRepository.save(product).block(timeout)!!
        val found = productRepository.findById(saved.id!!).block(timeout)!!

        assertEquals(saved.id, found.id)
        assertEquals("embedded-mongo-roundtrip", found.name)
        assertEquals(BigDecimal("19.99"), found.price)

        // NOTE: 이 println은 EmbeddedMongo.host 에 접근하지 않는다 — 접근 시 lazy 초기화가
        // 실행되어 외부 Mongo 사용 중(CI)에도 임베디드 다운로드를 유발한다.
        println("[MONGO-TEST-PROOF] round-trip OK -> id=${found.id} name=${found.name}")

        productRepository.deleteAll().block(timeout)
    }
}
