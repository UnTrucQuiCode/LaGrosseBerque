import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import {SearchEngine} from './search-engine/search-engine';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App {
  protected readonly title = signal('angular-ui');
}
