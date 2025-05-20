import axios from "axios";

export async function fetchWeather(lat: number, lon: number) {
  const response = await axios.get(`https://api.ambeedata.com/weather/latest/by-lat-lng`, {
    params: { lat, lng: lon },
    headers: { "x-api-key": "YOUR_AMBEE_API_KEY" }
  });
  return response.data;
}
