import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatSelectModule } from '@angular/material/select';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatCardModule } from '@angular/material/card';

interface FileItem {
  name: string;
  path: string;
  isDir: boolean;
  isSrt: boolean;
}

@Component({
  selector: 'app-translator',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    MatButtonModule,
    MatSelectModule,
    MatProgressBarModule,
    MatCardModule
  ],
  templateUrl: './translator.component.html',
  styleUrl: './translator.component.scss'
})
export class TranslatorComponent {
  items: FileItem[] = [];
  models: string[] = [];
  selectedFile = '';
  targetLang = 'ja';
  selectedModel = 'gemma2:27b';
  translating = false;
  progress = 0;
  log = '';

  private api = 'http://localhost:5000/api';
  private token = localStorage.getItem('token');

  constructor(private http: HttpClient) {
    this.loadModels();
    this.loadFolder('');
  }

  private headers() {
    return { headers: { Authorization: `Bearer ${this.token}` } };
  }

  loadModels() {
    this.http.get<string[]>(`${this.api}/models`, this.headers())
      .subscribe(m => this.models = m);
  }

  loadFolder(path: string) {
    this.http.post<any>(`${this.api}/tree`, { path }, this.headers())
      .subscribe(res => this.items = res.items);
  }

  selectFile(path: string) {
    this.selectedFile = '/mnt/media/' + path;
  }

  translate() {
    if (!this.selectedFile) return;

    this.translating = true;
    this.progress = 0;
    this.log = 'Starting translation...\n';

    this.http.post<any>(`${this.api}/translate`, {
      file: this.selectedFile,
      lang: this.targetLang,
      model: this.selectedModel
    }, this.headers()).subscribe({
      next: (res: any) => {
        this.log += res.output || '';
        if (res.success) this.log += '\nTRANSLATION COMPLETED!\n';
      },
      error: (err) => this.log += `\nERROR: ${err.error?.error || 'Unknown'}\n`,
      complete: () => {
        this.translating = false;
        this.progress = 100;
      }
    });

    // Smooth fake progress
    const iv = setInterval(() => {
      if (this.progress < 90) this.progress += 8;
    }, 1500);
    setTimeout(() => clearInterval(iv), 120000);
  }
}