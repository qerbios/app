# Stage 1: build
FROM golang:1.22-alpine AS build

WORKDIR /src

# Скопируем go.mod/go.sum из cmd/server
COPY cmd/server/go.mod cmd/server/go.sum ./

RUN go mod download

# Копируем весь исходник
COPY cmd/server/ .

RUN go build -o app main.go

# Stage 2: minimal runtime
FROM gcr.io/distroless/base-debian12:nonroot

WORKDIR /app
COPY --from=build /src/app .

USER nonroot:nonroot
CMD ["./app"]
