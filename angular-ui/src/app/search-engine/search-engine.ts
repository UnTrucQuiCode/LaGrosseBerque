import { Component } from '@angular/core';
import { MarkdownModule } from 'ngx-markdown';


@Component({
  selector: 'app-search-engine',
  standalone: true,
  templateUrl: './search-engine.html',
  styleUrls: ['./search-engine.scss'],
  imports: [MarkdownModule]
})

export class SearchEngine {

}
