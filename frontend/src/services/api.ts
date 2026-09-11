/**
 * Base API client for ClimateEye AI backend.
 * Provides unified request handling and error processing.
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

export interface ApiResponse<T = unknown> {
  status: string;
  message?: string;
  data?: T;
  [key: string]: unknown;
}

export class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  async get<T>(endpoint: string, params?: Record<string, string | number>): Promise<T> {
    let url = `${this.baseUrl}${endpoint}`;
    if (params) {
      const searchParams = new URLSearchParams();
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          searchParams.append(key, String(value));
        }
      });
      const queryString = searchParams.toString();
      if (queryString) {
        url += `?${queryString}`;
      }
    }

    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`API GET request failed with status ${response.status}: ${response.statusText}`);
    }

    return response.json();
  }

  async post<T, B = unknown>(endpoint: string, body: B): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      throw new Error(`API POST request failed with status ${response.status}: ${response.statusText}`);
    }

    return response.json();
  }
}

export const apiClient = new ApiClient();
