import './App.css';
import Header from './components/Header'
import SideMenuBar from "./components/SideMenuBar";
import Button from '@mui/material/Button';



function App() {
  return (
    <>
      <Header />
      <div className="container">
          <SideMenuBar />
      </div>
    </>
  );
}

export default App;
