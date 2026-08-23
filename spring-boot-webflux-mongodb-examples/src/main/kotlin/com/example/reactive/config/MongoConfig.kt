package com.example.reactive.config

import com.mongodb.reactivestreams.client.MongoClient
import com.mongodb.reactivestreams.client.MongoClients
import org.springframework.boot.autoconfigure.mongo.MongoProperties
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration
import org.springframework.data.mongodb.config.AbstractReactiveMongoConfiguration
import org.springframework.data.mongodb.config.EnableReactiveMongoAuditing
import org.springframework.data.mongodb.core.convert.MongoCustomConversions
import org.springframework.data.mongodb.repository.config.EnableReactiveMongoRepositories
import java.time.LocalDateTime
import java.time.ZoneOffset
import java.util.*
import org.springframework.core.convert.converter.Converter
import java.time.ZonedDateTime

@Configuration
@EnableReactiveMongoRepositories(basePackages = ["com.example.reactive.repository"])
@EnableReactiveMongoAuditing
class MongoConfig(
    private val mongoProperties: MongoProperties,
) : AbstractReactiveMongoConfiguration() {

    // spring.data.mongodb.database (또는 uri) 설정을 따르도록 함 — 기본값 reactive_db
    override fun getDatabaseName(): String = mongoProperties.mongoClientDatabase

    // 부모 기본 구현은 어떤 호스트/포트/uri 설정도 적용하지 않은 채 드라이버 기본값(127.0.0.1:27017)으로
    // 클라이언트를 생성하므로, spring.data.mongodb.* 설정을 실제로 반영하도록 오버라이드한다.
    override fun reactiveMongoClient(): MongoClient {
        val uri = mongoProperties.uri
            ?: "mongodb://${mongoProperties.host}:${mongoProperties.port}"
        return MongoClients.create(uri)
    }

    @Bean
    override fun customConversions(): MongoCustomConversions {
        val converters = listOf(
            LocalDateTimeToDateConverter(),
            DateToLocalDateTimeConverter()
        )
        return MongoCustomConversions(converters)
    }

    class LocalDateTimeToDateConverter : Converter<LocalDateTime, Date> {
        override fun convert(source: LocalDateTime): Date {
            return Date.from(source.atZone(ZoneOffset.UTC).toInstant())
        }
    }

    class DateToLocalDateTimeConverter : Converter<Date, LocalDateTime> {
        override fun convert(source: Date): LocalDateTime {
            return LocalDateTime.ofInstant(source.toInstant(), ZoneOffset.UTC)
        }
    }
}