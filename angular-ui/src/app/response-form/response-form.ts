import { Component, OnInit } from '@angular/core';
import { MarkdownModule } from 'ngx-markdown';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpClientModule } from '@angular/common/http';


@Component({
  selector: 'app-response-form',
  standalone: true,
  imports: [MarkdownModule, FormsModule, HttpClientModule],
  templateUrl: './response-form.html',
  styleUrl: './response-form.scss'
})
export class ResponseForm implements OnInit {
  monTexteMarkdown! : string;
  message: string = '';
  author: string = 'Noe';
  type: string = 'response';
  saving = false;
  saveOk = false;
  saveError: string | null = null;
  lastSavedId: number | null = null;

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.monTexteMarkdown = `
    ## Titre

    p_i = exp(w_i) / Σ exp(w_j)

    Voici du code :

    \`\`\`javascript
    function coucou() {
      return "salut 🧠";
    }
    \`\`\`
    `;
  }

  onSubmit() {
    if (!this.message || this.saving) return;
    this.saving = true;
    this.saveOk = false;
    this.saveError = null;

    const trimmed = this.message.trim();
    const payload = {
      type: this.type || 'response',
      content: trimmed,
      content_complete: trimmed,
      author: this.author || 'Nemo'
    };

    this.http.post<any>('http://localhost:8000/souvenirs/', payload).subscribe({
      next: (res) => {
        this.saveOk = true;
        this.lastSavedId = res?.mem_id ?? null;
        this.message = '';
        this.saving = false;
      },
      error: (err) => {
        this.saveError = (err?.error?.detail || err?.message || 'Erreur inconnue');
        this.saving = false;
      }
    });
  }
}
