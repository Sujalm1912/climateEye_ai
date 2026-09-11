/**
 * Location Service for ClimateEye AI frontend.
 * Prepares geocoding and location search communication with backend.
 */

import { apiClient, ApiResponse } from './api';

export interface LocationResult {
  id: number;
  city: string;
  latitude: number;
  longitude: number;
  country?: string;
  country_code?: string;
  state_or_region?: string;
  timezone?: string;
}

export const locationService = {
  /**
   * Search for locations by name or region.
   */
  async searchLocation(query: string): Promise<ApiResponse<LocationResult[]>> {
    return apiClient.get<ApiResponse<LocationResult[]>>('/api/location/search', { q: query });
  },
};
