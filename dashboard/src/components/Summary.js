import axios from "axios";
import { useEffect, useState } from "react";

export default function Summary() {
    const [data, setData] = useState({ total_requests: 0});

    useEffect(()=> {
        axios.get("http://localhost:8000/analytics/summary")
            .then(res=> setData(res.data));
    }, []);

    return (
        <div>
            <h2>Total Requests</h2>
            <h1>{data.total_requests}</h1>
        </div>
    );
}