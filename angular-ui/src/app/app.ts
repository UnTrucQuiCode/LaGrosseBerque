import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import {SearchEngine} from './search-engine/search-engine';
import {ContextNoe} from './context-noe/context-noe';
import {ResponseForm} from './response-form/response-form';

@Component({
  selector: 'app-root',
  standalone:true,
  imports: [RouterOutlet, SearchEngine, ContextNoe, ResponseForm],
  templateUrl: './search-engine/search-engine.html',
  styleUrl: './app.scss'
})
export class App {
  protected readonly title = signal('angular-ui');
}
