import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface SubtitleFile {
  path: string;
  name: string;
  relative: string;
}

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private baseUrl = 'http://192.168.0.6:5001/api';

  constructor(private http: HttpClient) {}

  getFiles(): Observable<SubtitleFile[]> {
    return this.http.get<SubtitleFile[]>(`${this.baseUrl}/files`);
  }

  getModels(): Observable<string[]> {
    return this.http.get<string[]>(`${this.baseUrl}/models`);
  }

  getReadme(): Observable<{ content: string }> {
    return this.http.get<{ content: string }>(`${this.baseUrl}/readme`);
  }

  translate(data: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/translate`, data);
  }
}