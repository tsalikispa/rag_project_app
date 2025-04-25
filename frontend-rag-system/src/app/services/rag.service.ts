// src/app/services/rag.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface QueryResponse {
  answer: string;
  sources: DocumentSource[];
  timing: {
    total_ms: number;
  };
}

export interface DocumentSource {
  id: string | number;
  document_name: string;
  page?: number;
  source: string;
}

export interface UploadResponse {
  id: string;
  name: string;
  chunk_count: number;
  message: string;
}

export interface RebuildIndexResponse {
  success: boolean;
  documents_processed: number;
  total_chunks: number;
  message: string;
}

@Injectable({
  providedIn: 'root'
})
export class RagService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) { }

  query(queryText: string): Observable<QueryResponse> {
    return this.http.post<QueryResponse>(`${this.apiUrl}/query/`, { query: queryText });
  }

  uploadDocument(formData: FormData): Observable<UploadResponse> {
    return this.http.post<UploadResponse>(`${this.apiUrl}/upload/`, formData);
  }

  rebuildIndex(): Observable<RebuildIndexResponse> {
    return this.http.post<RebuildIndexResponse>(`${this.apiUrl}/rebuild-index/`, {});
  }
}
