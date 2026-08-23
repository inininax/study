package com.example.reactive

import de.flapdoodle.embed.mongo.distribution.Version
import de.flapdoodle.embed.mongo.transitions.Mongod
import de.flapdoodle.embed.mongo.transitions.RunningMongodProcess
import de.flapdoodle.reverse.TransitionWalker
import org.slf4j.LoggerFactory

/**
 * Boots a real MongoDB (flapdoodle 4.x transitions API) once per JVM for tests.
 *
 * NOTE: Boot 3.2 removed EmbeddedMongoAutoConfiguration, and this project's main-source
 * MongoConfig extends AbstractReactiveMongoConfiguration, whose @Bean factory chain builds
 * its own client from spring.data.mongodb properties (an extra MongoClient bean would NOT
 * be routed into that chain). So tests wire the embedded instance in by pointing those
 * properties at it (see @DynamicPropertySource in the test classes).
 */
object EmbeddedMongo {

    private val log = LoggerFactory.getLogger(EmbeddedMongo::class.java)

    val mongod: TransitionWalker.ReachedState<RunningMongodProcess> by lazy {
        Mongod.instance()
            .start(Version.Main.PRODUCTION) // random free port resolved by Net.defaults()
            .also { running ->
                val address = running.current().serverAddress
                log.info("Embedded MongoDB {} listening on {}:{}", Version.Main.PRODUCTION, address.host, address.port)
                println("[EMBEDDED-MONGO] started ${Version.Main.PRODUCTION} on ${address.host}:${address.port}")
                Runtime.getRuntime().addShutdownHook(Thread {
                    runCatching { running.close() }
                })
            }
    }

    val port: Int
        get() = mongod.current().serverAddress.port

    val host: String
        get() = mongod.current().serverAddress.host
}
