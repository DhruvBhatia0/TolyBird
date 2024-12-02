const API_BASE_URL = '/api';

export interface SubmissionRequest {
  tweet_text: string;
  bid_amount: number;
}

export interface SubmissionResponse {
  submission_id: number;
  tweet_text: string;
  bid_amount: number;
  created_at: string;
  message: string;
}

export const createSubmission = async (data: SubmissionRequest): Promise<SubmissionResponse> => {
  const response = await fetch(`${API_BASE_URL}/submissions`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  const contentType = response.headers.get("content-type");
  if (!contentType || !contentType.includes("application/json")) {
    throw new Error(`Server returned ${response.status} ${response.statusText}`);
  }

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.error || 'Failed to create submission');
  }

  return response.json();
}; 