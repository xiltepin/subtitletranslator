import { Component, OnInit, OnDestroy, NgZone, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService, SubtitleFile } from '../../services/api';
import { FilterPipe } from '../../pipes/filter-pipe';

declare var bootstrap: any; // Para usar Bootstrap Modal

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, FormsModule, FilterPipe],
  providers: [ApiService],
  templateUrl: './home.html',
  styleUrl: './home.css'
})
export class HomeComponent implements OnInit, OnDestroy {
  files: SubtitleFile[] = [];
  models: string[] = [];
  selectedFile: string = '';
  lang: string = 'ja';
  context: string = '';
  model: string = 'gemma3:12b';
  testMode: boolean = false;

  loading = false;        // para carga inicial de archivos y spinner
  translating = false;    // para deshabilitar formulario y mostrar progress bar durante traducción

  progress: number = 0;
  output: string = '';
  outputFile: string | null = null;

  private eventSource: EventSource | null = null;

  constructor(private api: ApiService, private zone: NgZone, private cdr: ChangeDetectorRef) {}

  ngOnInit(): void {
    this.loadFiles();
    this.loadModels();
  }

  ngOnDestroy(): void {
    this.closeEventSource();
  }
  

  searchTerm: string = '';
  selectedFileName: string = '';

  getFileName(path: string): string {
    if (!path) return '';
    return path.split('/').pop() || '';
  }

  // Para cerrar la lista al seleccionar
  selectFile(file: SubtitleFile) {
    this.selectedFile = file.path;
    this.selectedFileName = file.relative;
    this.searchTerm = file.relative;
  }

  loadFiles(): void {
    console.log('[loadFiles] START - setting loading=true');
    this.loading = true;
    this.output = 'Cargando lista de archivos subtítulos... (puede tardar unos segundos)\n';

    this.api.getFiles().subscribe({
      next: (data) => {
        console.log('[loadFiles] SUCCESS - received', data.length, 'files');
        this.files = data;
        this.loading = false;
        this.cdr.markForCheck();
        this.output += `¡Biblioteca cargada exitosamente! 🎉\n`;
        this.output += `📁 Encontrados ${data.length} archivos .srt listos para traducir\n\n`;
        this.output += `Selecciona un archivo y pon un buen contexto para calidad máxima 🔥\n\n`;
        console.log('[loadFiles] DONE - loading is now false, files.length=', this.files.length);
      },
      error: (err) => {
        console.log('[loadFiles] ERROR:', err);
        this.loading = false;
        this.cdr.markForCheck();
        this.output += '❌ Error al cargar archivos: ' + (err.error?.error || err.message || 'Servidor no responde') + '\n';
        this.output += 'Asegúrate de que el backend Flask esté corriendo en http://localhost:5000\n\n';
      }
    });
  }

  loadModels(): void {
    this.api.getModels().subscribe({
      next: (data) => this.models = data,
      error: () => this.models = ['gemma3:12b', 'gemma2:9b']
    });
  }

  translate(): void {
    if (!this.selectedFile || !this.lang) {
      this.output += '⚠️ Por favor selecciona un archivo y el idioma destino.\n';
      return;
    }

    this.closeEventSource();

    this.translating = true;
    this.progress = 0;
    this.outputFile = null;
    this.output += 'Iniciando traducción...\n\n';

    const params = new URLSearchParams();
    params.append('path', this.selectedFile);
    params.append('lang', this.lang.trim());
    if (this.context.trim()) params.append('context', this.context.trim());
    params.append('model', this.model);
    if (this.testMode) params.append('test', '5');

    this.eventSource = new EventSource(`http://localhost:5000/api/translate?${params.toString()}`);

    this.eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        console.log('[SSE onmessage] data:', data);

        if (data.type === 'progress') {
          this.zone.run(() => {
            console.log('[SSE progress] updating to', data.percent, '%');
            this.progress = data.percent;
            console.log('[SSE progress] progress is now:', this.progress);
            this.cdr.detectChanges();
          });
        } else if (data.type === 'log') {
          this.zone.run(() => {
            this.output += data.message + '\n';
            this.cdr.detectChanges();
          });
        } else if (data.type === 'complete') {
          this.zone.run(() => {
            this.outputFile = data.output_file;
            this.progress = 100;
            this.output += '\n¡Traducción completada con éxito! 🎉\n';
            this.translating = false;
            this.cdr.detectChanges();
            this.closeEventSource();
            
            // Mostrar el modal
            this.showSuccessModal();
          });
        } else if (data.type === 'error') {
          this.zone.run(() => {
            this.output += '\nERROR: ' + data.message + '\n';
            this.translating = false;
            this.cdr.detectChanges();
            this.closeEventSource();
          });
        }
      } catch (e) {
        console.log('[SSE onmessage] error parsing JSON:', e);
      }
    };

    this.eventSource.onerror = () => {
      this.output += '\nConexión perdida o error en el servidor.\n';
      this.translating = false;
      this.closeEventSource();
    };
  }

  private showSuccessModal(): void {
    const modalElement = document.getElementById('successModal');
    if (modalElement) {
      const modal = new bootstrap.Modal(modalElement);
      modal.show();
    }
  }

  private closeEventSource(): void {
    if (this.eventSource) {
      this.eventSource.close();
      this.eventSource = null;
    }
  }
}