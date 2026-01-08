FROM maven:3.9.9-eclipse-temurin-21 AS build
WORKDIR /workspace/app

COPY pom.xml .
COPY src src

RUN mvn -DskipTests package

FROM amazoncorretto:21
WORKDIR /app

ARG JAR_FILE=/workspace/app/target/*.jar
COPY --from=build ${JAR_FILE} /app/app.jar

EXPOSE 8000

ENTRYPOINT ["java","-XX:+ExitOnOutOfMemoryError","-jar", "/app/app.jar"]
