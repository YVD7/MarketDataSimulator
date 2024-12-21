from flask import Flask, request, jsonify
from MarketDataSimulator.Service.MarketDataSimulatorService import MarketDataSimulatorService

market_data_simulator_app = Flask(__name__)

@market_data_simulator_app.route("/MarketDataSimulator", methods=['POST'])
def market_data_simulator():
    data = request.get_json()
    # topic = "stock-market-data"
    if not data:
        return jsonify({"error": "No data provided"}), 400
    try:
        topic = "stock-market-data"
        mdss = MarketDataSimulatorService()
        mdss.kafka_producer(topic=topic, data=data)  # Send the data to the Kafka producer method
        return jsonify({"message": "Market data sent successfully"}), 200  # Return success response
    except Exception as e:
        return jsonify({"error": f"Failed to send data: {str(e)}"}), 500  # Return error if something goes wrong


# if __name__ == "__main__":
#     market_data_simulator_app.run(port=9000)





