import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../services/api';

@Component({
  selector: 'app-help',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './help.html',          // ← cambiado
  styleUrl: './help.css'               // ← opcional, si existe
})
export class HelpComponent implements OnInit {
  readme = 'Loading guide...';

  constructor(private api: ApiService) {}

  ngOnInit(): void {
    this.api.getReadme().subscribe({
      next: (res: { content: string }) => this.readme = res.content,
      error: () => this.readme = 'Could not load guide.'
    });
  }
}