/**
 * Chat Service for ClimateEye AI frontend.
 * Prepares AI interaction communication with backend.
 */

import { apiClient, ApiResponse } from './api';

export interface ChatResponse {
  status: string;
  response?: string;
  message?: string;
  gemini_configured?: boolean;
}

export const chatService = {
  /**
   * Send a question to the environmental intelligence chatbot.
   */
  async sendMessage(message: string, context?: string): Promise<ApiResponse<ChatResponse>> {
    return apiClient.post<ApiResponse<ChatResponse>>('/api/chat', {
      message,
      context,
    });
  },
};
