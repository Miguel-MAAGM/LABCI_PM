# Nombre del ejecutable
TARGET = spi_master

# Compilador y flags
CC = gcc
CFLAGS = -Wall -O2

# Archivos fuente
SRC = mcuToSpi.c

# Archivos objeto
OBJ = $(SRC:.c=.o)

# Ruta del ejecutable final
BIN = ./$(TARGET)

all: $(BIN)

$(BIN): $(OBJ)
	$(CC) $(CFLAGS) -o $@ $^

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJ) $(BIN)

.PHONY: all clean
