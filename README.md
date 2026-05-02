# Sistema de Monitoramento de Terremotos (Kafka + gRPC)



projeto de monitoração de terremotos em 4 nós com arquitetura Produtor → Consumidor/Produtor → Consumidor/Web Service ↔ Cliente e usando gRPC + Apache Kafka.

Essencial executar em múltiplas instâncias/contâineres.

**Instância 1 (Servidor/Broker):**
* Broker Apache Kafka
* **Node 2 (Processador):** `processor.py`
* **Node 3 (Servidor gRPC):** `server.py`

**Instância 2 (Borda/Sensor):**
* **Node 1 (Sensor):** `sensor.py`
* **Node 4 (Cliente):** `client.py`

---

##  Instalação 

Execute estes passos em **ambas** as instâncias:

1. **Instale as dependências:**
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv -y
   python3 -m venv venv
   source venv/bin/activate
   pip install kafka-python grpcio grpcio-tools
   ```

2. **Transfira os arquivos shared:** 
    earthquake.proto e const.py são parte das DUAS instâncias
3. **Compile o arquivo Protobuf (gRPC):**
   Com o arquivo `earthquake.proto` na pasta, rode:
   ```bash
   python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. earthquake.proto
   ```
4. **Configuração de IP:**
Dentro de const.py:
   ```bash
    BROKER_ADDR = 'IP_DA_INSTANCIA_1'
    BROKER_PORT = '9092'  
    ```
Até na instância 2, o IP aqui é o IP da instância 1.

5. **Configuração do Kafka**: Na instância 1 apenas
#### Basic configuration of Kafka (for remote access to the broker)
```
cd kafka_2.13-4.2.0/
```

**Enable remote access to the broker:** Edit the file **config/server.properties** (in the kafka directory) in order to change the line starting with **advertised_listeners**, replacing (only) the first occurrence of **localhost** with the **IP address** of the machine where the Broker will run (server01). It is recommended to use a fixed public IP address for this machine. That line should look like this:

advertised.listeners=PLAINTEXT://32.195.37.234:9092,CONTROLLER://localhost:9093

#### Then create the metadata files with the configuration
```
KAFKA_CLUSTER_ID="$(bin/kafka-storage.sh random-uuid)"
```
```
bin/kafka-storage.sh format --standalone -t $KAFKA_CLUSTER_ID -c config/server.properties
```
##  Execução


 Em **TODOS** os terminais listados com **EXCEÇÃO** do que roda o broker Kafka, a primeira coisa a fazer é ativar o ambiente virtual do Python onde as dependências foram instaladas:
> ```bash
> source venv/bin/activate
> ```

---

### MÁQUINA 1: Instância do Servidor

**Terminal 1 (O Broker Kafka):**
Navegue até a pasta do Kafka (ex: `cd kafka_2.13-4.2.0/`) e inicie o servidor. Deixe este terminal aberto (ele ficará mostrando os logs).
```bash
bin/kafka-server-start.sh config/server.properties
```

**Terminal 2**:
```bash
python3 processor.py
```
**Terminal 3**:
```bash
python3 server.py
```
### MÁQUINA 2: Instância do Cliente

**Terminal 4**: Mostra os terremotos relevantes
```bash
python3 sensor.py
```
**Terminal 5**: mostra o ÚLTIMO terremoto. usar sob demanda.

```bash
python3 client.py
```
