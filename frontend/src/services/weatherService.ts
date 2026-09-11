/**
 * Weather Service for ClimateEye AI frontend.
 * Prepares API communication for environmental metrics.
 */

import { apiClient, ApiResponse } from './api';

export interface WeatherMetrics {
  latitude: number;
  longitude: number;
  timezone?: string;
  temperature?: number;
  apparent_temperature?: number;
  humidity?: number;
  cloud_cover?: number;
  precipitation?: number;
  wind_speed?: number;
  wind_direction?: number;
  weather_condition?: string;
  weather_code?: number;
  time?: string;
}

export const weatherService = {
  /**
   * Fetch current environmental metrics for coordinates.
   */
  async getWeather(latitude?: number, longitude?: number): Promise<ApiResponse<WeatherMetrics>> {
    const params: Record<string, string | number> = {};
    if (latitude !== undefined) params.latitude = latitude;
    if (longitude !== undefined) params.longitude = longitude;

    return apiClient.get<ApiResponse<WeatherMetrics>>('/api/weather', params);
  },
};
