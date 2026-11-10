# --- Stage 1: Build dell'applicazione ---
FROM maven:3.9.6-eclipse-temurin-21-alpine AS build
WORKDIR /app

# Copia il pom.xml e scarica le dipendenze (ottimizza la cache di Docker)
COPY pom.xml .
RUN mvn dependency:go-offline -B

# Copia il codice sorgente e compila il progetto
COPY src ./src
RUN mvn clean package -DskipTests

# --- Stage 2: Runtime leggero ---
FROM eclipse-temurin:21-jre-alpine
WORKDIR /app

# Crea un utente non-root per maggiore sicurezza
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

# Copia il file .jar generato nello stage precedente
COPY --from=build /app/target/*.jar app.jar

# Espone la porta standard dell'applicazione
EXPOSE 8080

# Comando di avvio
ENTRYPOINT ["java", "-jar", "app.jar"]