import React, { useState, useEffect } from "react";
import { useSearchParams } from "react-router-dom";
import "../../assets/CSS/SearchCar.css";

const CarSearch = () => {
  const [searchParams] = useSearchParams();
  const query = searchParams.get("query");
  const [car, setCar] = useState(null);

  useEffect(() => {
    const fetchCar = async () => {
      try {
        const response = await fetch(`http://localhost:8000/search-cars?query=${query}`);
        const data = await response.json();
        if (data.length > 0) {
          setCar(data[0]);
        }
      } catch (error) {
        console.error("Error fetching car data:", error);
      }
    };
    if (query) fetchCar();
  }, [query]);

  if (!car) return <p>Loading...</p>;

  return (
    <div className="search-car-container">
      <div className="car-image">
        <img src={car.image_url} alt={car.name} />
      </div>
      <div className="car-details">
        <h2>{car.name}</h2>
        <p className="price">Rs. {car.price}</p>
        <p className="variant">Variant: {car.variant || "Not Available"}</p>
        <p className="city">Ex-Showroom price, {car.city || "Unknown"}</p>
        <button className="offer-button">Get Offers</button>
      </div>
    </div>
  );
};

export default CarSearch;