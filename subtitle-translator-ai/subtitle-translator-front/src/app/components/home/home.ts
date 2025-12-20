import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService, SubtitleFile } from '../../services/api';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './home.html',
  styleUrl: './home.css'
})
export class HomeComponent implements OnInit {
  files: SubtitleFile[] = [];
  models: string[] = [];
  selectedFile: string = '';
  lang: string = 'ja';
  context: string = '';
  model: string = 'gemma2:27b';
  testMode: boolean = false;
  loading = false;
  output: string = '';
  outputFile: string | null = null;

  constructor(private api: ApiService) {}

  ngOnInit(): void {
    this.loadFiles();
    this.loadModels();
  }

  loadFiles(): void {
    this.loading = true;
    this.api.getFiles().subscribe({
      next: (data) => {
        this.files = data;
        this.loading = false;
      },
      error: (err) => {
        this.output = 'Error loading files: ' + (err.error?.error || err.message);
        this.loading = false;
      }
    });
  }

  loadModels(): void {
    this.api.getModels().subscribe({
      next: (data) => this.models = data,
      error: () => this.models = ['gemma2:27b', 'gemma2:9b']
    });
  }

  translate(): void {
    if (!this.selectedFile || !this.lang) {
      this.output = 'Please select a file and target language.';
      return;
    }

    this.loading = true;
    this.output = 'Starting translation...\n\n';

    const payload = {
      path: this.selectedFile,
      lang: this.lang.trim(),
      context: this.context.trim(),
      model: this.model,
      test: this.testMode ? 5 : null
    };

    this.api.translate(payload).subscribe({
      next: (res: any) => {
        this.output += res.output || 'No output from server.';
        this.outputFile = res.output_file;
        if (res.success) {
          this.output += '\n\n✓ Translation completed successfully!';
        }
        this.loading = false;
      },
      error: (err) => {
        this.output += '\nError: ' + (err.error?.details || err.error?.error || err.message);
        this.loading = false;
      }
    });
  }
}