import { bootstrapApplication } from '@angular/platform-browser';
import { appConfig } from './app/app.config';
import { App } from './app/app';
import { contextNoeComponent } from './context-noe/context-noe.ts';

bootstrapApplication(App, appConfig)
  .catch((err) => console.error(err));
