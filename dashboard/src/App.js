// import logo from './logo.svg';
// import './App.css';
import Summary from './components/Summary';
import RequestsByKey from './components/RequestsByKey';
import StatusCodes from './components/StatusCodes';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  Tooltip,
  Legend
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  Tooltip,
  Legend
);



function App() {
  return (
    <div style={{ padding: "20px" }}>
      <h1>API Gateway Dashboard</h1>
      <Summary />
      <h2>Requests by API Key</h2>
      <RequestsByKey />
      <h2>Status Codes</h2>
      <StatusCodes />
    </div>
  );
}

export default App;
