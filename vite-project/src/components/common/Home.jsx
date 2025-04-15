import React from 'react';
import '../../assets/css/Home.css'; // Import CSS

const Home = () => {
  return (
    <div className="homepage">
      {/* Car Comparison Section */}
      <div className="comparison-section">
        <h1>Compare Cars</h1>
        <p>
          Important decisions like car purchase are often confusing. The “Compare Cars” tool from Vehicle Vault is designed to help you in car comparison on the basis of prices, mileage, power, performances, and other features and specifications. Our car comparison tool now comes with enhanced capabilities to compare cars at version level.
        </p>
        {/* <p>To get started, here’s a comparison for the top 2 most popular cars: <strong>Creta vs Seltos</strong>.</p> */}

        {/* Four Box Fields */}
        <div className="car-selection">
          <div className="car-box">
            <span>Select Car</span>
          </div>
          <div className="car-box">
            <span>Select Car</span>
          </div>
          <div className="car-box">
            <span>Select Car</span>
          </div>
          <div className="car-box">
            <span>Select Car</span>
          </div>
        </div>

        {/* Compare Button */}
        <div className="compare-button">
          <button>Compare</button>
        </div>
      </div>
    </div>
  );
};

export default Home;