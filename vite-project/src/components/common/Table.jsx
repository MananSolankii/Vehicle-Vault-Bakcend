// import React from 'react'

// export const Table = () => {
//   return (
//     const [cars, setCars] = useState([]);
//   const [loading, setLoading] = useState(true);
//   const [error, setError] = useState(null);

//   useEffect(() => {
//     const fetchCars = async () => {
//       try {
//         const response = await fetch('YOUR_API_ENDPOINT_HERE'); // Add your API endpoint here
//         if (!response.ok) {
//           throw new Error('Network response was not ok');
//         }
//         const data = await response.json();
//         setCars(data);
//       } catch (error) {
//         setError(error.message);
//       } finally {
//         setLoading(false);
//       }
//     };

//     fetchCars();
//   }, []);

//   if (loading) return <div>Loading...</div>;
//   if (error) return <div>Error: {error}</div>;

//   return (
//     <div>
//       <table>
//         <thead>
//           <tr>
//             <th>Car Model</th>
//             <th>Year</th>
//             <th>Price</th>
//             <th>Features</th>
//           </tr>
//         </thead>
//         <tbody>
//           {cars.map((car) => (
//             <tr key={car.id}>
//               <td>{car.model}</td>
//               <td>{car.year}</td>
//               <td>{car.price}</td>
//               <td>{car.features.join(', ')}</td>
//             </tr>
//           ))}
//         </tbody>
//       </table>
//     </div>
//   )
// )
// }

