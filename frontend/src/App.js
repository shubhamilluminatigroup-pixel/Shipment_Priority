import React, { useState } from "react";
import axios from "axios";

function App() {
  const [shipments, setShipments] = useState([]);
  const [loading, setLoading] = useState(false);
  const [recalculating, setRecalculating] = useState(false);
  const [weights, setWeights] = useState({
    value: 0,
    weight: 0,
    volume: 0.25,
    shelf_life_days: 0.5,
    days_to_delivery: 0.5,
  });

  const fetchShipments = () => {
    setLoading(true);
    axios
      .get("http://127.0.0.1:8000/shipments/")
      .then((response) => {
        setShipments(response.data);
      })
      .catch((error) => {
        console.error("Error fetching shipments:", error);
      })
      .finally(() => {
        setLoading(false);
      });
  };

  const recalculateScores = () => {
    setRecalculating(true);
    axios
      .post("http://localhost:8000/shipments/score/")
      .then(() => fetchShipments())
      .catch((error) => {
        console.error("Error recalculating scores:", error);
      })
      .finally(() => {
        setRecalculating(false);
      });
  };

  const updateWeights = () => {
    axios
      .post("http://localhost:8000/weights/fixed/", weights)
      .then(() => alert("Weights updated successfully!"))
      .catch((error) => {
        console.error("Error updating weights:", error);
      });
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setWeights((prev) => ({
      ...prev,
      [name]: parseFloat(value),
    }));
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-white p-6">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-extrabold text-gray-800 mb-6 text-center">
          📦 Shipment Dashboard
        </h1>

        {/* Weight Config Inputs */}
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-6">
          {["value", "weight", "volume", "shelf_life_days", "days_to_delivery"].map((field) => (
            <div key={field}>
              <label className="block text-sm font-semibold text-gray-700 mb-1 capitalize">
                {field.replace(/_/g, " ")}
              </label>
              <input
                type="number"
                step="0.01"
                min="0"
                max="1"
                name={field}
                value={weights[field]}
                onChange={handleInputChange}
                className="w-full border rounded px-3 py-2 focus:outline-none focus:ring focus:border-blue-300"
              />
            </div>
          ))}
        </div>

        <div className="flex justify-center space-x-4 mb-6">
          <button
            onClick={updateWeights}
            className="bg-yellow-500 hover:bg-yellow-600 text-white font-semibold px-6 py-2 rounded shadow"
          >
            Update Weights
          </button>
          <button
            onClick={fetchShipments}
            className="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-6 py-2 rounded shadow"
          >
            {loading ? "Loading..." : "Fetch Shipments"}
          </button>
          <button
            onClick={recalculateScores}
            className="bg-green-600 hover:bg-green-700 text-white font-semibold px-6 py-2 rounded shadow"
          >
            {recalculating ? "Recalculating..." : "Recalculate Scores"}
          </button>
        </div>

        <div className="overflow-x-auto shadow-lg rounded-xl border border-gray-200 bg-white">
          <table className="min-w-full text-sm text-gray-700">
            <thead className="bg-blue-100 text-gray-900">
              <tr>
                <th className="px-4 py-3 text-left">Shipment ID</th>
                <th className="px-4 py-3 text-left">Status</th>
                <th className="px-4 py-3 text-left">Priority Score</th>
                <th className="px-4 py-3 text-left">Created At</th>
                <th className="px-4 py-3 text-left">Updated At</th>
                <th className="px-4 py-3 text-left">Shelf Life</th>
                <th className="px-4 py-3 text-left">Volume</th>
                <th className="px-4 py-3 text-left">Weight</th>
                <th className="px-4 py-3 text-left">Value</th>
              </tr>
            </thead>
            <tbody>
              {shipments.length === 0 ? (
                <tr>
                  <td colSpan="9" className="text-center py-6 text-gray-500">
                    No shipments available.
                  </td>
                </tr>
              ) : (
                shipments.map((shipment, index) => (
                  <tr
                    key={index}
                    className={
                      index % 2 === 0 ? "bg-white" : "bg-gray-50 hover:bg-blue-50"
                    }
                  >
                    <td className="px-4 py-3 font-mono">{shipment.shipment_id}</td>
                    <td className="px-4 py-3">{shipment.shipment_status}</td>
                    <td className="px-4 py-3">
                      {shipment.priority_score != null
                        ? shipment.priority_score.toFixed(2)
                        : "N/A"}
                    </td>
                    <td className="px-4 py-3">
                      {new Date(shipment.created_at).toLocaleString()}
                    </td>
                    <td className="px-4 py-3">
                      {new Date(shipment.updated_at).toLocaleString()}
                    </td>
                    <td className="px-4 py-3">{shipment.shelf_life_days} days</td>
                    <td className="px-4 py-3">
                      {shipment.volume ? shipment.volume.toFixed(2) : "N/A"} m³
                    </td>
                    <td className="px-4 py-3">
                      {shipment.weight ? shipment.weight.toFixed(2) : "N/A"} kg
                    </td>
                    <td className="px-4 py-3">
                      {shipment.value ? shipment.value.toFixed(2) : "N/A"} $
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default App;
