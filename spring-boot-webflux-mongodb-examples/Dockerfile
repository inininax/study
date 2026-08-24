# ---------- Build stage ----------
FROM gradle:8.11-jdk21 AS build
WORKDIR /workspace

COPY build.gradle.kts ./
COPY src ./src

RUN gradle bootJar --no-daemon \
    && mv "$(find build/libs -name '*.jar' ! -name '*-plain.jar' | head -n 1)" /workspace/app.jar

# ---------- Runtime stage ----------
FROM eclipse-temurin:21-jre-alpine AS runtime

RUN addgroup -S spring && adduser -S spring -G spring

WORKDIR /app
COPY --from=build --chown=spring:spring /workspace/app.jar app.jar

USER spring
EXPOSE 8080

ENTRYPOINT ["java", "-jar", "app.jar"]
