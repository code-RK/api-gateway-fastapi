import { useEffect, useState } from "react";
import axios from "axios";
import { Pie } from "react-chartjs-2";

export default function StatusCodes() {
  const [chartData, setChartData] = useState({
    labels: [],
    datasets: []
  });

  useEffect(() => {
    axios.get("http://localhost:8000/analytics/status-codes")
      .then(res => {
        const labels = res.data.map(item => item.status_code);
        const values = res.data.map(item => item.count);

        setChartData({
          labels,
          datasets: [
            {
                data: values
            }
          ]
        });
      });
  }, []);

  return <Pie data={chartData} />;
}