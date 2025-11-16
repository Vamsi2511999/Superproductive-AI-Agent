import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { Task } from '../models/task.model';

@Injectable({ providedIn: 'root' })
export class ApiService {
  private base = environment.apiUrl;
  constructor(private http: HttpClient) {}

  getTasks(): Observable<Task[]> {
    return this.http.get<Task[]>(`${this.base}/tasks`);
  }

  getTasksByDateRange(start: string, end: string): Observable<Task[]> {
    return this.http.get<Task[]>(`${this.base}/tasks?start=${encodeURIComponent(start)}&end=${encodeURIComponent(end)}`);
  }

  createTaskFromRaw(raw: any): Observable<Task[]> {
    // backend will run extractor and return tasks
    return this.http.post<Task[]>(`${this.base}/extract`, raw);
  }

  chatQuery(message: string): Observable<any> {
    return this.http.post<any>(`${this.base}/chat`, { message });
  }
}