import axios from "axios";
import { useEffect, useState } from "react";
import { Bar } from "react-chartjs-2";

export default function RequestsByKey() {
    const [chartData, setChartData] = useState({
        labels: [],
        datasets: []
    });

    useEffect(()=> {
        axios.get("http://localhost:8000/analytics/by-key")
            .then(res=> {
                const labels = res.data.map(item => item.api_key || "Unknown");
                const values = res.data.map(item => item.count);
                // console.log(labels)
                // console.log(values)
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

    return <Bar data={chartData} />;
}