import React from 'react';
import './App.css';
import Tabs from "./components/Tabs";
import Notification from "./components/Notification";
import Loader from "./components/Loader";

function App() {
  return (
      <div style={{height: '100vh', maxHeight: '100vh'}}>
          <Tabs/>
          <Notification/>
          <Loader/>
      </div>
  );
}

export default App;
