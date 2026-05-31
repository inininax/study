package com.example.reactive.config

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
class MongoConfig : AbstractReactiveMongoConfiguration() {

    override fun getDatabaseName(): String = "reactive_db"

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