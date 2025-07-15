import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-response-form',
  standalone: true,
  imports: [],
  templateUrl: './response-form.html',
  styleUrl: './response-form.scss'
})
export class ResponseForm implements OnInit {
  monTexteMarkdown! : string;

  ngOnInit() {
    this.monTexteMarkdown = `
    ## Titre

    Voici du code :

    \`\`\`javascript
    function coucou() {
      return "salut 🧠";
    }
    \`\`\`
    `;
  }
}

