# Nombre del ejecutable
TARGET = test

# Archivos fuente
SRC = test.cpp

# Compilador
CXX = g++

# Flags de compilación
CXXFLAGS = -Wall -O2

# Librerías necesarias
LDFLAGS = -lm -lrt -pthread

# Regla principal
all: $(TARGET)

$(TARGET): $(SRC)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(SRC) $(LDFLAGS)

# Regla de limpieza
clean:
	rm -f $(TARGET)
