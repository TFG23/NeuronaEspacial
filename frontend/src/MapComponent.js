import { useState, useEffect, useRef } from "react";
import { GoogleMap, LoadScript, Rectangle } from "@react-google-maps/api";

const containerStyle = {
  width: "100%",
  height: "400px"
};

const defaultCenter = {
  lat: 40.73061,
  lng: -73.935242
};




function MapComponent() {
  // console.log("MapComponent rendered");
  const [rectangle, setRectangle] = useState(null);
  
  const onLoad = (r) =>{
    if (r !== null) setRectangle(r)
  }

  const boundsChanged = () =>{
    console.log(rectangle);

  } 
  return (
    <LoadScript googleMapsApiKey="AIzaSyA1QWTppXmqZ3uzeyb9nlV5h9tul9-n52Q">
      <GoogleMap
        mapContainerStyle={containerStyle}
        center={defaultCenter}
        zoom={10}
        onLoad={(map) => (console.log(map))}
      >
        <Rectangle
          bounds={{
            north: defaultCenter.lat + 0.1,
            south: defaultCenter.lat - 0.1,
            east: defaultCenter.lng + 0.1,
            west: defaultCenter.lng - 0.1
          }}
          editable
          draggable
          options={{ fillColor: "rgba(0, 0, 255, 0.2)", strokeColor: "blue" }}
          onLoad={onLoad}
          onBoundsChanged={boundsChanged}
        />
      </GoogleMap>
    </LoadScript>
  );
}

export default MapComponent;