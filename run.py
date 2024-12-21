import asyncio
from flask import Flask
from MarketDataSimulator.Controller.MarketDataSimulatorController import market_data_simulator_app
from DataConsumer.Controller.DataConsumerController import data_consumer_app
from DataReader.Controller.DataReaderController import data_reader_app

app = Flask(__name__)

running_services = {
    'market_data_simulator': False,
    'data_consumer': False,
    'data_reader': False
}

async def start_service(service, port):
    running_services[service] = True
    await asyncio.to_thread(globals()[f"{service}_app"].run, port=port)

@app.route('/start', methods=['POST'])
async def start_services():
    if all(running_services.values()):
        return "All microservices are already running", 400

    await asyncio.gather(
        start_service('market_data_simulator', 9000),
        start_service('data_consumer', 8000),
        start_service('data_reader', 8080)
    )
    return "All microservices started", 200

@app.route('/stop', methods=['POST'])
async def stop_services():
    for service in running_services:
        running_services[service] = False

    await asyncio.gather(
        asyncio.to_thread(market_data_simulator_app.shutdown),
        asyncio.to_thread(data_consumer_app.shutdown),
        asyncio.to_thread(data_reader_app.shutdown)
    )
    return "All microservices stopped", 200

if __name__ == '__main__':
    app.run(port=5000)