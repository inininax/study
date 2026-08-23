package com.example.reactive.config

import kotlinx.coroutines.CoroutineDispatcher
import kotlinx.coroutines.Dispatchers
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration

@Configuration
class CoroutineConfig {

    // Dispatchers.IO/Default 는 JVM 전역 싱글톤이라 컨테이너 종료 시 destroy 메서드를 호출하면 안 된다.
    // destroyMethod = "" 로 종료 훅을 비활성화한다.
    @Bean(destroyMethod = "")
    fun ioDispatcher(): CoroutineDispatcher = Dispatchers.IO

    @Bean(destroyMethod = "")
    fun defaultDispatcher(): CoroutineDispatcher = Dispatchers.Default
}
